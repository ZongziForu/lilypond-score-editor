#!/usr/bin/env python3
"""Generate part wrapper .ly files from a manifest and optionally compile them."""

import argparse
import json
import os
import shutil
import subprocess
import sys


def load_manifest(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
    # Try YAML first
    try:
        import yaml

        return yaml.safe_load(data)
    except ImportError:
        pass
    # Fallback to JSON
    try:
        return json.loads(data)
    except json.JSONDecodeError as exc:
        print(
            f"Error: cannot parse manifest as YAML or JSON. PyYAML is required for YAML. ({exc})",
            file=sys.stderr,
        )
        sys.exit(1)


def make_wrapper(
    source_path: str,
    part: dict,
    manifest: dict,
    output_dir: str,
) -> str:
    rel_source = os.path.relpath(
        os.path.abspath(source_path),
        os.path.abspath(output_dir),
    )

    lines = [
        r'\version "2.24.4"',
        "",
        f'\\include "{rel_source}"',
    ]

    layout_include = part.get("layout_include") or manifest.get("layout_include")
    if layout_include:
        rel_layout = os.path.relpath(
            os.path.abspath(layout_include),
            os.path.abspath(output_dir),
        )
        lines.append(f'\\include "{rel_layout}"')

    includes = part.get("include_files") or manifest.get("include_files") or []
    for inc in includes:
        rel_inc = os.path.relpath(
            os.path.abspath(inc),
            os.path.abspath(output_dir),
        )
        lines.append(f'\\include "{rel_inc}"')

    lines.append("")
    output_name = part.get("output_name") or part["id"]
    lines.append(r"\book {")
    lines.append(f'  \\bookOutputName "{output_name}"')
    lines.append("")
    lines.append(r"  \header {")
    lines.append(f'    instrument = "{part["name"]}"')
    lines.append(r"  }")
    lines.append("")

    staff_type = part.get("staff_type", "Staff")
    instrument_name = part.get("instrument_name") or part["name"]
    short_name = part.get("short_instrument_name") or instrument_name
    midi_instrument = part.get("midi_instrument") or ""

    lines.append(r"  \score {")
    lines.append(f'    \\new {staff_type} \\with {{')
    lines.append(f'      instrumentName = "{instrument_name}"')
    lines.append(f'      shortInstrumentName = "{short_name}"')
    if midi_instrument:
        lines.append(f'      midiInstrument = "{midi_instrument}"')
    lines.append(r"    } {")

    if part.get("clef"):
        lines.append(f'      \\clef {part["clef"]}')

    music_ref = f"\\{part['variable']}"
    if part.get("transposition"):
        # transposition expected as "c d" or similar; keep it simple
        lines.append(f'      \\transpose {part["transposition"]} {{ {music_ref} }}')
    else:
        lines.append(f"      {music_ref}")

    lines.append(r"    }")
    lines.append("")
    lines.append(r"    \layout { }")
    lines.append(r"    \midi { }")
    lines.append(r"  }")
    lines.append(r"}")
    lines.append("")

    return "\n".join(lines)


def compile_wrapper(
    wrapper_path: str,
    fmt: str,
    no_point_and_click: bool,
    timeout: int,
) -> dict:
    lilypond = shutil.which("lilypond")
    if not lilypond:
        return {
            "ok": False,
            "exit_code": -1,
            "stderr": "lilypond not found in PATH.",
        }

    base, _ = os.path.splitext(wrapper_path)
    cmd = [lilypond, f"-f{fmt}", "-o", base]
    if no_point_and_click:
        cmd.append("-dno-point-and-click")
    cmd.append(wrapper_path)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.path.dirname(wrapper_path) or ".",
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "ok": False,
            "exit_code": -2,
            "stderr": exc.stderr or "Timeout",
        }

    return {
        "ok": result.returncode == 0,
        "exit_code": result.returncode,
        "stderr": result.stderr,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract parts from a LilyPond score via manifest.")
    parser.add_argument("source", help="Source .ly file")
    parser.add_argument("manifest", help="Manifest YAML/JSON file")
    parser.add_argument("--output-dir", default="build/parts", help="Output directory for wrappers")
    parser.add_argument("--compile", action="store_true", help="Compile generated wrappers")
    parser.add_argument(
        "--format",
        choices=["pdf", "png", "svg", "ps"],
        default="pdf",
        help="Output format (default: pdf)",
    )
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument(
        "--no-point-and-click",
        action="store_true",
        help="Disable point-and-click links",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Compilation timeout in seconds (default: 60)",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.source):
        print(f"Error: source not found: {args.source}", file=sys.stderr)
        return 1
    if not os.path.isfile(args.manifest):
        print(f"Error: manifest not found: {args.manifest}", file=sys.stderr)
        return 1

    manifest = load_manifest(args.manifest)
    os.makedirs(args.output_dir, exist_ok=True)

    results = []
    for part in manifest.get("parts", []):
        wrapper = make_wrapper(args.source, part, manifest, args.output_dir)
        wrapper_path = os.path.join(args.output_dir, f"{part['id']}.ly")
        with open(wrapper_path, "w", encoding="utf-8") as f:
            f.write(wrapper)

        result = {
            "id": part["id"],
            "wrapper_path": wrapper_path,
            "output_name": part.get("output_name") or part["id"],
        }

        if args.compile:
            comp = compile_wrapper(
                wrapper_path,
                args.format,
                args.no_point_and_click,
                args.timeout,
            )
            result["compile_status"] = "ok" if comp["ok"] else "failed"
            result["exit_code"] = comp["exit_code"]
            result["stderr_summary"] = comp.get("stderr", "")[:500]
        else:
            result["compile_status"] = "skipped"

        results.append(result)

    if args.json:
        print(json.dumps({"results": results}, indent=2))
    else:
        for r in results:
            print(f"Part: {r['id']}")
            print(f"  Wrapper: {r['wrapper_path']}")
            print(f"  Output name: {r['output_name']}")
            print(f"  Compile: {r['compile_status']}")
            if r.get("stderr_summary"):
                print(f"  Stderr: {r['stderr_summary']}")
            print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
