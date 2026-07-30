#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET}"
dataset="${2:?usage: $0 GPU DATASET}"
root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"
py="$root/envs/radar310/bin/python"
seed=2028
cfg="$repo/tools/cfgs/astyx_models/pointpillars_taac_${dataset}_car.yaml"
input_tag="${INPUT_TAG:-sqv_xy_iou0p24_s0p40}"
input="$root/results/${input_tag}_${dataset}_seed${seed}.pkl"
export PYTHONPATH="$repo${PYTHONPATH:+:$PYTHONPATH}"

case "$dataset" in
  astyx) overrides=(DATA_CONFIG.DATASET AstyxDataset DATA_CONFIG.DATA_PATH "$repo/data/astyx" DATA_CONFIG.INFO_PATH.train "['astyx_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['astyx_infos_val.pkl']");;
  truckscenes) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/man-truckscenes-mini/unified" DATA_CONFIG.INFO_PATH.train "['truckscenes_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['truckscenes_infos_val.pkl']");;
  v2xradarv) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/v2x-radar-v-400/unified" DATA_CONFIG.INFO_PATH.train "['v2xradarv_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['v2xradarv_infos_val.pkl']");;
  kradar) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/kradar-400/unified" DATA_CONFIG.INFO_PATH.train "['kradar_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['kradar_infos_val.pkl']");;
  *) exit 2;;
esac

powers=(${POWERS:-0.0 1.0 2.0})
scales=(${SCALES:-1.0 2.0 4.0 8.0})
alphas=(${ALPHAS:-0.05 0.10 0.20 0.30})
for power in "${powers[@]}"; do
  for scale in "${scales[@]}"; do
    for alpha in "${alphas[@]}"; do
      tag="rcspt_p${power/./p}_k${scale/./p}_a${alpha/./p}"
      log="$root/logs/fair_ablation/${tag}_${dataset}_seed${seed}_gpu${gpu}.log"
      output="$root/results/${tag}_${dataset}_seed${seed}.pkl"
      env CUDA_VISIBLE_DEVICES="$gpu" "$py" "$root/evaluate_range_compensated_support.py" \
        --cfg_file "$cfg" --input "$input" --output "$output" \
        --range_power "$power" --support_scale "$scale" --alpha "$alpha" \
        --set "${overrides[@]}" >"$log" 2>&1
    done
  done
done
