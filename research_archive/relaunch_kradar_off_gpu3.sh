#!/usr/bin/env bash
set -euo pipefail
root=/root/autodl-tmp/radar_champion
cd "$root"

# Remove only the obsolete waiters tied to the failed GPU-3 runs.
pkill -TERM -f '[q]ueue_variant_eval_lane.sh 3 kradar 2028 drav' || true
pkill -TERM -f '[q]ueue_variant_eval_lane.sh 3 kradar 2028 pvd_rgpc' || true

nohup env QFL_VARIANT=drav ./run_qfl_one.sh 0 kradar 2028 \
  >logs/fair_ablation/relaunch_drav_kradar_gpu0.out 2>&1 &
nohup ./queue_variant_eval_lane.sh 0 kradar 2028 drav \
  >logs/fair_ablation/relaunch_eval_drav_kradar_gpu0.out 2>&1 &

nohup env QFL_VARIANT=pvd_rgpc ./run_qfl_one.sh 1 kradar 2028 \
  >logs/fair_ablation/relaunch_pvd_rgpc_kradar_gpu1.out 2>&1 &
nohup ./queue_variant_eval_lane.sh 1 kradar 2028 pvd_rgpc \
  >logs/fair_ablation/relaunch_eval_pvd_rgpc_kradar_gpu1.out 2>&1 &

echo "K-Radar DRAV/PVD+RGPC moved off GPU 3."
