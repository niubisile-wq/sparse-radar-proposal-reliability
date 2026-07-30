#!/usr/bin/env bash
set -euo pipefail

variant="${1:?usage: $0 VARIANT}"
root=/root/autodl-tmp/radar_champion
cd "$root"

launch_one() {
  local gpu="$1"
  local dataset="$2"
  nohup env QFL_VARIANT="$variant" ./run_qfl_one.sh \
    "$gpu" "$dataset" 2028 \
    >"logs/fair_ablation/launch_${variant}_${dataset}_seed2028.out" 2>&1 &
  nohup ./queue_variant_eval_lane.sh "$gpu" "$dataset" 2028 "$variant" \
    >"logs/fair_ablation/queue_eval_${variant}_${dataset}_seed2028.out" 2>&1 &
}

launch_one 0 astyx
launch_one 1 truckscenes
launch_one 2 v2xradarv
launch_one 3 kradar
echo "$variant four-dataset seed-2028 screen launched."
