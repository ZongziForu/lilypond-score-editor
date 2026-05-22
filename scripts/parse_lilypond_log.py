#!/usr/bin/env python3
"""Parse LilyPond stdout/stderr/log and emit structured diagnostics."""

import argparse
import json
import re
import sys


PATTERNS = [
    ("error", re.compile(r"error:\s*(.*)")),
    ("error", re.compile(r"syntax error.*")),
    ("error", re.compile(r"unexpected\b.*")),
    ("error", re.compile(r"unknown escaped string.*")),
    ("error", re.compile(r"not a note name.*")),
    ("error", re.compile(r"cannot find file.*")),
    ("error", re.compile(r"Guile signaled an error.*")),
    ("error", re.compile(r"programming error.*")),
    ("error", re.compile(r"wrong type for argument.*")),
    ("warning", re.compile(r"warning:\s*(.*)")),
    ("error", re.compile(r"bar check failed.*")),
    ("warning", re.compile(r"lyrics do not align.*")),
    ("error", re.compile(r"unmatched.*")),
]


def parse_text(text: str) -> list[dict]:
    issues = []
    for line in text.splitlines():
        for severity, pat in PATTERNS:
            m = pat.search(line)
            if m:
                msg = m.group(0)
                # Try to extract line number
                line_no = None
                lm = re.search(r":(\d+):(\d+):", line)
                if lm:
                    line_no = int(lm.group(1))
                issue = {
                    "severity": severity,
                    "line": line_no,
                    "message": msg,
                    "likely_cause": infer_cause(msg),
                    "suggested_fix": infer_fix(msg),
                }
                issues.append(issue)
                break
    return issues


def infer_cause(msg: str) -> str:
    lower = msg.lower()
    if "syntax error" in lower or "unexpected" in lower:
        return "Missing or extra brace, bracket, or delimiter."
    if "bar check" in lower:
        return "Measure durations do not match the time signature."
    if "cannot find file" in lower:
        return "An \\include path is incorrect or the file is missing."
    if "guile" in lower:
        return "Invalid Scheme expression."
    if "lyrics" in lower and "align" in lower:
        return "Lyric syllable count does not match note events."
    if "unknown escaped" in lower or "not a note name" in lower:
        return "Typo in command or note name."
    return "Inspect the message and surrounding source lines."


def infer_fix(msg: str) -> str:
    lower = msg.lower()
    if "syntax error" in lower or "unexpected" in lower:
        return "Check braces, \\<< >>, and parentheses near the error line."
    if "bar check" in lower:
        return "Verify note/rest durations in the flagged measure."
    if "cannot find file" in lower:
        return "Correct the \\include path or create the missing file."
    if "guile" in lower:
        return "Review the Scheme expression for quoting and parentheses."
    if "lyrics" in lower and "align" in lower:
        return "Adjust syllables or add __ for melismas."
    if "unknown escaped" in lower or "not a note name" in lower:
        return "Fix the spelling typo."
    return "Make a minimal change near the reported location."


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse LilyPond log output.")
    parser.add_argument("log", nargs="?", help="Log file path (optional)")
    parser.add_argument("--text", help="Raw log text to parse")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    text = ""
    if args.text:
        text = args.text
    elif args.log:
        try:
            with open(args.log, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: file not found: {args.log}", file=sys.stderr)
            return 1
    else:
        text = sys.stdin.read()

    issues = parse_text(text)

    if args.json:
        print(json.dumps({"issues": issues}, indent=2))
    else:
        if not issues:
            print("No recognized issues found.")
        for issue in issues:
            line_str = f"line {issue['line']}" if issue["line"] else "unknown line"
            print(f"[{issue['severity'].upper()}] {line_str}: {issue['message']}")
            print(f"  Cause: {issue['likely_cause']}")
            print(f"  Fix:   {issue['suggested_fix']}")
            print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
