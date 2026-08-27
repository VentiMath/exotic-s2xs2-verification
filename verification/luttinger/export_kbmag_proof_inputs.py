#!/usr/bin/env python3
"""Export the eight original four-generator filled presentations as RWS files."""

import argparse
import json
import subprocess
from pathlib import Path

from group_attack import gap_word


def slug(filling):
    return (f'{filling["half_drift"]}_'
            f'{"p" if filling["sign_a"] > 0 else "m"}1_'
            f'{"p" if filling["sign_b"] > 0 else "m"}1')


def gap_list(words):
    return "[" + ",".join(gap_word(word) for word in words) + "]"


def program(data, output_dir):
    lines = ['LoadPackage("kbmag");;']
    for case, filling in enumerate(data["paper_fillings"]):
        # This is the completion-stable order recorded by the original sweep:
        # only case zero is base-first; the other seven are filling-first.
        relators = (data["relators"] + filling["relators"] if case == 0
                    else filling["relators"] + data["relators"])
        lines += [
            f'F := FreeGroup({data["ngens"]});;',
            f'rels := {gap_list(relators)};',
            'G := F/rels;',
            'rws := KBMAGRewritingSystem(G);;',
            f'WriteRWS(rws,"{output_dir}/{slug(filling)}.rws");;',
        ]
    lines.append('QUIT;')
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("r_presentations.json"))
    parser.add_argument("--output-dir", type=Path,
                        default=Path("raw_proof_inputs"))
    parser.add_argument("--gap-file", type=Path,
                        default=Path("r_kbmag_proof_inputs.g"))
    parser.add_argument("--gap", default="../bin/gap")
    parser.add_argument("--no-run", action="store_true")
    args = parser.parse_args()

    data = json.loads(args.input.read_text(encoding="ascii"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.gap_file.write_text(program(data, args.output_dir), encoding="ascii")
    if not args.no_run:
        subprocess.run([args.gap, "-q", args.gap_file], check=True)
    print(args.output_dir, "8 original presentation inputs")


if __name__ == "__main__":
    main()
