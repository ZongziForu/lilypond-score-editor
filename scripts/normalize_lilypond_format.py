#!/usr/bin/env python3
"""Conservative formatter for LilyPond files."""

import argparse
import sys


def normalize(lines: list[str]) -> list[str]:
    out: list[str] = []
    indent_level = 0
    indent_unit = 2

    for raw in lines:
        stripped = raw.rstrip()
        if not stripped:
            out.append("")
            continue

        # Very simple heuristic: count braces on the line
        opens = stripped.count("{") + stripped.count("<<")
        closes = stripped.count("}") + stripped.count(">>")

        # Adjust indent for lines that start with closing braces
        if stripped.startswith("}") or stripped.startswith(">>"):
            indent_level = max(0, indent_level - 1)

        indent = " " * (indent_unit * indent_level)
        out.append(indent + stripped.lstrip())

        # Adjust indent for next lines based on opens/closes
        net = opens - closes
        indent_level = max(0, indent_level + net)

    # Ensure trailing newline
    if out and out[-1] != "":
        out.append("")
    elif not out:
        out.append("")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Conservatively format a LilyPond file.")
    parser.add_argument("input", help="LilyPond file")
    parser.add_argument("--in-place", action="store_true", help="Edit file in place")
    parser.add_argument("--output", help="Output file path")
    args = parser.parse_args()

    if args.in_place and args.output:
        print("Error: --in-place and --output are mutually exclusive.", file=sys.stderr)
        return 1

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: file not found: {args.input}", file=sys.stderr)
        return 1

    formatted = normalize(lines)

    if args.in_place:
        with open(args.input, "w", encoding="utf-8") as f:
            f.writelines(line + ("\n" if not line.endswith("\n") else "") for line in formatted)
    elif args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.writelines(line + ("\n" if not line.endswith("\n") else "") for line in formatted)
    else:
        for line in formatted:
            sys.stdout.write(line + ("\n" if not line.endswith("\n") else ""))

    return 0


if __name__ == "__main__":
    sys.exit(main())
