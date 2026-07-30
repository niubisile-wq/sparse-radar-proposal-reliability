#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET SEED VOTE_IOU STRENGTH TAG}"
dataset="${2:?usage: $0 GPU DATASET SEED VOTE_IOU STRENGTH TAG}"
seed="${3:?usage: $0 GPU DATASET SEED VOTE_IOU STRENGTH TAG}"
vote_iou="${4:?usage: $0 GPU DATASET SEED VOTE_IOU STRENGTH TAG}"
strength="${5:?usage: $0 GPU DATASET SEED VOTE_IOU STRENGTH TAG}"
tag="${6:?usage: $0 GPU DATASET SEED VOTE_IOU STRENGTH TAG}"
root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"
py="$root/envs/radar310/bin/python"
cfg="$repo/tools/cfgs/astyx_models/pointpillars_taac_${dataset}_car.yaml"
stage="$root/results/m3_stable_stage_${dataset}_seed${seed}.pkl"
output="$root/results/${tag}_${dataset}_seed${seed}.pkl"
log="$root/logs/fair_ablation/${tag}_${dataset}_seed${seed}_gpu${gpu}.log"
export PYTHONPATH="$repo${PYTHONPATH:+:$PYTHONPATH}"

case "$dataset" in
  astyx) overrides=(DATA_CONFIG.DATASET AstyxDataset DATA_CONFIG.DATA_PATH "$repo/data/astyx" DATA_CONFIG.INFO_PATH.train "['astyx_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['astyx_infos_val.pkl']");;
  truckscenes) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/man-truckscenes-mini/unified" DATA_CONFIG.INFO_PATH.train "['truckscenes_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['truckscenes_infos_val.pkl']");;
  v2xradarv) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/v2x-radar-v-400/unified" DATA_CONFIG.INFO_PATH.train "['v2xradarv_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['v2xradarv_infos_val.pkl']");;
  kradar) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/kradar-400/unified" DATA_CONFIG.INFO_PATH.train "['kradar_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['kradar_infos_val.pkl']");;
  *) exit 2;;
esac

env CUDA_VISIBLE_DEVICES="$gpu" "$py" "$root/evaluate_box_voting.py" \
  --cfg_file "$cfg" --input "$stage" --output "$output" \
  --vote_iou "$vote_iou" --strength "$strength" --mode xy --residual_count 50 \
  --set "${overrides[@]}" >"$log" 2>&1
