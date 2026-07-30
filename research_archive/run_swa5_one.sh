#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET SEED}"
dataset="${2:?usage: $0 GPU DATASET SEED}"
seed="${3:?usage: $0 GPU DATASET SEED}"
root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"
python_bin="$root/envs/radar310/bin/python"
cfg_dir="$repo/tools/cfgs/astyx_models"
train_log_dir="$root/logs/swa_training"
eval_log_dir="$root/logs/fair_ablation"
mkdir -p "$train_log_dir" "$eval_log_dir"
export PYTHONPATH="$repo${PYTHONPATH:+:$PYTHONPATH}"

case "$dataset" in
    astyx)
        overrides=(--set DATA_CONFIG.DATASET AstyxDataset
            DATA_CONFIG.DATA_PATH "$repo/data/astyx"
            DATA_CONFIG.INFO_PATH.train "['astyx_infos_train.pkl']"
            DATA_CONFIG.INFO_PATH.test "['astyx_infos_val.pkl']")
        ;;
    truckscenes)
        overrides=(--set DATA_CONFIG.DATASET UnifiedRadarDataset
            DATA_CONFIG.DATA_PATH "$root/data/man-truckscenes-mini/unified"
            DATA_CONFIG.INFO_PATH.train "['truckscenes_infos_train.pkl']"
            DATA_CONFIG.INFO_PATH.test "['truckscenes_infos_val.pkl']")
        ;;
    v2xradarv)
        overrides=(--set DATA_CONFIG.DATASET UnifiedRadarDataset
            DATA_CONFIG.DATA_PATH "$root/data/v2x-radar-v-400/unified"
            DATA_CONFIG.INFO_PATH.train "['v2xradarv_infos_train.pkl']"
            DATA_CONFIG.INFO_PATH.test "['v2xradarv_infos_val.pkl']")
        ;;
    kradar)
        overrides=(--set DATA_CONFIG.DATASET UnifiedRadarDataset
            DATA_CONFIG.DATA_PATH "$root/data/kradar-400/unified"
            DATA_CONFIG.INFO_PATH.train "['kradar_infos_train.pkl']"
            DATA_CONFIG.INFO_PATH.test "['kradar_infos_val.pkl']")
        ;;
    *) echo "unsupported dataset: $dataset" >&2; exit 2 ;;
esac

cfg="$cfg_dir/pointpillars_bevgate_${dataset}_car.yaml"
train_tag="swa5_train_${dataset}_seed${seed}"
eval_tag="fair_swa5_${dataset}_seed${seed}"
train_log="$train_log_dir/${train_tag}_gpu${gpu}.log"
eval_log="$eval_log_dir/${eval_tag}_gpu${gpu}.log"

cd "$repo"
env CUDA_VISIBLE_DEVICES="$gpu" "$python_bin" -u tools/train.py \
    --cfg_file "$cfg" --batch_size 4 --epochs 160 --workers 4 \
    --extra_tag "$train_tag" --fix_random_seed --seed "$seed" \
    --ckpt_save_interval 10 --max_ckpt_save_num 5 \
    --set MODEL.BACKBONE_2D.USE_BEV_ATTENTION False \
    "${overrides[@]:1}" >"$train_log" 2>&1

ckpt_dir=$(find "$repo/output" -type d -path "*/${train_tag}/ckpt" -print -quit)
if [[ -z "$ckpt_dir" ]]; then
    echo "checkpoint directory not found for $train_tag" >&2
    exit 3
fi
average_ckpt="$ckpt_dir/checkpoint_swa5.pth"
"$python_bin" "$root/average_last_checkpoints.py" \
    --ckpt-dir "$ckpt_dir" --output "$average_ckpt" --count 5 \
    >>"$train_log" 2>&1

env CUDA_VISIBLE_DEVICES="$gpu" "$python_bin" -u tools/test.py \
    --cfg_file "$cfg" --batch_size 4 --workers 4 \
    --extra_tag "$eval_tag" --ckpt "$average_ckpt" \
    --set MODEL.BACKBONE_2D.USE_BEV_ATTENTION False \
    "${overrides[@]:1}" >"$eval_log" 2>&1
