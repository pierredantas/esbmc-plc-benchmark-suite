#!/usr/bin/env python3
"""Render a PLCopen LD body as IEC 61131-3 structured text.

Every element in a ladder rung carries a localId and a connectionPointIn naming the
localId(s) it is wired from. Reconstructing ST means walking that graph backwards from
each coil (or block input) to the power rail: two connections on one connectionPointIn
are parallel branches (OR), a chain of single-input elements is a series (AND). The
walk is memoized per localId so a contact feeding two coils is evaluated once.

Scope is the suite's own single-<LD>-body POUs (runner/adapters and the g_/ld_ corpus).
A file mixing LD with FBD or SFC bodies (imported Beremiz examples) renders only its
LD pous and is fine with that: the LD body is still valid PLCopen, and the caller
decides whether the mix is worth showing.

    python3 -m runner.ld_to_st benchmarks/traffic/g_traffic_light/clean.xml
"""
import collections
import sys
import xml.etree.ElementTree as ET

# Function blocks: called as statements against a declared instance.
FB_TYPES = {"TON", "TOF", "TP", "CTU", "CTD", "CTUD", "R_TRIG", "F_TRIG", "SR", "RS"}
# Standard functions: called as expressions, no instance.
FN_TYPES = {"AND", "OR", "XOR", "NOT", "EQ", "NE", "LE", "GE", "LT", "GT",
            "ADD", "SUB", "MUL", "DIV", "SEL", "LIMIT", "MOVE"}


def _is_fb_instance(el):
    """True when a <block> is a stateful function block, called as a statement."""
    return el.type_name in FB_TYPES or (
        el.type_name and el.type_name not in FN_TYPES and el.instance_name)


def strip_ns(tag):
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def ns_of(tag):
    """The `{uri}` prefix a tag carries, or "" for an unnamespaced document."""
    return tag[:tag.index("}") + 1] if tag.startswith("{") else ""


def local(el, tag):
    ns = ns_of(el.tag)
    return el.find(f"{ns}{tag}") if ns else el.find(tag)


def local_all(el, tag):
    ns = ns_of(el.tag)
    return el.findall(f"{ns}{tag}") if ns else el.findall(tag)


class Element:
    """One LD graph node: a rail, contact, coil, block, or in/outVariable."""

    def __init__(self, xml_el):
        self.kind = strip_ns(xml_el.tag)
        self.id = xml_el.get("localId")
        self.xml = xml_el
        self.negated = xml_el.get("negated") == "true"
        self.storage = xml_el.get("storage")
        var = local(xml_el, "variable")
        self.var = var.text.strip() if var is not None and var.text else None
        expr = local(xml_el, "expression")
        self.expr = expr.text.strip() if expr is not None and expr.text else None
        self.type_name = xml_el.get("typeName")
        self.instance_name = xml_el.get("instanceName")

    def inputs(self, formal=None):
        """The (refLocalId, formalParameter) pairs a connectionPointIn is wired from.

        `formal` selects one named input block (a block's <inputVariables>/<variable>
        wrapper) when the element carries several; None means the element's own single
        connectionPointIn (contact, coil, inVariable, outVariable).
        """
        if formal is None:
            cpi = local(self.xml, "connectionPointIn")
        else:
            cpi = None
            for v in local_all(local(self.xml, "inputVariables"), "variable"):
                if v.get("formalParameter") == formal:
                    cpi = local(v, "connectionPointIn")
                    break
        if cpi is None:
            return []
        out = []
        for conn in local_all(cpi, "connection"):
            out.append((conn.get("refLocalId"), conn.get("formalParameter")))
        return out

    def output_formals(self):
        names = []
        for v in local_all(local(self.xml, "outputVariables"), "variable"):
            names.append(v.get("formalParameter"))
        return names


