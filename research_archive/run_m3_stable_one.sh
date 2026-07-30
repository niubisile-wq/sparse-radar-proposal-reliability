#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET SEED}"
dataset="${2:?usage: $0 GPU DATASET SEED}"
seed="${3:?usage: $0 GPU DATASET SEED}"
root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"
py="$root/envs/radar310/bin/python"
cfg="$repo/tools/cfgs/astyx_models/pointpillars_taac_${dataset}_car.yaml"
rdar="$root/results/rdar_${dataset}_seed${seed}.pkl"
expert=$(find "$repo/output" \
  -path "*pointpillars_stable_bevgate_${dataset}_car/expert_rcnms_stable_bevgate_${dataset}_seed${seed}/eval/*/result.pkl" \
  -print -quit)
stage="$root/results/m3_stable_stage_${dataset}_seed${seed}.pkl"
output="$root/results/m3_stable_${dataset}_seed${seed}.pkl"
stage_log="$root/logs/fair_ablation/m3_stable_stage_${dataset}_seed${seed}_gpu${gpu}.log"
final_log="$root/logs/fair_ablation/m3_stable_${dataset}_seed${seed}_gpu${gpu}.log"
export PYTHONPATH="$repo${PYTHONPATH:+:$PYTHONPATH}"

case "$dataset" in
  astyx) overrides=(DATA_CONFIG.DATASET AstyxDataset DATA_CONFIG.DATA_PATH "$repo/data/astyx" DATA_CONFIG.INFO_PATH.train "['astyx_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['astyx_infos_val.pkl']");;
  truckscenes) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/man-truckscenes-mini/unified" DATA_CONFIG.INFO_PATH.train "['truckscenes_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['truckscenes_infos_val.pkl']");;
  v2xradarv) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/v2x-radar-v-400/unified" DATA_CONFIG.INFO_PATH.train "['v2xradarv_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['v2xradarv_infos_val.pkl']");;
  kradar) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/kradar-400/unified" DATA_CONFIG.INFO_PATH.train "['kradar_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['kradar_infos_val.pkl']");;
  *) exit 2;;
esac

env CUDA_VISIBLE_DEVICES="$gpu" "$py" "$root/evaluate_expert_quality_gate.py" \
  --cfg_file "$cfg" --rdar "$rdar" --expert "$expert" --output "$stage" \
  --match_iou 0.30 --alpha 0.30 --iou_power 0.25 \
  --unmatched_scale 0.50 --residual_count 50 \
  --set "${overrides[@]}" >"$stage_log" 2>&1

env CUDA_VISIBLE_DEVICES="$gpu" "$py" "$root/evaluate_box_voting.py" \
  --cfg_file "$cfg" --input "$stage" --output "$output" \
  --vote_iou 0.24 --strength 0.40 --mode xy --residual_count 50 \
  --set "${overrides[@]}" >"$final_log" 2>&1
