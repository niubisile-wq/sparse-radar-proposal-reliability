#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET SEED}"
dataset="${2:?usage: $0 GPU DATASET SEED}"
seed="${3:?usage: $0 GPU DATASET SEED}"

root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"
python_bin="$root/envs/radar310/bin/python"
cfg="$repo/tools/cfgs/astyx_models/pointpillars_taac_${dataset}_car.yaml"
log="$root/logs/fair_ablation/fair_taac_rcnms_${dataset}_seed${seed}_gpu${gpu}.log"

ckpt="$(
    find "$repo/output" \
        -path "*pointpillars_taac_${dataset}_car/fair_taac_${dataset}_seed${seed}/ckpt/checkpoint_epoch_160.pth" \
        -print -quit
)"
if [[ -z "$ckpt" ]]; then
    echo "TAAC checkpoint not found for dataset=$dataset seed=$seed" >&2
    exit 3
fi

cd "$repo"
exec env CUDA_VISIBLE_DEVICES="$gpu" "$python_bin" tools/test.py \
    --cfg_file "$cfg" --batch_size 8 --workers 2 \
    --extra_tag "fair_taac_rcnms_${dataset}_seed${seed}" \
    --ckpt "$ckpt" \
    --set MODEL.POST_PROCESSING.SCORE_THRESH 0.0 \
        MODEL.POST_PROCESSING.NMS_CONFIG.NMS_THRESH 0.50 \
    >"$log" 2>&1
