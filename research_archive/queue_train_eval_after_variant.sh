#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET SEED DEPENDENCY_VARIANT VARIANT}"
dataset="${2:?usage: $0 GPU DATASET SEED DEPENDENCY_VARIANT VARIANT}"
seed="${3:?usage: $0 GPU DATASET SEED DEPENDENCY_VARIANT VARIANT}"
dependency="${4:?usage: $0 GPU DATASET SEED DEPENDENCY_VARIANT VARIANT}"
variant="${5:?usage: $0 GPU DATASET SEED DEPENDENCY_VARIANT VARIANT}"
root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"

while ! find "$repo/output" \
  -path "*pointpillars_${dependency}_${dataset}_car/screen_${dependency}_${dataset}_seed${seed}/ckpt/checkpoint_epoch_160.pth" \
  -print -quit | grep -q .; do
  sleep 20
done
cd "$root"
env QFL_VARIANT="$variant" ./run_qfl_one.sh "$gpu" "$dataset" "$seed"
./eval_qfl_rdar_one.sh "$gpu" "$dataset" "$seed" "$variant"
