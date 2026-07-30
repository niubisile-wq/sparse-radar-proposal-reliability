#!/usr/bin/env bash
set -euo pipefail
gpu="${1:?gpu}"
datasets="${2:?dataset list, comma separated}"
export CUDA_VISIBLE_DEVICES="$gpu"
base=/root/autodl-tmp/radar_champion
repo="$base/repos/OpenPCDet_current"
py="$base/envs/radar310/bin/python"
outbase="$base/results/review_upgrade_20260730/vote_only_12cell"
IFS=',' read -ra items <<< "$datasets"
for item in "${items[@]}"; do
  dataset="${item%%:*}"
  seed="${item##*:}"
  cfg="$repo/tools/cfgs/astyx_models/pointpillars_taac_${dataset}_car.yaml"
  input="$base/results/rdar_${dataset}_seed${seed}.pkl"
  output="$outbase/${dataset}_seed${seed}.pkl"
  log="$outbase/${dataset}_seed${seed}.log"
  mkdir -p "$outbase"
  case "$dataset" in
    astyx) overrides=(DATA_CONFIG.DATASET AstyxDataset DATA_CONFIG.DATA_PATH "$repo/data/astyx" DATA_CONFIG.INFO_PATH.train "['astyx_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['astyx_infos_val.pkl']");;
    truckscenes) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$base/data/man-truckscenes-mini/unified" DATA_CONFIG.INFO_PATH.train "['truckscenes_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['truckscenes_infos_val.pkl']");;
    v2xradarv) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$base/data/v2x-radar-v-400/unified" DATA_CONFIG.INFO_PATH.train "['v2xradarv_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['v2xradarv_infos_val.pkl']");;
    kradar) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$base/data/kradar-400/unified" DATA_CONFIG.INFO_PATH.train "['kradar_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['kradar_infos_val.pkl']");;
  esac
  "$py" "$base/evaluate_box_voting.py" --cfg_file "$cfg" --input "$input" --output "$output" --vote_iou 0.24 --strength 0.40 --mode xy --residual_count 50 --workers 0 --set "${overrides[@]}" >"$log" 2>&1
done
