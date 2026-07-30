#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET SEED...}"
dataset="${2:?usage: $0 GPU DATASET SEED...}"
shift 2
root=/root/autodl-tmp/radar_champion
status="$root/logs/fair_ablation/rdar_${dataset}_queue.status"
: >"$status"

cd "$root"
for seed in "$@"; do
    echo "$(date -Iseconds) START dataset=$dataset seed=$seed gpu=$gpu" >>"$status"
    ./eval_rdar_one.sh "$gpu" "$dataset" "$seed"
    rc=$?
    echo "$(date -Iseconds) END dataset=$dataset seed=$seed gpu=$gpu rc=$rc" >>"$status"
done
