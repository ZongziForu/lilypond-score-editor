#!/usr/bin/env python3
"""Heuristic bar duration checker for LilyPond files.

Supports:
- Simple time signatures (4/4, 3/4, etc.)
- Compound time signatures (7+5/8, 3+2/4)
- Tuplets (\tuplet 3/2 { ... }, \tuplet 5/4 { ... })
- Grace notes (skipped)
- Chordmode / lyricmode / markup blocks (skipped)
"""

import argparse
import json
import os
import re
import sys


def duration_to_fraction(token: str) -> float:
    # token like 4, 8., 2.., 16
    m = re.match(r"^(\d+)(\.*)$", token)
    if not m:
        return 0.0
    base = int(m.group(1))
    dots = len(m.group(2))
    value = 4.0 / base
    add = value
    for _ in range(dots):
        add /= 2.0
        value += add
    return value


def parse_time_signature(line: str) -> tuple[int, int] | None:
    # Support compound meters like \time 7+5/8 or \time 3+2/4
    m = re.search(r"\\time\s+(?:(\d+)\+)*(\d+)/(\d+)", line)
    if m:
        # If there are plus-separated beats, sum them; otherwise use the single beat
        groups = m.groups()
        # groups will look like (None, '7', '8') for simple, or ('3', '2', '4') for compound
        # Actually regex behavior: (\d+)\+ is optional, so groups vary
        # Better approach: capture the whole numerator
        pass
    # Simpler approach: extract the full numerator string
    m = re.search(r"\\time\s+([\d+]+)/(\d+)", line)
    if m:
        num_str = m.group(1)
        den = int(m.group(2))
        beats = sum(int(x) for x in num_str.split("+"))
        return beats, den
    return None


def extract_durations(line: str, last_dur: str) -> tuple[list[tuple[str, float]], str]:
    """Extract explicit duration strings from a line with tuplet scaling.

    Returns (results, updated_last_dur) so duration inheritance works across lines.
    """
    # Remove simple scheme/markup blocks to reduce noise
    line = re.sub(r"#\([^)]*\)", "", line)
    line = re.sub(r"\\markup\s*\{[^}]*\}", "", line)
    # Remove common non-music commands that contain pitch names
    line = re.sub(r"\\(key|transpose|relative|clef)\s+\S+", "", line)

    # Match tuplet declarations: \tuplet 3/2 { or \tuplet 5/4 {
    tuplet_match = re.search(r"\\tuplet\s+(\d+)/(\d+)\s*\{", line)
    tuplet_ratio = 1.0
    if tuplet_match:
        actual = int(tuplet_match.group(1))
        normal = int(tuplet_match.group(2))
        tuplet_ratio = normal / actual

    # Match note/chord/rest with optional duration
    matches = re.finditer(
        r"(?P<token>(?<!\\)\b(?:[a-grs](?:is|es|isis|eses)?[,']*|[rs])(?![a-zA-Z])|<[^>]+>)(?P<dur>[\d]+\.?\.?)?",
        line,
    )
    results = []
    for m in matches:
        dur = m.group("dur")
        if dur:
            last_dur = dur
            results.append((dur, tuplet_ratio))
        else:
            token = m.group("token")
            if re.search(r"[a-grs]|<[^>]+>|\b[rs]\b", token):
                results.append((last_dur, tuplet_ratio))
    return results, last_dur


def check_file(path: str) -> list[dict]:
    issues = []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    beats_per_bar = 4
    beat_unit = 4
    # duration_to_fraction returns quarter-note units (quarter=1.0)
    bar_duration = 4.0  # 4/4 = 4 quarter notes

    current_bar = 0
    accumulated = 0.0
    bar_start_line = 1
    skip_depth = 0
    tuplet_depth = 0
    tuplet_ratio = 1.0
    last_dur = "4"  # LilyPond default duration is quarter

    for idx, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        # Skip comments entirely
        if line.startswith("%"):
            continue
        # Remove inline comments
        if "%" in line:
            line = line.split("%", 1)[0]

        # Track skip blocks (chordmode, lyricmode, markup)
        if skip_depth > 0:
            skip_depth += line.count("{") - line.count("}")
            if skip_depth <= 0:
                skip_depth = 0
            continue

        if re.search(r"\\(chordmode|lyricmode|markup)\b", line):
            skip_depth = line.count("{") - line.count("}")
            if skip_depth <= 0:
                skip_depth = 0
            continue

        # Skip grace lines heuristically
        if re.search(r"\\(grace|appoggiatura|acciaccatura)\b", line):
            continue

        # Track tuplet blocks
        if tuplet_depth > 0:
            tuplet_depth += line.count("{") - line.count("}")
            if tuplet_depth <= 0:
                tuplet_depth = 0
                tuplet_ratio = 1.0
            # Continue processing this line for notes within the tuplet

        ts = parse_time_signature(line)
        if ts:
            beats_per_bar, beat_unit = ts
            bar_duration = beats_per_bar * (4.0 / beat_unit)
            # Reset current bar tracking after a time signature change
            accumulated = 0.0
            current_bar = 0
            bar_start_line = idx
            last_dur = "4"
            continue

        # Check for tuplet start on this line
        if tuplet_depth == 0:
            tuplet_match = re.search(r"\\tuplet\s+(\d+)/(\d+)\s*\{", line)
            if tuplet_match:
                actual = int(tuplet_match.group(1))
                normal = int(tuplet_match.group(2))
                tuplet_ratio = normal / actual
                tuplet_depth = 1  # The opening brace is on this line

        durs, last_dur = extract_durations(line, last_dur)
        for dur_str, ratio in durs:
            accumulated += duration_to_fraction(dur_str) * ratio

        # Bar checks split measures
        if "|" in line:
            # Heuristic: count bar checks
            bars = line.split("|")
            # First chunk belongs to current bar
            for i, _ in enumerate(bars):
                if i > 0:
                    # Completed a bar
                    diff = accumulated - bar_duration
                    if abs(diff) > 1e-9:
                        issues.append(
                            {
                                "bar": current_bar + 1,
                                "line": bar_start_line,
                                "expected": bar_duration,
                                "actual": accumulated,
                                "message": f"Bar {current_bar + 1} duration mismatch (expected {bar_duration}, got {accumulated})",
                            }
                        )
                    current_bar += 1
                    accumulated = 0.0
                    bar_start_line = idx

    # Check final incomplete bar
    if abs(accumulated) > 1e-9 and abs(accumulated - bar_duration) > 1e-9:
        issues.append(
            {
                "bar": current_bar + 1,
                "line": bar_start_line,
                "expected": bar_duration,
                "actual": accumulated,
                "message": f"Final bar duration mismatch (expected {bar_duration}, got {accumulated})",
            }
        )

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Heuristic bar duration checker with tuplet and compound meter support.")
    parser.add_argument("input", help="LilyPond file")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Error: file not found: {args.input}", file=sys.stderr)
        return 1

    issues = check_file(args.input)

    if args.json:
        print(json.dumps({"issues": issues}, indent=2))
    else:
        if not issues:
            print("No obvious bar duration issues found.")
        for issue in issues:
            print(f"[WARNING] line {issue['line']}: {issue['message']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
