#!/usr/bin/env python3
"""Compile a LilyPond file and report results.

Supports common backends (pdf, png, svg, ps) and engraving options.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys


def compile_lilypond(
    input_path: str,
    output_dir: str | None,
    fmt: str,
    no_point_and_click: bool,
    resolution: int | None,
    backend: str | None,
    jobs: int | None,
    preview: bool,
    timeout: int,
) -> dict:
    lilypond = shutil.which("lilypond")
    if not lilypond:
        return {
            "ok": False,
            "exit_code": -1,
            "command": "",
            "stdout": "",
            "stderr": "lilypond not found in PATH. Please install LilyPond.",
            "output_dir": output_dir,
            "input": input_path,
        }

    input_path = os.path.abspath(input_path)
    base, _ = os.path.splitext(os.path.basename(input_path))

    if output_dir:
        output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        output_base = os.path.join(output_dir, base)
    else:
        output_base = os.path.join(os.path.dirname(input_path), base)

    cmd = [lilypond, f"-f{fmt}", "-o", output_base]

    if no_point_and_click:
        cmd.append("-dno-point-and-click")

    if resolution is not None:
        cmd.append(f"-dresolution={resolution}")

    if backend is not None:
        cmd.append(f"-dbackend={backend}")

    if jobs is not None:
        cmd.append(f"-djob-count={jobs}")

    if preview:
        cmd.append("-dpreview")

    cmd.append(input_path)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=output_dir or os.path.dirname(input_path),
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "ok": False,
            "exit_code": -2,
            "command": " ".join(cmd),
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
            "output_dir": output_dir,
            "input": input_path,
        }

    return {
        "ok": result.returncode == 0,
        "exit_code": result.returncode,
        "command": " ".join(cmd),
        "stdout": result.stdout,
        "stderr": result.stderr,
        "output_dir": output_dir or os.path.dirname(input_path),
        "input": input_path,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a LilyPond file.")
    parser.add_argument("input", help="Path to .ly file")
    parser.add_argument("--output-dir", help="Output directory")
    parser.add_argument(
        "--format",
        choices=["pdf", "png", "svg", "ps"],
        default="pdf",
        help="Output format (default: pdf)",
    )
    parser.add_argument(
        "--no-point-and-click",
        action="store_true",
        help="Disable point-and-click links",
    )
    parser.add_argument(
        "--resolution",
        type=int,
        help="PNG resolution in DPI (e.g., 300)",
    )
    parser.add_argument(
        "--backend",
        choices=["svg", "ps", "eps", "cairo"],
        help="Explicit backend override",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        help="Number of parallel jobs (LilyPond -djob-count)",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Generate preview image (cropped first system)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Compilation timeout in seconds (default: 60)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output structured JSON",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Error: file not found: {args.input}", file=sys.stderr)
        return 1

    result = compile_lilypond(
        args.input,
        args.output_dir,
        args.format,
        args.no_point_and_click,
        args.resolution,
        args.backend,
        args.jobs,
        args.preview,
        args.timeout,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Command: {result['command']}")
        print(f"Exit code: {result['exit_code']}")
        if result["stdout"]:
            print("--- stdout ---")
            print(result["stdout"])
        if result["stderr"]:
            print("--- stderr ---")
            print(result["stderr"])
        print(f"Output dir: {result['output_dir']}")
        if result["ok"]:
            print("Result: OK")
        else:
            print("Result: FAILED")

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
