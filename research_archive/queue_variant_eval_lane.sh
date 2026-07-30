#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET SEED VARIANT}"
dataset="${2:?usage: $0 GPU DATASET SEED VARIANT}"
seed="${3:?usage: $0 GPU DATASET SEED VARIANT}"
variant="${4:?usage: $0 GPU DATASET SEED VARIANT}"
root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"

while ! find "$repo/output" \
  -path "*pointpillars_${variant}_${dataset}_car/screen_${variant}_${dataset}_seed${seed}/ckpt/checkpoint_epoch_160.pth" \
  -print -quit | grep -q .; do
  sleep 20
done
"$root/eval_qfl_rdar_one.sh" "$gpu" "$dataset" "$seed" "$variant"
