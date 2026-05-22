#!/usr/bin/env python3
"""Auto-generate a parts manifest from a LilyPond score file.

Heuristics:
- Detects music variables (e.g., violinIMusic = \relative)
- Detects staff declarations with instrumentName
- Attempts to map variables to staves by order of appearance
- Suggests clefs based on instrument name or \clef commands in variables
"""

import argparse
import json
import os
import re
import sys


def extract_music_variables(text: str) -> list[dict]:
    """Find variable definitions that contain music (\relative, \absolute, \drummode, etc.)."""
    vars_found = []
    # Pattern: name = \relative  or  name = \drummode  etc.
    pattern = re.compile(
        r"^(\w+)\s*=\s*\\(?:relative|absolute|transpose|drummode|chordmode)\b",
        re.MULTILINE,
    )
    for m in pattern.finditer(text):
        name = m.group(1)
        # Skip common non-music variables
        if name in ("global", "layout", "paper", "header", "score", "book"):
            continue
        vars_found.append({"name": name, "line": text[: m.start()].count("\n") + 1})
    return vars_found


def extract_staffs(text: str) -> list[dict]:
    """Find \new Staff declarations and their instrument names."""
    staffs = []
    # Match \new Staff [\with { instrumentName = "..." }] followed by \variable or {
    pattern = re.compile(
        r"\\new\s+(Staff|DrumStaff|RhythmicStaff|TabStaff)"
        r"(?:\s*\\with\s*\{[^}]*instrumentName\s*=\s*\"([^\"]*)\"[^}]*\})?"
        r"(?:\s*\\[A-Za-z]+|\s*\{)",
        re.MULTILINE,
    )
    for m in pattern.finditer(text):
        staff_type = m.group(1)
        instrument_name = m.group(2) or ""
        staffs.append(
            {
                "type": staff_type,
                "instrument_name": instrument_name,
                "line": text[: m.start()].count("\n") + 1,
            }
        )
    return staffs


def guess_clef(variable_name: str, instrument_name: str, source_text: str) -> str:
    """Guess clef from context."""
    # Search for \clef in the variable definition
    # Find the variable block and look for \clef inside
    var_pattern = re.compile(
        rf"^{re.escape(variable_name)}\s*=.*?^(?=\w+\s*=|\\(score|book|paper|layout|header)\b|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    m = var_pattern.search(source_text)
    if m:
        block = m.group(0)
        clef_match = re.search(r"\\clef\s+\"?([^\"\s]+)\"?", block)
        if clef_match:
            return clef_match.group(1)

    # Guess from instrument name
    name_lower = instrument_name.lower()
    if any(x in name_lower for x in ("violin", "flute", "oboe", "clarinet", "trumpet")):
        return "treble"
    if any(x in name_lower for x in ("viola", "alto", "trombone", "cello", "bassoon")):
        if "viola" in name_lower or "alto" in name_lower:
            return "alto"
        return "tenor"
    if any(x in name_lower for x in ("cello", "bass", "double bass", "bassoon", "tuba")):
        if "cello" in name_lower:
            return "bass"
        return "bass"
    if "drum" in name_lower:
        return "percussion"

    return "treble"


def guess_midi_instrument(instrument_name: str) -> str:
    """Map instrument name to a MIDI instrument name."""
    mapping = {
        "violin": "violin",
        "viola": "viola",
        "cello": "cello",
        "double bass": "contrabass",
        "flute": "flute",
        "oboe": "oboe",
        "clarinet": "clarinet",
        "bassoon": "bassoon",
        "horn": "french horn",
        "trumpet": "trumpet",
        "trombone": "trombone",
        "tuba": "tuba",
        "piano": "acoustic grand",
        "guitar": "acoustic guitar (nylon)",
        "bass": "electric bass (finger)",
        "drum": "standard kit",
    }
    name_lower = instrument_name.lower()
    for key, value in mapping.items():
        if key in name_lower:
            return value
    return ""


def build_manifest(source_path: str, source_text: str) -> dict:
    variables = extract_music_variables(source_text)
    staffs = extract_staffs(source_text)

    parts = []
    # Heuristic: map variables to staffs by order of appearance
    # If counts match, pair them 1:1
    # If not, use all variables and let user edit
    for i, var in enumerate(variables):
        instrument_name = ""
        if i < len(staffs):
            instrument_name = staffs[i]["instrument_name"]

        # Generate a friendly id from variable name
        var_name = var["name"]
        part_id = re.sub(r"Music$", "", var_name)
        # Insert hyphens before capitals and lowercase (violinI -> violin-i)
        part_id = re.sub(r"([a-z])([A-Z])", r"\1-\2", part_id)
        part_id = part_id.lower().replace("_", "-")
        if not part_id:
            part_id = var_name.lower()

        clef = guess_clef(var_name, instrument_name, source_text)
        midi = guess_midi_instrument(instrument_name)

        part = {
            "id": part_id,
            "name": instrument_name or part_id.replace("-", " ").title(),
            "variable": var_name,
            "clef": clef,
        }
        if midi:
            part["midi_instrument"] = midi

        parts.append(part)

    manifest = {
        "source": os.path.basename(source_path),
        "output_dir": "build/parts",
        "parts": parts,
    }
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Auto-generate a parts manifest from a LilyPond score file."
    )
    parser.add_argument("source", help="Source .ly file")
    parser.add_argument("--output", "-o", help="Output manifest path (default: print to stdout)")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of YAML")
    args = parser.parse_args()

    if not os.path.isfile(args.source):
        print(f"Error: file not found: {args.source}", file=sys.stderr)
        return 1

    with open(args.source, "r", encoding="utf-8") as f:
        text = f.read()

    manifest = build_manifest(args.source, text)

    if args.json:
        output = json.dumps(manifest, indent=2)
    else:
        try:
            import yaml

            output = yaml.dump(manifest, sort_keys=False, allow_unicode=True)
        except ImportError:
            print(
                "Warning: PyYAML not installed; falling back to JSON. Install with: pip install pyyaml",
                file=sys.stderr,
            )
            output = json.dumps(manifest, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Manifest written to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
