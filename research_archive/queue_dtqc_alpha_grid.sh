#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET SEED}"
dataset="${2:?usage: $0 GPU DATASET SEED}"
seed="${3:?usage: $0 GPU DATASET SEED}"
root=/root/autodl-tmp/radar_champion

while [[ ! -s "$root/results/rdar_dtqc_${dataset}_seed${seed}.pkl" ]]; do
    sleep 15
done

cd "$root"
for spec in "0.25 25" "0.35 35" "0.65 65" "0.75 75"; do
    read -r alpha tag <<<"$spec"
    ./eval_dtqc_alpha_one.sh "$gpu" "$dataset" "$seed" "$alpha" "$tag"
done
