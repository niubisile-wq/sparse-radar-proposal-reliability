#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET}"
dataset="${2:?usage: $0 GPU DATASET}"
root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"
py="$root/envs/radar310/bin/python"
cfg="$repo/tools/cfgs/astyx_models/pointpillars_stable_bevgate_${dataset}_car.yaml"

case "$dataset" in
  astyx) overrides=(DATA_CONFIG.DATASET AstyxDataset DATA_CONFIG.DATA_PATH "$repo/data/astyx" DATA_CONFIG.INFO_PATH.train "['astyx_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['astyx_infos_val.pkl']");;
  truckscenes) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/man-truckscenes-mini/unified" DATA_CONFIG.INFO_PATH.train "['truckscenes_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['truckscenes_infos_val.pkl']");;
  v2xradarv) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/v2x-radar-v-400/unified" DATA_CONFIG.INFO_PATH.train "['v2xradarv_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['v2xradarv_infos_val.pkl']");;
  kradar) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/kradar-400/unified" DATA_CONFIG.INFO_PATH.train "['kradar_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['kradar_infos_val.pkl']");;
  *) exit 2;;
esac

for seed in 2026 2027; do
  ckpt=$(find "$repo/output" \
    -path "*pointpillars_stable_bevgate_${dataset}_car/fair_stable_bevgate_${dataset}_seed${seed}/ckpt/checkpoint_epoch_160.pth" \
    -print -quit)
  [[ -n "$ckpt" ]] || continue
  tag="expert_rcnms_stable_bevgate_${dataset}_seed${seed}"
  log="$root/logs/fair_ablation/${tag}_gpu${gpu}.log"
  cd "$repo"
  env CUDA_VISIBLE_DEVICES="$gpu" "$py" tools/test.py \
    --cfg_file "$cfg" --batch_size 8 --workers 2 \
    --extra_tag "$tag" --ckpt "$ckpt" \
    --set MODEL.POST_PROCESSING.SCORE_THRESH 0.0 \
      MODEL.POST_PROCESSING.NMS_CONFIG.NMS_THRESH 0.50 \
      "${overrides[@]}" >"$log" 2>&1
done
