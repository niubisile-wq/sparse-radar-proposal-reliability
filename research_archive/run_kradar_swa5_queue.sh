#!/usr/bin/env bash
set -euo pipefail

root=/root/autodl-tmp/radar_champion
status="$root/logs/fair_ablation/kradar_swa5_queue.status"
echo "$(date -Iseconds) QUEUED" >>"$status"
for seed in 2026 2027 2028; do
    echo "$(date -Iseconds) START seed=$seed" >>"$status"
    "$root/run_swa5_one.sh" 3 kradar "$seed"
    echo "$(date -Iseconds) END seed=$seed" >>"$status"
done
echo "$(date -Iseconds) COMPLETE" >>"$status"
