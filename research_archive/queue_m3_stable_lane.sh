#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET}"
dataset="${2:?usage: $0 GPU DATASET}"
root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"
for seed in 2026 2027; do
  pattern="*pointpillars_stable_bevgate_${dataset}_car/expert_rcnms_stable_bevgate_${dataset}_seed${seed}/eval/*/result.pkl"
  while ! find "$repo/output" -path "$pattern" -print -quit | grep -q .; do
    sleep 20
  done
  "$root/run_m3_stable_one.sh" "$gpu" "$dataset" "$seed"
done
