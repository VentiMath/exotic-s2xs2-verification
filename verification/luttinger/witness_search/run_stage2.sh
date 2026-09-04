#!/bin/bash
# run_stage2.sh <case indices...>  — runs every (case, target) job for the given cases,
# PARALLEL jobs at a time (default 8), one log per job under logs/.  Idempotent: a job
# whose log already ends in "JOB DONE" is skipped, so the driver can be re-run.
set -uo pipefail
cd "$(dirname "$0")"
GAP="${GAP:-$HOME/opt/gap-4.16.1/gap}"
PARALLEL="${PARALLEL:-8}"
mkdir -p logs
TARGETS=(LI7 A5 L2_7 A6 L2_8 L2_11 L2_13 L2_17 A7 L2_19 L2_16 L3_3 U3_3 L2_23 L2_25 M11 L2_27 L2_29 L2_31 A8 L3_4 L2_37 U4_2 Sz_8 L2_32 L2_41 L2_43 L2_47 L2_49 U3_4 L2_53 M12)
jobs_file=$(mktemp)
for c in "$@"; do for t in "${TARGETS[@]}"; do
  log="logs/case${c}_${t}.log"
  if [ -f "$log" ] && grep -q "JOB DONE" "$log"; then continue; fi
  echo "$c $t" >> "$jobs_file"
done; done
echo "$(wc -l < "$jobs_file" | tr -d ' ') jobs to run, $PARALLEL at a time"
xargs -P "$PARALLEL" -L 1 bash -c 'c=$0; t=$1; WS_CASE=$c WS_TARGET=$t "'"$GAP"'" -q -A stage2_worker.g > "logs/case${c}_${t}.log" 2>&1' < "$jobs_file"
rm -f "$jobs_file"
echo "stage 2 driver finished"
