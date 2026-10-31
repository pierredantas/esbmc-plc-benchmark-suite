"""Harness adjustment for programs written by others (R1.3): drop I/O addresses and declare every variable
that no coil writes as an input, so that all routes treat it as free. Nothing else changes.

    normalize_io.py IN.xml OUT.xml
"""
import sys
import xml.etree.ElementTree as ET

src, dst = sys.argv[1:3]
tree = ET.parse(src)
root = tree.getroot()
ns = root.tag[1:root.tag.index("}")] if root.tag.startswith("{") else ""
q = (lambda t: f"{{{ns}}}{t}") if ns else (lambda t: t)
ET.register_namespace("", ns)
for pou in root.iter(q("pou")):
    iface = pou.find(q("interface"))
    coils = {c.findtext(q("variable")) for c in pou.iter(q("coil"))}
    variables = []
    for block in list(iface):
        variables += [(block.tag, v) for v in list(block)]
        iface.remove(block)
    ins, outs, loc = ET.Element(q("inputVars")), ET.Element(q("outputVars")), ET.Element(q("localVars"))
    for _, v in variables:
        v.attrib.pop("address", None)
        t = v.find(q("type"))
        is_fb = t is not None and t.find(q("derived")) is not None
        (loc if is_fb else outs if v.get("name") in coils else ins).append(v)
    for b in (ins, outs, loc):
        if len(b):
            iface.append(b)
tree.write(dst, xml_declaration=True, encoding="utf-8")
