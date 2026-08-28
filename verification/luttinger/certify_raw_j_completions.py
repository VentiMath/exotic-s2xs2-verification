#!/usr/bin/env python3
"""Compile and independently replay certificates for raw j-scan completions."""

import argparse
import json
from pathlib import Path
import subprocess
import sys


BASE = Path(__file__).resolve().parent
ROOT = BASE.parent


def run(command):
    result = subprocess.run(
        [str(part) for part in command], cwd=BASE, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    if result.returncode:
        print(result.stdout, end="", file=sys.stderr)
        raise SystemExit(result.returncode)
    return result.stdout.strip()


def portable(output):
    """Remove checkout-specific prefixes from recorded verifier output."""
    return output.replace(str(ROOT) + "/", "")


def successes(result_paths):
    chosen = {}
    for result_path in result_paths:
        result_path = result_path.resolve()
        data = json.loads(result_path.read_text(encoding="ascii"))
        assert data["format"] == "j-scan-raw-completion-v1"
        for case in data["cases"]:
            if not case["certified_trivial"]:
                continue
            # Prefer the first successful ordering supplied by the caller.
            chosen.setdefault(case["slug"], (result_path.parent, case))
    return sorted(chosen.items())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "results", nargs="+", type=Path,
        help="raw_completion_results.json files in preferred-order sequence")
    parser.add_argument("--image", default="luttinger-kbmag-proof:4")
    parser.add_argument("--slug", action="append",
                        help="certify only this successful case (repeatable)")
    parser.add_argument("--reuse-history", action="store_true")
    args = parser.parse_args()

    cases = successes(args.results)
    if args.slug:
        requested = set(args.slug)
        cases = [item for item in cases if item[0] in requested]
        missing = requested - {item[0] for item in cases}
        if missing:
            raise SystemExit(f"requested slugs are not successful: {sorted(missing)}")

    rows = []
    for number, (slug, (directory, case)) in enumerate(cases, 1):
        input_rws = directory / f"{slug}_input.rws"
        history = directory / f"{slug}.history"
        certificate = directory / f"{slug}.json.gz"
        presentation = BASE.parent / case["presentation"]
        if not args.reuse_history or not history.exists():
            history_output = run([
                sys.executable, "kbmag_history.py", input_rws, history,
                "--image", args.image,
            ])
        else:
            history_output = f"reused {history}"
        compiler_output = run([
            sys.executable, "compile_kbmag_certificate.py", history,
            certificate, "--input", presentation, "--case", "0",
        ])
        python_output = run([
            sys.executable, "verify_kbmag_certificate.py", certificate,
            "--input", presentation,
        ])
        ruby_output = run([
            "ruby", "verify_certificates.rb", "--input", presentation,
            "--expected-count", "1", certificate,
        ])
        print(f"[{number}/{len(cases)}] {slug}: {python_output}", flush=True)
        rows.append({
            "slug": slug,
            "ordering_directory": str(directory.relative_to(BASE)),
            "presentation": str(presentation.relative_to(BASE)),
            "input_rws": str(input_rws.relative_to(BASE)),
            "history": str(history.relative_to(BASE)),
            "certificate": str(certificate.relative_to(BASE)),
            "history_output": portable(history_output),
            "compiler_output": portable(compiler_output),
            "python_verifier": portable(python_output),
            "ruby_verifier": ruby_output,
        })

    summary = {
        "format": "j-scan-raw-certificates-v1",
        "image": args.image,
        "cases": rows,
    }
    output = BASE / "raw_j_certificate_results.json"
    output.write_text(
        json.dumps(summary, separators=(",", ":"), sort_keys=True) + "\n",
        encoding="ascii")
    print(f"certified and double-verified: {len(rows)}/{len(cases)}")
    print(output)


if __name__ == "__main__":
    main()
