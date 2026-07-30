#!/usr/bin/env bash
set -euo pipefail

root=/root/autodl-tmp/radar_champion
cd "$root"

nohup env QFL_VARIANT=drav ./run_qfl_one.sh 1 astyx 2028 \
  >logs/fair_ablation/launch_drav_astyx.out 2>&1 &
nohup ./queue_variant_eval_lane.sh 1 astyx 2028 drav \
  >logs/fair_ablation/queue_eval_drav_astyx.out 2>&1 &

nohup env QFL_VARIANT=drav ./run_qfl_one.sh 2 truckscenes 2028 \
  >logs/fair_ablation/launch_drav_truckscenes.out 2>&1 &
nohup ./queue_variant_eval_lane.sh 2 truckscenes 2028 drav \
  >logs/fair_ablation/queue_eval_drav_truckscenes.out 2>&1 &

nohup env QFL_VARIANT=drav ./run_qfl_one.sh 1 v2xradarv 2028 \
  >logs/fair_ablation/launch_drav_v2xradarv.out 2>&1 &
nohup ./queue_variant_eval_lane.sh 1 v2xradarv 2028 drav \
  >logs/fair_ablation/queue_eval_drav_v2xradarv.out 2>&1 &

# Keep exactly one live process on GPU 3 because of its stale CUDA context.
nohup env QFL_VARIANT=drav ./run_qfl_one.sh 3 kradar 2028 \
  >logs/fair_ablation/launch_drav_kradar.out 2>&1 &
nohup ./queue_variant_eval_lane.sh 3 kradar 2028 drav \
  >logs/fair_ablation/queue_eval_drav_kradar.out 2>&1 &

echo "DRAV seed-2028 screening launched."
