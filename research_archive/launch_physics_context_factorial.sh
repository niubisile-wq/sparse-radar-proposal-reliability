#!/usr/bin/env bash
set -euo pipefail

root=/root/autodl-tmp/radar_champion
cd "$root"

launch_one() {
  local gpu="$1"
  local dataset="$2"
  local variant="$3"
  local seed=2028
  nohup env QFL_VARIANT="$variant" ./run_qfl_one.sh \
    "$gpu" "$dataset" "$seed" \
    >"logs/fair_ablation/relaunch_${variant}_${dataset}_seed${seed}.out" 2>&1 &
  nohup ./queue_variant_eval_lane.sh \
    "$gpu" "$dataset" "$seed" "$variant" \
    >"logs/fair_ablation/relaunch_eval_${variant}_${dataset}_seed${seed}.out" 2>&1 &
}

# Three compact PointPillars jobs use ~4-5 GB/card in total and raise compute
# occupancy substantially above a single ~30%-utilization job.
for variant in pvd drav pvd_rgpc; do
  launch_one 0 astyx "$variant"
  launch_one 1 truckscenes "$variant"
  launch_one 2 v2xradarv "$variant"
  launch_one 3 kradar "$variant"
done

echo "PVD/DRAV/PVD+RGPC seed-2028 factorial relaunched (12 jobs)."
