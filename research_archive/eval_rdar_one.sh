#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET SEED}"
dataset="${2:?usage: $0 GPU DATASET SEED}"
seed="${3:?usage: $0 GPU DATASET SEED}"

root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"
python_bin="$root/envs/radar310/bin/python"
cfg="$repo/tools/cfgs/astyx_models/pointpillars_taac_${dataset}_car.yaml"
log="$root/logs/fair_ablation/fair_rdar_${dataset}_seed${seed}_gpu${gpu}.log"
output="$root/results/rdar_${dataset}_seed${seed}.pkl"

primary="$(
    find "$repo/output" \
        -path "*pointpillars_bevgate_${dataset}_car/fair_rcnms_${dataset}_seed${seed}/eval/*/result.pkl" \
        -print -quit
)"
residual="$(
    find "$repo/output" \
        -path "*pointpillars_taac_${dataset}_car/fair_taac_rcnms_${dataset}_seed${seed}*/eval/*/result.pkl" \
        -print -quit
)"
if [[ -z "$primary" || -z "$residual" ]]; then
    echo "Expert result missing for dataset=$dataset seed=$seed" >&2
    exit 3
fi

cd "$repo"
exec env PYTHONPATH="$repo" CUDA_VISIBLE_DEVICES="$gpu" "$python_bin" \
    "$root/evaluate_residual_dual_expert.py" \
    --cfg_file "$cfg" \
    --primary "$primary" \
    --residual "$residual" \
    --output "$output" \
    --match_iou 0.10 \
    --residual_topk 50 \
    >"$log" 2>&1
