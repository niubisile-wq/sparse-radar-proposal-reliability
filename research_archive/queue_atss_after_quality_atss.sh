#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET}"
dataset="${2:?usage: $0 GPU DATASET}"
root=/root/autodl-tmp/radar_champion

while [[ ! -s "$root/results/rdar_qflr55atss_${dataset}_seed2028.pkl" ]]; do
    sleep 15
done

cd "$root"
QFL_VARIANT=atss ./run_qfl_one.sh "$gpu" "$dataset" 2028 &
QFL_VARIANT=atss ./queue_variant_eval_lane.sh \
    "$gpu" "$dataset" 2028 atss &
wait
