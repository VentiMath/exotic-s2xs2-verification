#!/usr/bin/env python3
"""Run KBMAG with equation ancestry enabled and retain its stdout.

The ordinary GAP wrapper deliberately discards this stream.  ``kbprog -ve``
numbers every derived equation and names the two parent equations whose
overlap produced it; that is the raw material for an independently replayed
normal-closure certificate.
"""

import argparse
import subprocess
from pathlib import Path


IMAGE = "luttinger-kbmag-proof:local"
KBPROG = ("/home/gap/inst/gap-4.11.1/pkg/kbmag-1.5.9/bin/"
          "x86_64-pc-linux-gnu-default64-kv7/kbprog")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--image", default=IMAGE)
    parser.add_argument("--kbprog-args", default="",
                        help="extra kbprog options, e.g. '-me 300000 -t 100' "
                             "(see sealed_transport/kbprog_options.json)")
    args = parser.parse_args()

    root = Path.cwd().resolve()
    source = args.input.resolve()
    output = args.output.resolve()
    try:
        relative = source.relative_to(root)
        output.relative_to(root)
    except ValueError as error:
        raise SystemExit("input and output must be inside the repository") from error
    output.parent.mkdir(parents=True, exist_ok=True)

    command = [
        "docker", "run", "--rm", "-i",
        "-v", f"{root}:/w", "-w", "/w", args.image,
        KBPROG, "-ve", *args.kbprog_args.split(), str(Path("/w") / relative),
    ]
    with output.open("wb") as stream:
        result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT)
    if result.returncode:
        raise SystemExit(result.returncode)
    print(output)


if __name__ == "__main__":
    main()
