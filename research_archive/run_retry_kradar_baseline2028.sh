#!/usr/bin/env bash
set -euo pipefail

root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"
python_bin="$root/envs/radar310/bin/python"
cfg="$repo/tools/cfgs/astyx_models/pointpillars_bevgate_kradar_car.yaml"
tag=fair_pointpillars_kradar_seed2028
log="$root/logs/fair_ablation/${tag}_gpu3.log"
export PYTHONPATH="$repo${PYTHONPATH:+:$PYTHONPATH}"

cd "$repo"
exec env CUDA_VISIBLE_DEVICES=3 "$python_bin" -u tools/train.py \
    --cfg_file "$cfg" --batch_size 4 --epochs 160 --workers 4 \
    --extra_tag "$tag" --fix_random_seed --seed 2028 \
    --ckpt_save_interval 160 --max_ckpt_save_num 1 \
    --set MODEL.BACKBONE_2D.USE_BEV_ATTENTION False \
    DATA_CONFIG.DATASET UnifiedRadarDataset \
    DATA_CONFIG.DATA_PATH "$root/data/kradar-400/unified" \
    DATA_CONFIG.INFO_PATH.train "['kradar_infos_train.pkl']" \
    DATA_CONFIG.INFO_PATH.test "['kradar_infos_val.pkl']" \
    >"$log" 2>&1
