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
export PYTHONPATH="$repo${PYTHONPATH:+:$PYTHONPATH}"

case "$dataset" in
    astyx)
        overrides=(DATA_CONFIG.DATASET AstyxDataset
            DATA_CONFIG.DATA_PATH "$repo/data/astyx"
            DATA_CONFIG.INFO_PATH.train "['astyx_infos_train.pkl']"
            DATA_CONFIG.INFO_PATH.test "['astyx_infos_val.pkl']")
        ;;
    truckscenes)
        overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset
            DATA_CONFIG.DATA_PATH "$root/data/man-truckscenes-mini/unified"
            DATA_CONFIG.INFO_PATH.train "['truckscenes_infos_train.pkl']"
            DATA_CONFIG.INFO_PATH.test "['truckscenes_infos_val.pkl']")
        ;;
    v2xradarv)
        overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset
            DATA_CONFIG.DATA_PATH "$root/data/v2x-radar-v-400/unified"
            DATA_CONFIG.INFO_PATH.train "['v2xradarv_infos_train.pkl']"
            DATA_CONFIG.INFO_PATH.test "['v2xradarv_infos_val.pkl']")
        ;;
    kradar)
        overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset
            DATA_CONFIG.DATA_PATH "$root/data/kradar-400/unified"
            DATA_CONFIG.INFO_PATH.train "['kradar_infos_train.pkl']"
            DATA_CONFIG.INFO_PATH.test "['kradar_infos_val.pkl']")
        ;;
    *) echo "unsupported dataset: $dataset" >&2; exit 2 ;;
esac

ckpt=""
while [[ -z "$ckpt" ]]; do
    ckpt="$(find "$repo/output" \
        -path "*pointpillars_iouaware_${dataset}_car/$tag/ckpt/checkpoint_epoch_160.pth" \
        -print -quit)"
    [[ -n "$ckpt" ]] || sleep 5
done
cd "$repo"
for alpha in 0.0 0.1 0.2 0.3 0.4 0.6 0.7; do
    alpha_tag="alpha_${alpha/./p}"
    log="$root/logs/fair_ablation/eval_${tag}_${alpha_tag}_gpu${gpu}.log"
    env CUDA_VISIBLE_DEVICES="$gpu" "$python_bin" -u tools/test.py \
        --cfg_file "$cfg" --batch_size 4 --workers 4 \
        --extra_tag "$tag" --ckpt "$ckpt" --eval_tag "$alpha_tag" \
        --set MODEL.DENSE_HEAD.IOU_FUSION_ALPHA "$alpha" "${overrides[@]}" \
        >"$log" 2>&1
done
