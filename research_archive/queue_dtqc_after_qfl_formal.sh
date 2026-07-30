#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET}"
dataset="${2:?usage: $0 GPU DATASET}"
root=/root/autodl-tmp/radar_champion

for seed in 2026 2027; do
    result="$root/results/rdar_qflr_${dataset}_seed${seed}.pkl"
    while [[ ! -s "$result" ]]; do
        sleep 15
    done
done

cd "$root"
QFL_VARIANT=dtqc ./run_qfl_one.sh "$gpu" "$dataset" 2028 &
QFL_VARIANT=dtqc ./queue_variant_eval_lane.sh \
    "$gpu" "$dataset" 2028 dtqc &
wait
