#!/bin/sh

set -eu
umask 022

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
output=${1:-"$script_dir/arxiv-source-v1.5.5.tar.gz"}
stage=$(mktemp -d "${TMPDIR:-/tmp}/arxiv-source.XXXXXX")

cleanup() {
  rm -f "$stage/main.tex" "$stage/source.tar"
  rmdir "$stage" 2>/dev/null || true
}
trap cleanup EXIT HUP INT TERM

cp "$script_dir/main.tex" "$stage/main.tex"
chmod 0644 "$stage/main.tex"
TZ=UTC touch -t 202608280000 "$stage/main.tex"

COPYFILE_DISABLE=1 tar \
  --format=ustar \
  --uid 0 --gid 0 --uname root --gname root \
  -cf "$stage/source.tar" -C "$stage" main.tex
gzip -n -c "$stage/source.tar" > "$output"

shasum -a 256 "$output"
