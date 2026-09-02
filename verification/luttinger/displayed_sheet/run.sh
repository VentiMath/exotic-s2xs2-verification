#!/bin/bash
# Replays displayed_sheet.g in the pinned GAP container and captures output.txt.
set -euo pipefail
cd "$(dirname "$0")"
../../bin/gap -q < displayed_sheet.g 2>&1 | grep -v "requested image's platform" | tee output.txt
shasum -a 256 displayed_sheet.g run.sh output.txt > SHA256SUMS
