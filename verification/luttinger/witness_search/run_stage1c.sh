#!/bin/bash
# run_stage1c.sh <case indices...> — Size() ladder per case, 2 at a time, 1800 CPU-seconds each.
cd "$(dirname "$0")"; mkdir -p logs
GAP="${GAP:-$HOME/opt/gap-4.16.1/gap}"
printf '%s\n' "$@" | xargs -P 2 -I{} bash -c 'ulimit -t 1800; WS_CASE={} "'"$GAP"'" -q -A stage1c_size.g > logs/stage1c_case{}.log 2>&1 || echo "case {}: killed or failed" >> logs/stage1c_case{}.log'
echo "stage 1c driver finished"
