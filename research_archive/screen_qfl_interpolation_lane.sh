#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET}"
dataset="${2:?usage: $0 GPU DATASET}"
root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"
py="$root/envs/radar310/bin/python"
seed=2028
cfg="$repo/tools/cfgs/astyx_models/pointpillars_qflr_${dataset}_car.yaml"

ckpt_a=$(find "$repo/output" \
  -path "*pointpillars_qflr_${dataset}_car/screen_qflr_${dataset}_seed${seed}/ckpt/checkpoint_epoch_160.pth" \
  -print -quit)
ckpt_b=$(find "$repo/output" \
  -path "*pointpillars_qflr75_${dataset}_car/screen_qflr75_${dataset}_seed${seed}/ckpt/checkpoint_epoch_160.pth" \
  -print -quit)
[[ -n "$ckpt_a" && -n "$ckpt_b" ]] || exit 3

case "$dataset" in
  astyx) overrides=(DATA_CONFIG.DATASET AstyxDataset DATA_CONFIG.DATA_PATH "$repo/data/astyx" DATA_CONFIG.INFO_PATH.train "['astyx_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['astyx_infos_val.pkl']");;
  truckscenes) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/man-truckscenes-mini/unified" DATA_CONFIG.INFO_PATH.train "['truckscenes_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['truckscenes_infos_val.pkl']");;
  v2xradarv) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/v2x-radar-v-400/unified" DATA_CONFIG.INFO_PATH.train "['v2xradarv_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['v2xradarv_infos_val.pkl']");;
  *) exit 2;;
esac

residual=$(find "$repo/output" \
  -path "*pointpillars_taac_${dataset}_car/fair_taac_rcnms_${dataset}_seed${seed}*/eval/*/result.pkl" \
  -print -quit)
[[ -n "$residual" ]] || exit 4

for weight_b in 0.10 0.20 0.30 0.40 0.50 0.60 0.70 0.80 0.90; do
  short="${weight_b/./p}"
  tag="qflinterp_w${short}_${dataset}_seed${seed}"
  ckpt="$root/results/${tag}.pth"
  test_log="$root/logs/fair_ablation/${tag}_gpu${gpu}.log"
  rdar_log="$root/logs/fair_ablation/rdar_${tag}_gpu${gpu}.log"
  output="$root/results/rdar_${tag}.pkl"
  "$py" "$root/interpolate_checkpoints.py" \
    --a "$ckpt_a" --b "$ckpt_b" --weight_b "$weight_b" --output "$ckpt"
  cd "$repo"
  env CUDA_VISIBLE_DEVICES="$gpu" "$py" tools/test.py \
    --cfg_file "$cfg" --batch_size 8 --workers 2 \
    --extra_tag "$tag" --ckpt "$ckpt" \
    --set MODEL.POST_PROCESSING.SCORE_THRESH 0.0 \
      MODEL.POST_PROCESSING.NMS_CONFIG.NMS_THRESH 0.50 \
      "${overrides[@]}" >"$test_log" 2>&1
  primary=$(find "$repo/output" \
    -path "*pointpillars_qflr_${dataset}_car/${tag}/eval/*/result.pkl" \
    -print -quit)
  env PYTHONPATH="$repo" CUDA_VISIBLE_DEVICES="$gpu" "$py" \
    "$root/evaluate_residual_dual_expert.py" \
    --cfg_file "$cfg" --primary "$primary" --residual "$residual" \
    --output "$output" --match_iou 0.10 --residual_topk 50 \
    --set "${overrides[@]}" >"$rdar_log" 2>&1
done
