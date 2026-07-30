#!/usr/bin/env bash
set -euo pipefail

root=/root/autodl-tmp/radar_champion
seed=2028
while [[ ! -f "$root/results/rdar_qflf_kradar_seed${seed}.pkl" ]]; do
  sleep 20
done
cd "$root"
for variant in qflr qflr75 qflh; do
  env QFL_VARIANT="$variant" ./run_qfl_one.sh 3 kradar "$seed"
  ./eval_qfl_rdar_one.sh 3 kradar "$seed" "$variant"
done
