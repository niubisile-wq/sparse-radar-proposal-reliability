#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET SEED}"
dataset="${2:?usage: $0 GPU DATASET SEED}"
seed="${3:?usage: $0 GPU DATASET SEED}"

root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"
python_bin="$root/envs/radar310/bin/python"
cfg="$repo/tools/cfgs/astyx_models/pointpillars_iouaware_${dataset}_car.yaml"
tag="fair_iouaware_${dataset}_seed${seed}"
log="$root/logs/fair_ablation/${tag}_gpu${gpu}.log"
mkdir -p "$root/logs/fair_ablation"
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

cd "$repo"
exec env CUDA_VISIBLE_DEVICES="$gpu" "$python_bin" -u tools/train.py \
    --cfg_file "$cfg" --batch_size 4 --epochs 160 --workers 4 \
    --extra_tag "$tag" --fix_random_seed --seed "$seed" \
    --ckpt_save_interval 160 --max_ckpt_save_num 1 \
    "${overrides[@]}" >"$log" 2>&1
