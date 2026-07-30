#!/usr/bin/env bash
set -u
BASE=/root/autodl-tmp/radar_champion
IMG=/root/autodl-tmp/稀疏雷达提案可靠性四模块论文实验全量冻结映像_20260727_000030
PY=$BASE/envs/radar310/bin/python
CFG=$BASE/repos/OpenPCDet_current/tools/cfgs/astyx_models/pointpillars_stable_bevgate_kradar_car.yaml
EXPERT=$BASE/repos/OpenPCDet_current/output/root/autodl-tmp/radar_champion/repos/OpenPCDet_current/tools/cfgs/astyx_models/pointpillars_stable_bevgate_kradar_car/review_expert_seed2028/eval/epoch_160/val/default/result.pkl
OUT=$BASE/results/review_upgrade_20260730/strict_fixed_expert_factorial_12cell
mkdir -p "$OUT/gate_logs" "$OUT/gate_pkl" "$OUT/vote_logs" "$OUT/vote_pkl"
cd "$BASE/repos/OpenPCDet_current"
for seed in 2026 2027 2028; do
  CUDA_VISIBLE_DEVICES=$((seed % 2)) "$PY" "$IMG/evaluate_expert_quality_gate.py" \
    --cfg_file "$CFG" --rdar "$BASE/results/rdar_kradar_seed${seed}.pkl" \
    --expert "$EXPERT" --output "$OUT/gate_pkl/kradar_seed${seed}.pkl" \
    --match_iou 0.30 --alpha 0.30 --iou_power 0.25 --unmatched_scale 0.50 \
    --residual_count 50 --workers 1 >"$OUT/gate_logs/kradar_seed${seed}.log" 2>&1
done
for seed in 2026 2027 2028; do
  CUDA_VISIBLE_DEVICES=$((seed % 2)) "$PY" "$IMG/evaluate_box_voting.py" \
    --cfg_file "$CFG" --input "$OUT/gate_pkl/kradar_seed${seed}.pkl" \
    --output "$OUT/vote_pkl/kradar_seed${seed}.pkl" --vote_iou 0.24 \
    --strength 0.40 --mode xy --only_lower_score_neighbors --residual_count 50 \
    --workers 1 >"$OUT/vote_logs/kradar_seed${seed}.log" 2>&1
done
echo "K-Radar fixed expert factorial complete"
