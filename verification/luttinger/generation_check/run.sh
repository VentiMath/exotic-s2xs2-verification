#!/bin/sh
# Replay: export Q and the eight loops from the sealed JSON, then enumerate in GAP.
# GAP is taken from $GAP, else from PATH, else from the repository's Docker wrapper.
set -eu
cd "$(dirname "$0")"
python3 export_generation_input.py
GAPBIN="${GAP:-$(command -v gap || echo ../../bin/gap)}"
"$GAPBIN" -q -A generation_check.g | tee output.txt
sha256sum generation_input.g generation_check.g output.txt > SHA256SUMS 2>/dev/null || shasum -a 256 generation_input.g generation_check.g output.txt > SHA256SUMS
