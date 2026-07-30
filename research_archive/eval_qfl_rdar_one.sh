#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET SEED VARIANT}"
dataset="${2:?usage: $0 GPU DATASET SEED VARIANT}"
seed="${3:?usage: $0 GPU DATASET SEED VARIANT}"
variant="${4:?usage: $0 GPU DATASET SEED VARIANT}"
root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"
py="$root/envs/radar310/bin/python"
cfg="$repo/tools/cfgs/astyx_models/pointpillars_${variant}_${dataset}_car.yaml"
train_tag="screen_${variant}_${dataset}_seed${seed}"
eval_tag="eval_rcnms_${variant}_${dataset}_seed${seed}"
test_log="$root/logs/fair_ablation/${eval_tag}_gpu${gpu}.log"
rdar_log="$root/logs/fair_ablation/eval_rdar_${variant}_${dataset}_seed${seed}_gpu${gpu}.log"
rdar_output="$root/results/rdar_${variant}_${dataset}_seed${seed}.pkl"

ckpt=$(find "$repo/output" \
  -path "*pointpillars_${variant}_${dataset}_car/${train_tag}/ckpt/checkpoint_epoch_160.pth" \
  -print -quit)
[[ -n "$ckpt" ]] || exit 3

case "$dataset" in
  astyx) overrides=(DATA_CONFIG.DATASET AstyxDataset DATA_CONFIG.DATA_PATH "$repo/data/astyx" DATA_CONFIG.INFO_PATH.train "['astyx_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['astyx_infos_val.pkl']");;
  truckscenes) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/man-truckscenes-mini/unified" DATA_CONFIG.INFO_PATH.train "['truckscenes_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['truckscenes_infos_val.pkl']");;
  v2xradarv) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/v2x-radar-v-400/unified" DATA_CONFIG.INFO_PATH.train "['v2xradarv_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['v2xradarv_infos_val.pkl']");;
  kradar) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/kradar-400/unified" DATA_CONFIG.INFO_PATH.train "['kradar_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['kradar_infos_val.pkl']");;
  *) exit 2;;
esac

cd "$repo"
env CUDA_VISIBLE_DEVICES="$gpu" "$py" tools/test.py \
  --cfg_file "$cfg" --batch_size 8 --workers 2 \
  --extra_tag "$eval_tag" --ckpt "$ckpt" \
  --set MODEL.POST_PROCESSING.SCORE_THRESH 0.0 \
    MODEL.POST_PROCESSING.NMS_CONFIG.NMS_THRESH 0.50 \
    "${overrides[@]}" >"$test_log" 2>&1

primary=$(find "$repo/output" \
  -path "*pointpillars_${variant}_${dataset}_car/${eval_tag}/eval/*/result.pkl" \
  -print -quit)
residual=$(find "$repo/output" \
  -path "*pointpillars_taac_${dataset}_car/fair_taac_rcnms_${dataset}_seed${seed}*/eval/*/result.pkl" \
  -print -quit)
[[ -n "$primary" && -n "$residual" ]] || exit 4

env PYTHONPATH="$repo" CUDA_VISIBLE_DEVICES="$gpu" "$py" \
  "$root/evaluate_residual_dual_expert.py" \
  --cfg_file "$cfg" --primary "$primary" --residual "$residual" \
  --output "$rdar_output" --match_iou 0.10 --residual_topk 50 \
  --set "${overrides[@]}" >"$rdar_log" 2>&1