class Pou:
    """One <pou>'s LD body: the element graph plus the ST it renders as."""

    def __init__(self, pou_el):
        self.name = pou_el.get("name")
        self.pou_type = pou_el.get("pouType")
        self.elements = {}
        self.inputs, self.outputs, self.locals_ = [], [], []
        self._collect_interface(pou_el)
        body = local(pou_el, "body")
        self.ld = local(body, "LD") if body is not None else None
        if self.ld is not None:
            for child in self.ld:
                el = Element(child)
                if el.id is not None:
                    self.elements[el.id] = el
        self.fb_instances = {}  # instanceName -> typeName, declared as encountered
        self._memo = {}
        self._in_progress = set()

    def _collect_interface(self, pou_el):
        iface = local(pou_el, "interface")
        if iface is None:
            return
        for group, sink in (("inputVars", self.inputs), ("outputVars", self.outputs),
                             ("localVars", self.locals_)):
            grp = local(iface, group)
            if grp is None:
                continue
            for v in local_all(grp, "variable"):
                type_el = local(v, "type")
                type_name = _type_text(type_el) if type_el is not None else "BOOL"
                sink.append((v.get("name"), type_name))

    def expr_for(self, ref_id, formal=None):
        """The ST boolean/value expression feeding a connectionPointIn's source.

        A malformed file could wire a refLocalId cycle (invalid PLCopen, never seen in
        this suite's corpus, but a build-time tool should degrade one page rather than
        crash the whole build over it), so re-entering a key still on the call stack
        returns a marker instead of recursing forever.
        """
        key = (ref_id, formal)
        if key in self._memo:
            return self._memo[key]
        if key in self._in_progress:
            return "(* cyclic reference *)"
        el = self.elements.get(ref_id)
        if el is None:
            return "(* unresolved *)"
        self._in_progress.add(key)
        try:
            result = self._expr_for_element(el, formal)
        finally:
            self._in_progress.discard(key)
        self._memo[key] = result
        return result

    def _expr_for_element(self, el, formal):
        if el.kind == "leftPowerRail":
            return "TRUE"
        if el.kind in ("contact",):
            upstream = self._series_or_parallel(el.inputs())
            var = f"NOT {el.var}" if el.negated else el.var
            return var if upstream == "TRUE" else f"({upstream} AND {var})"
        if el.kind == "inVariable":
            return f"NOT ({el.expr})" if el.negated else el.expr
        if el.kind == "block":
            return self._block_output(el, formal)
        if el.kind == "coil":
            # A coil feeding a downstream connectionPointIn passes its own rung value through.
            return self._series_or_parallel(el.inputs())
        return f"(* {el.kind} *)"

    def _series_or_parallel(self, refs):
        """OR the branches on one connectionPointIn, AND a single upstream chain."""
        if not refs:
            return "TRUE"
        terms = [self.expr_for(ref, formal) for ref, formal in refs]
        if len(terms) == 1:
            return terms[0]
        return "(" + " OR ".join(terms) + ")"

    def _block_output(self, el, formal):
        """A block's output expression: `<instance>.<formal>` for an FB, else inline."""
        if _is_fb_instance(el):
            name = el.instance_name or f"{el.type_name}_{el.id}"
            out_formal = formal or (el.output_formals()[:1] or ["Q"])[0]
            return f"{name}.{out_formal}"

        formals_in = {}
        for v in local_all(local(el.xml, "inputVariables"), "variable"):
            fp = v.get("formalParameter")
            refs = el.inputs(formal=fp)
            formals_in[fp] = self._series_or_parallel(refs) if refs else None
        args = list(formals_in.values())
        if el.type_name == "NOT":
            return f"NOT ({args[0]})"
        if el.type_name == "AND":
            return "(" + " AND ".join(args) + ")"
        if el.type_name == "OR":
            return "(" + " OR ".join(args) + ")"
        if el.type_name == "XOR":
            return "(" + " XOR ".join(args) + ")"
        if el.type_name in ("EQ", "NE", "LE", "GE", "LT", "GT"):
            op = {"EQ": "=", "NE": "<>", "LE": "<=", "GE": ">=", "LT": "<",
                  "GT": ">"}[el.type_name]
            return f"({args[0]} {op} {args[1]})"
        if el.type_name in ("ADD", "SUB", "MUL", "DIV"):
            op = {"ADD": "+", "SUB": "-", "MUL": "*", "DIV": "/"}[el.type_name]
            return "(" + f" {op} ".join(args) + ")"
        if el.type_name == "SEL":
            g, in0, in1 = formals_in.get("G"), formals_in.get("IN0"), formals_in.get("IN1")
            return f"SEL({g}, {in0}, {in1})"
        return f"{el.type_name}({', '.join(args)})"

    def statements(self):
        """One ST assignment (or IF for set/reset coils) per coil, in localId order.

        Block calls the coils depend on are emitted first, in the order their outputs
        are first read, so a call statement always precedes any expression that reads
        `<instance>.<formal>`.

        Two coils or outVariables can legally target the same identifier (two rungs
        gated on complementary conditions, only one ever live in a given scan) and the
        scan-order overwrite this renders is faithful to that. But rendered as bare
        sequential assignments, a reader cannot tell that case apart from a genuine
        always-wins collision, so a comment marks every target written more than once.
        """
        calls, seen_calls = [], set()

        visiting = set()

        def collect_calls(ref_id, formal=None):
            key = (ref_id, formal)
            if key in visiting:
                return  # a cyclic refLocalId; expr_for renders the marker for it
            visiting.add(key)
            try:
                el = self.elements.get(ref_id)
                if el is None:
                    return
                if el.kind == "block" and _is_fb_instance(el):
                    if el.id in seen_calls:
                        return
                    seen_calls.add(el.id)
                    formals_in = {}
                    for v in local_all(local(el.xml, "inputVariables"), "variable"):
                        fp = v.get("formalParameter")
                        refs = el.inputs(formal=fp)
                        for ref, sub_fp in refs:
                            collect_calls(ref, sub_fp)
                        formals_in[fp] = self._series_or_parallel(refs) if refs else None
                    name = el.instance_name or f"{el.type_name}_{el.id}"
                    self.fb_instances[name] = el.type_name
                    args = ", ".join(f"{k}:={v}" for k, v in formals_in.items()
                                      if v is not None)
                    calls.append(f"{name}({args});")
                elif el.kind == "block":
                    for v in local_all(local(el.xml, "inputVariables"), "variable"):
                        for ref, sub_fp in el.inputs(formal=v.get("formalParameter")):
                            collect_calls(ref, sub_fp)
                else:
                    for ref, fp in el.inputs(formal):
                        collect_calls(ref, fp)
            finally:
                visiting.discard(key)

        coils = sorted((e for e in self.elements.values() if e.kind == "coil"),
                        key=lambda e: int(e.id))
        out_only = sorted((e for e in self.elements.values() if e.kind == "outVariable"),
                           key=lambda e: int(e.id))
        targets = [c.var for c in coils] + [ov.expr or f"out_{ov.id}" for ov in out_only]
        write_counts = collections.Counter(targets)

        def mark(target, line):
            if write_counts[target] > 1:
                return line + f"  (* {write_counts[target]} writers to {target}: "\
                    "scan order decides which value survives *)"
            return line

        lines = []
        for coil in coils:
            for ref, fp in coil.inputs():
                collect_calls(ref, fp)
            expr = self._series_or_parallel(coil.inputs())
            if coil.storage == "set":
                line = f"IF {expr} THEN\n    {coil.var} := TRUE;\nEND_IF;"
            elif coil.storage == "reset":
                line = f"IF {expr} THEN\n    {coil.var} := FALSE;\nEND_IF;"
            elif coil.negated:
                line = f"{coil.var} := NOT {expr};"
            else:
                line = f"{coil.var} := {expr};"
            lines.append(mark(coil.var, line))

        for ov in out_only:
            for ref, fp in ov.inputs():
                collect_calls(ref, fp)
            expr = self._series_or_parallel(ov.inputs())
            target = ov.expr or f"out_{ov.id}"
            line = f"{target} := {'NOT ' if ov.negated else ''}{expr};"
            lines.append(mark(target, line))

        call_lines = [c for c in calls if c]
        return call_lines + lines


