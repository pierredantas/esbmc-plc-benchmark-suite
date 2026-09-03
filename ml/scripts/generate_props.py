#!/usr/bin/env python3
"""Generate props.yaml for one IEC 61131-3 program via the fine-tuned SLM.

    python3 ml/scripts/generate_props.py path/to/program.st --domain motor_control --language ST
    python3 ml/scripts/generate_props.py path/to/program.st -o benchmarks/motor_control/new_task/props.yaml

Prints the generated YAML to stdout by default; pass -o/--out to write it to
a file instead (and suppress the stdout echo).
"""
import argparse
import sys
from pathlib import Path

from mlx_lm import load, generate
from mlx_lm.sample_utils import make_sampler

REPO_ROOT = Path(__file__).resolve().parents[2]

# The two checkpoints trained this session:
#   -iter300            152 raw benchmark examples, best val-loss checkpoint
#   -augmented-best      239 examples (+ ld_to_st.py ST renderings), final checkpoint
# Neither dominates the other — see ml/README.md for the tradeoffs — so the
# default below is a deliberate choice, not a "best" one; override with
# --adapter-path to try the other.
DEFAULT_ADAPTER = REPO_ROOT / "ml" / "adapters" / "qwen2.5-coder-1.5b-props-augmented-best"

SYSTEM_PROMPT = (
    "You are a formal-verification assistant for IEC 61131-3 PLC programs. "
    "Given the source of one program variant, emit its safety properties as "
    "a props.yaml document: format_version, then a properties list where each "
    "item has id (P1, P2, ...), kind (invariant | mutual_exclusion | absence | "
    "reachability | assertion | termination), an expression or variables list "
    "as the kind requires, and a one-sentence justification grounded in the "
    "program's physical/safety intent. Output only the YAML, no commentary."
)


def generate_props(source: str, domain: str, language: str, model_path: str, adapter_path: str, max_tokens: int) -> str:
    user_prompt = (
        f"Domain: {domain}\n"
        f"Language: {language}\n"
        f"Program:\n```\n{source}```\n\n"
        "Emit the props.yaml safety properties for this program."
    )

    model, tokenizer = load(model_path, adapter_path=adapter_path)
    # Qwen2.5's chat template ends turns with <|im_end|>, but the tokenizer's
    # eos_token_ids only has <|endoftext|>; without this generate() runs past
    # the turn boundary and appends trailing garbage after the YAML.
    im_end_ids = tokenizer.encode("<|im_end|>", add_special_tokens=False)
    tokenizer.eos_token_ids = set(tokenizer.eos_token_ids) | set(im_end_ids)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
    prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True)
    sampler = make_sampler(temp=0.0)
    return generate(model, tokenizer, prompt=prompt, max_tokens=max_tokens, sampler=sampler, verbose=False)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source_file")
    ap.add_argument("--domain", default="manufacturing")
    ap.add_argument("--language", default="ST")
    ap.add_argument("--model", default="mlx-community/Qwen2.5-Coder-1.5B-Instruct-4bit")
    ap.add_argument("--adapter-path", default=str(DEFAULT_ADAPTER))
    ap.add_argument("--max-tokens", type=int, default=512)
    ap.add_argument("-o", "--out", help="write the generated YAML here instead of printing it")
    args = ap.parse_args()

    source = Path(args.source_file).read_text()
    output = generate_props(source, args.domain, args.language, args.model, args.adapter_path, args.max_tokens)

    if args.out:
        Path(args.out).write_text(output.strip() + "\n")
        print(f"wrote {args.out}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
