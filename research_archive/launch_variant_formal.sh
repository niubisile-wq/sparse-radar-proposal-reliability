#!/usr/bin/env bash
set -euo pipefail

variant="${1:?usage: $0 VARIANT}"
root=/root/autodl-tmp/radar_champion
cd "$root"

launch_one() {
  local gpu="$1"
  local dataset="$2"
  local seed="$3"
  nohup env QFL_VARIANT="$variant" ./run_qfl_one.sh \
    "$gpu" "$dataset" "$seed" \
    >"logs/fair_ablation/launch_${variant}_${dataset}_seed${seed}.out" 2>&1 &
  nohup ./queue_variant_eval_lane.sh "$gpu" "$dataset" "$seed" "$variant" \
    >"logs/fair_ablation/queue_eval_${variant}_${dataset}_seed${seed}.out" 2>&1 &
}

# The 24 GB cards safely host two ~1.4 GB PointPillars jobs. GPU 3 is kept
# single-job because a stale, unrecoverable CUDA context occupies ~4.7 GB.
launch_one 0 astyx 2026
launch_one 0 astyx 2027
launch_one 1 v2xradarv 2026
launch_one 1 v2xradarv 2027
launch_one 2 truckscenes 2026
launch_one 2 truckscenes 2027

nohup bash -c "
  set -euo pipefail
  cd '$root'
  QFL_VARIANT='$variant' ./run_qfl_one.sh 3 kradar 2026
  ./eval_qfl_rdar_one.sh 3 kradar 2026 '$variant'
  QFL_VARIANT='$variant' ./run_qfl_one.sh 3 kradar 2027
  ./eval_qfl_rdar_one.sh 3 kradar 2027 '$variant'
" >"logs/fair_ablation/formal_${variant}_kradar_queue.out" 2>&1 &

echo "$variant formal seeds 2026/2027 launched."
