#!/usr/bin/env bash
set -euo pipefail
root=/root/autodl-tmp/radar_champion
cd "$root"

date -Iseconds
nvidia-smi --query-gpu=index,utilization.gpu,memory.used,memory.total \
  --format=csv,noheader
for variant in pvd drav pvd_rgpc; do
  for dataset in astyx truckscenes v2xradarv kradar; do
    log="$(
      ls -t logs/fair_ablation/screen_"${variant}"_"${dataset}"_seed2028_gpu*.log \
        2>/dev/null | head -1
    )"
    progress="$(
      grep 'Train:' "$log" 2>/dev/null | tail -1 \
        | sed -E 's/.*Train: +([0-9]+)\/160.*\(([ 0-9]+)%\).*/epoch=\1 progress=\2%/'
    )"
    printf '%-10s %-12s %s\n' "$variant" "$dataset" "${progress:-starting}"
  done
done