def _type_text(type_el):
    for child in type_el:
        tag = strip_ns(child.tag)
        if tag == "derived":
            return child.get("name")
        return tag
    return "BOOL"


def _var_block(keyword, vars_):
    if not vars_:
        return ""
    lines = [f"    {name} : {typ};" for name, typ in vars_]
    return f"{keyword}\n" + "\n".join(lines) + "\nEND_VAR\n"


def render_pou(pou):
    """One POU (program or function block) as ST source text."""
    lines = pou.statements()
    declared = {name for name, _ in pou.locals_}
    fb_vars = [(name, typ) for name, typ in pou.fb_instances.items()
               if name not in declared]
    header = "FUNCTION_BLOCK" if pou.pou_type == "functionBlock" else "PROGRAM"
    footer = "END_FUNCTION_BLOCK" if pou.pou_type == "functionBlock" else "END_PROGRAM"

    parts = [f"{header} {pou.name}"]
    parts.append(_var_block("VAR_INPUT", pou.inputs))
    parts.append(_var_block("VAR_OUTPUT", pou.outputs))
    local_decls = pou.locals_ + fb_vars
    parts.append(_var_block("VAR", local_decls))
    parts.append("\n" + "\n".join(lines) + "\n")
    parts.append(footer)
    return "\n".join(p for p in parts if p)


def translate(xml_path):
    """The ST rendering of every LD-bodied <pou> in a PLCopen XML file, in file order.

    Returns "" when the file has no LD body at all (a pure FBD/SFC program), so a
    caller can skip offering a translation rather than show an empty one.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    # <pou> is normally under <types><pous>, but a vendor export (Beckhoff/TwinCAT)
    # has been seen placing it under a proprietary <addData> extension instead. Search
    # the whole document rather than trust one canonical location. The namespace URI
    # itself also varies by exporter (tc6_0200 vs tc6_0201 seen in this corpus), so it
    # is read off the root tag rather than assumed.
    pou_tag = f"{ns_of(root.tag)}pou"
    rendered = []
    for pou_el in root.iter(pou_tag):
        pou = Pou(pou_el)
        if pou.ld is None:
            continue
        rendered.append(render_pou(pou))
    return "\n\n".join(rendered)


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(1)
    text = translate(sys.argv[1])
    print(text if text else "(* no LD body in this file *)")


if __name__ == "__main__":
    main()
