#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET COUNT}"
dataset="${2:?usage: $0 GPU DATASET COUNT}"
count="${3:?usage: $0 GPU DATASET COUNT}"
root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"
pattern="*pointpillars_bevgate_replay${count}_${dataset}_car/fair_bevgate_replay${count}_${dataset}_seed2028_rcnms/eval/*/result.pkl"
while ! find "$repo/output" -path "$pattern" -print -quit | grep -q .; do
  sleep 20
done
exec "$root/eval_replay_rdar_one.sh" "$gpu" "$dataset" 2028 "$count"
