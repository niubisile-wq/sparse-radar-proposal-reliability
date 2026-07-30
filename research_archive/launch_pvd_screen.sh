#!/usr/bin/env bash
set -euo pipefail

root=/root/autodl-tmp/radar_champion
cd "$root"

# GPU 3 retains a stale, non-computing CUDA context, so keep exactly one live
# training job there. GPU 1 safely hosts the two smaller Astyx/V2X screens.
nohup env QFL_VARIANT=pvd ./run_qfl_one.sh 1 astyx 2028 \
  >logs/fair_ablation/launch_pvd_astyx.out 2>&1 &
nohup ./queue_variant_eval_lane.sh 1 astyx 2028 pvd \
  >logs/fair_ablation/queue_eval_pvd_astyx.out 2>&1 &

nohup env QFL_VARIANT=pvd ./run_qfl_one.sh 2 truckscenes 2028 \
  >logs/fair_ablation/launch_pvd_truckscenes.out 2>&1 &
nohup ./queue_variant_eval_lane.sh 2 truckscenes 2028 pvd \
  >logs/fair_ablation/queue_eval_pvd_truckscenes.out 2>&1 &

nohup env QFL_VARIANT=pvd ./run_qfl_one.sh 1 v2xradarv 2028 \
  >logs/fair_ablation/launch_pvd_v2xradarv.out 2>&1 &
nohup ./queue_variant_eval_lane.sh 1 v2xradarv 2028 pvd \
  >logs/fair_ablation/queue_eval_pvd_v2xradarv.out 2>&1 &

nohup env QFL_VARIANT=pvd ./run_qfl_one.sh 3 kradar 2028 \
  >logs/fair_ablation/launch_pvd_kradar.out 2>&1 &
nohup ./queue_variant_eval_lane.sh 3 kradar 2028 pvd \
  >logs/fair_ablation/queue_eval_pvd_kradar.out 2>&1 &

echo "PVD seed-2028 screening launched."
