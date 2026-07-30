#!/usr/bin/env bash
set -euo pipefail
cd /root/autodl-tmp/radar_champion
nohup ./queue_variant_eval_lane.sh 0 astyx 2028 pvd_rgpc \
  >logs/fair_ablation/queue_eval_pvd_rgpc_astyx.out 2>&1 &
echo "RGPC Astyx evaluation queue launched."
