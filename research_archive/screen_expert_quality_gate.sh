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
expert=$(find "$repo/output" -path "*pointpillars_taac_${dataset}_car/fair_taac_rcnms_${dataset}_seed${seed}*/eval/*/result.pkl" -print -quit)
export PYTHONPATH="$repo${PYTHONPATH:+:$PYTHONPATH}"
[[ -n "$expert" ]]

case "$dataset" in
  astyx) overrides=(DATA_CONFIG.DATASET AstyxDataset DATA_CONFIG.DATA_PATH "$repo/data/astyx" DATA_CONFIG.INFO_PATH.train "['astyx_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['astyx_infos_val.pkl']");;
  truckscenes) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/man-truckscenes-mini/unified" DATA_CONFIG.INFO_PATH.train "['truckscenes_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['truckscenes_infos_val.pkl']");;
  v2xradarv) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/v2x-radar-v-400/unified" DATA_CONFIG.INFO_PATH.train "['v2xradarv_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['v2xradarv_infos_val.pkl']");;
  kradar) overrides=(DATA_CONFIG.DATASET UnifiedRadarDataset DATA_CONFIG.DATA_PATH "$root/data/kradar-400/unified" DATA_CONFIG.INFO_PATH.train "['kradar_infos_train.pkl']" DATA_CONFIG.INFO_PATH.test "['kradar_infos_val.pkl']");;
  *) exit 2;;
esac

for iou in 0.10 0.30 0.50; do
  for alpha in 0.15 0.30; do
    for power in 0.00 0.25; do
      for scale in 0.50 0.75 0.90; do
        tag="eqg_iou${iou/./p}_a${alpha/./p}_p${power/./p}_u${scale/./p}"
        log="$root/logs/fair_ablation/${tag}_${dataset}_seed${seed}_gpu${gpu}.log"
        output="$root/results/${tag}_${dataset}_seed${seed}.pkl"
        env CUDA_VISIBLE_DEVICES="$gpu" "$py" "$root/evaluate_expert_quality_gate.py" \
          --cfg_file "$cfg" --rdar "$rdar" --expert "$expert" --output "$output" \
          --match_iou "$iou" --alpha "$alpha" --iou_power "$power" \
          --unmatched_scale "$scale" --residual_count 50 \
          --set "${overrides[@]}" >"$log" 2>&1
      done
    done
  done
done
