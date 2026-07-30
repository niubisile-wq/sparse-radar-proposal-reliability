#!/usr/bin/env bash
set -u
BASE=/root/autodl-tmp/radar_champion
IMG=/root/autodl-tmp/稀疏雷达提案可靠性四模块论文实验全量冻结映像_20260727_000030
PY=$BASE/envs/radar310/bin/python
GATE=$IMG/evaluate_expert_quality_gate.py
VOTE=$IMG/evaluate_box_voting.py
CFGROOT=$BASE/repos/OpenPCDet_current/tools/cfgs/astyx_models
OUT=$BASE/results/review_upgrade_20260730/strict_fixed_expert_factorial_12cell
mkdir -p "$OUT/gate_logs" "$OUT/gate_pkl" "$OUT/vote_logs" "$OUT/vote_pkl"
cd "$BASE/repos/OpenPCDet_current"

expert_path() {
  local dataset="$1"
  local seed=2027
  if [[ "$dataset" == "kradar" ]]; then seed=2028; fi
  echo "$BASE/repos/OpenPCDet_current/output/root/autodl-tmp/radar_champion/repos/OpenPCDet_current/tools/cfgs/astyx_models/pointpillars_stable_bevgate_dapg_msbc_${dataset}_car/review_expert_seed${seed}/eval/epoch_160/val/default/result.pkl"
}

run_gate() {
  local gpu="$1" dataset="$2" seed="$3"
  local cfg="$CFGROOT/pointpillars_stable_bevgate_dapg_msbc_${dataset}_car.yaml"
  local rdar="$BASE/results/rdar_${dataset}_seed${seed}.pkl"
  local expert="$(expert_path "$dataset")"
  CUDA_VISIBLE_DEVICES="$gpu" "$PY" "$GATE" \
    --cfg_file "$cfg" --rdar "$rdar" --expert "$expert" \
    --output "$OUT/gate_pkl/${dataset}_seed${seed}.pkl" \
    --match_iou 0.30 --alpha 0.30 --iou_power 0.25 \
    --unmatched_scale 0.50 --residual_count 50 --workers 1 \
    >"$OUT/gate_logs/${dataset}_seed${seed}.log" 2>&1
}

jobs=()
for dataset in astyx truckscenes v2xradarv kradar; do
  for seed in 2026 2027 2028; do
    run_gate $(( ${#jobs[@]} % 2 )) "$dataset" "$seed" &
    jobs+=("$!")
    if (( ${#jobs[@]} % 2 == 0 )); then wait "${jobs[-2]}" "${jobs[-1]}"; fi
  done
done
wait

jobs=()
for dataset in astyx truckscenes v2xradarv kradar; do
  for seed in 2026 2027 2028; do
    gpu=$(( ${#jobs[@]} % 2 ))
    cfg="$CFGROOT/pointpillars_stable_bevgate_dapg_msbc_${dataset}_car.yaml"
    CUDA_VISIBLE_DEVICES="$gpu" "$PY" "$VOTE" \
      --cfg_file "$cfg" --input "$OUT/gate_pkl/${dataset}_seed${seed}.pkl" \
      --output "$OUT/vote_pkl/${dataset}_seed${seed}.pkl" \
      --vote_iou 0.24 --strength 0.40 --mode xy \
      --only_lower_score_neighbors --residual_count 50 --workers 1 \
      >"$OUT/vote_logs/${dataset}_seed${seed}.log" 2>&1 &
    jobs+=("$!")
    if (( ${#jobs[@]} % 2 == 0 )); then wait "${jobs[-2]}" "${jobs[-1]}"; fi
  done
done
wait
echo "strict fixed-expert factorial complete"
