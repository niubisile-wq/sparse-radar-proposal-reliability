#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET}"
dataset="${2:?usage: $0 GPU DATASET}"
root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"
py="$root/envs/radar310/bin/python"
cfg="$repo/tools/cfgs/astyx_models/pointpillars_taac_${dataset}_car.yaml"
quality_tag="iou0p30_a0p15_p0p25_u0p50"
export PYTHONPATH="$repo${PYTHONPATH:+:$PYTHONPATH}"

case "$dataset" in
  astyx) overrides=(DATA_CONFIG.DATASET AstyxDataset DATA_CONFIG.DATA_PATH "$repo/data/astyx" DATA_CONFIG.INFO_PATH.train "['astyx_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['astyx_infos_val.pkl']");;
  truckscenes) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/man-truckscenes-mini/unified" DATA_CONFIG.INFO_PATH.train "['truckscenes_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['truckscenes_infos_val.pkl']");;
  v2xradarv) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/v2x-radar-v-400/unified" DATA_CONFIG.INFO_PATH.train "['v2xradarv_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['v2xradarv_infos_val.pkl']");;
  kradar) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/kradar-400/unified" DATA_CONFIG.INFO_PATH.train "['kradar_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['kradar_infos_val.pkl']");;
  *) exit 2;;
esac

for seed in 2026 2027 2028; do
  if [[ "$seed" == 2028 ]]; then
    input="$root/results/aeq_stable_bevgate_${quality_tag}_${dataset}_seed${seed}.pkl"
  else
    input="$root/results/qformal_${quality_tag}_${dataset}_seed${seed}.pkl"
  fi
  for vote_iou in 0.22 0.24 0.25 0.26 0.28; do
    for strength in 0.35 0.40 0.45 0.50; do
      tag="m3rob_q15p25_viou${vote_iou/./p}_s${strength/./p}"
      output="$root/results/${tag}_${dataset}_seed${seed}.pkl"
      log="$root/logs/fair_ablation/${tag}_${dataset}_seed${seed}_gpu${gpu}.log"
      env CUDA_VISIBLE_DEVICES="$gpu" "$py" "$root/evaluate_box_voting.py" \
        --cfg_file "$cfg" --input "$input" --output "$output" \
        --vote_iou "$vote_iou" --strength "$strength" --mode xy \
        --residual_count 50 --set "${overrides[@]}" >"$log" 2>&1
    done
  done
done
