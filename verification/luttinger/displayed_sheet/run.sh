#!/bin/bash
# Replays displayed_sheet.g in the GAP container pinned BY DIGEST (not the mutable
# :latest tag that verification/bin/gap uses) and captures output.txt.
# The image is linux/amd64; on arm64 hosts it runs under emulation, so timings in
# the output are orders of magnitude only.  Verdicts do not depend on the platform.
set -euo pipefail
cd "$(dirname "$0")"
IMAGE="gapsystem/gap-docker@sha256:d66dca500c3d8b8ca88824d3c3c7315183335af029f6b74ce592ed0d148edaee"
docker run --rm -i --platform linux/amd64 -v "$PWD":/w -w /w "$IMAGE" gap -q < displayed_sheet.g 2>&1 \
  | grep -v "requested image's platform" | tee output.txt
shasum -a 256 displayed_sheet.g run.sh output.txt > SHA256SUMS
