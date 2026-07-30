#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET SEED COUNT}"
dataset="${2:?usage: $0 GPU DATASET SEED COUNT}"
seed="${3:?usage: $0 GPU DATASET SEED COUNT}"
count="${4:?usage: $0 GPU DATASET SEED COUNT}"
root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"
py="$root/envs/radar310/bin/python"
cfg="$repo/tools/cfgs/astyx_models/pointpillars_bevgate_replay${count}_${dataset}_car.yaml"
log="$root/logs/fair_ablation/rdar_replay${count}_${dataset}_seed${seed}_gpu${gpu}.log"
output="$root/results/rdar_replay${count}_${dataset}_seed${seed}.pkl"
primary=$(find "$repo/output" \
  -path "*pointpillars_bevgate_replay${count}_${dataset}_car/fair_bevgate_replay${count}_${dataset}_seed${seed}_rcnms/eval/*/result.pkl" \
  -print -quit)
residual=$(find "$repo/output" \
  -path "*pointpillars_taac_${dataset}_car/fair_taac_rcnms_${dataset}_seed${seed}*/eval/*/result.pkl" \
  -print -quit)
[[ -n "$primary" && -n "$residual" ]]

cd "$repo"
exec env PYTHONPATH="$repo" CUDA_VISIBLE_DEVICES="$gpu" "$py" \
  "$root/evaluate_residual_dual_expert.py" \
  --cfg_file "$cfg" --primary "$primary" --residual "$residual" \
  --output "$output" --match_iou 0.10 --residual_topk 50 \
  >"$log" 2>&1
