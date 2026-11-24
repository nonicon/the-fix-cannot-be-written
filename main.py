#!/usr/bin/env python3
"""The Fix Cannot Be Written — entry for make.fun's
"Say What Actually Broke" bounty.

Writes one line of software error copy (the brutal truth about
what actually broke) to /output/entry.txt. Deterministic, stdlib only.
"""

import os
import sys

ENTRY = (
    "The disk is full because we log everything, including this "
    "error about the disk being full — the fix cannot be written."
)


def validate_entry(text: str) -> str:
    """Enforce the kit gate from RULES.txt: UTF-8 text of 1-200
    characters, a single line, not only whitespace."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    text.encode("utf-8")  # must be valid UTF-8
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry is {len(text)} chars, must be 1-200")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    return text


def output_path() -> str:
    """Honour MAKEFUN_OUTPUT_DIR first, then legacy OUTPUT_DIR,
    then the default /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get(
        "OUTPUT_DIR", "/output"
    )
    return os.path.join(out_dir, "entry.txt")


def main() -> int:
    text = validate_entry(ENTRY.strip())
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    # Round-trip read-back: the written file must equal the entry exactly.
    with open(path, encoding="utf-8") as f:
        written = f.read()
    if written != text:
        raise RuntimeError("round-trip check failed: written file differs")
    print(f"wrote {len(text)} chars to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
