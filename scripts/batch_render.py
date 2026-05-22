#!/usr/bin/env python3
"""Batch compile multiple LilyPond files in a directory."""

import argparse
import fnmatch
import json
import os
import shutil
import subprocess
import sys


def compile_one(
    path: str,
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
            "file": path,
            "ok": False,
            "exit_code": -1,
            "stderr": "lilypond not found in PATH.",
        }

    base, _ = os.path.splitext(os.path.basename(path))
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        output_base = os.path.join(output_dir, base)
    else:
        output_base = os.path.join(os.path.dirname(path) or ".", base)

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
    cmd.append(path)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=output_dir or os.path.dirname(path) or ".",
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "file": path,
            "ok": False,
            "exit_code": -2,
            "stderr": exc.stderr or "Timeout",
        }

    return {
        "file": path,
        "ok": result.returncode == 0,
        "exit_code": result.returncode,
        "stderr": result.stderr,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Batch render LilyPond files.")
    parser.add_argument("directory", help="Directory to scan")
    parser.add_argument("--pattern", default="*.ly", help="File pattern (default: *.ly)")
    parser.add_argument("--output-dir", help="Output directory")
    parser.add_argument(
        "--format",
        choices=["pdf", "png", "svg", "ps"],
        default="pdf",
        help="Output format (default: pdf)",
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue after a compilation failure",
    )
    parser.add_argument("--json", action="store_true", help="Output JSON")
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
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: not a directory: {args.directory}", file=sys.stderr)
        return 1

    files = sorted(
        [
            os.path.join(args.directory, f)
            for f in os.listdir(args.directory)
            if fnmatch.fnmatch(f, args.pattern)
        ]
    )

    results = []
    for path in files:
        result = compile_one(
            path,
            args.output_dir,
            args.format,
            args.no_point_and_click,
            args.resolution,
            args.backend,
            args.jobs,
            args.preview,
            args.timeout,
        )
        results.append(result)
        if not result["ok"] and not args.continue_on_error:
            break

    if args.json:
        print(json.dumps({"results": results}, indent=2))
    else:
        for r in results:
            status = "OK" if r["ok"] else "FAIL"
            print(f"[{status}] {r['file']} (exit {r['exit_code']})")
            if not r["ok"] and r.get("stderr"):
                for line in r["stderr"].splitlines()[:10]:
                    print(f"  {line}")

    failed = [r for r in results if not r["ok"]]
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
