#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET}"
dataset="${2:?usage: $0 GPU DATASET}"
root=/root/autodl-tmp/radar_champion
status="$root/logs/fair_ablation/taac_rcnms_${dataset}_queue.status"
: >"$status"

cd "$root"
for seed in 2026 2027 2028; do
    echo "$(date -Iseconds) START dataset=$dataset seed=$seed gpu=$gpu" >>"$status"
    ./eval_taac_rcnms_one.sh "$gpu" "$dataset" "$seed"
    rc=$?
    echo "$(date -Iseconds) END dataset=$dataset seed=$seed gpu=$gpu rc=$rc" >>"$status"
done
