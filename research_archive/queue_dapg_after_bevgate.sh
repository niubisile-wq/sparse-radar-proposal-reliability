#!/usr/bin/env bash
set -euo pipefail

root=/root/autodl-tmp/radar_champion
queue_status="$root/logs/fair_ablation/seed_queue.status"
dapg_status="$root/logs/fair_ablation/dapg_queue.status"
runner="$root/run_fair_dapg_seed.sh"

echo "$(date -Iseconds) QUEUED dapg_seeds=2026,2027,2028" >>"$dapg_status"
until grep -q 'QUEUE_COMPLETE' "$queue_status" 2>/dev/null; do
    sleep 20
done

for seed in 2026 2027 2028; do
    echo "$(date -Iseconds) START_WAVE seed=$seed" >>"$dapg_status"
    bash "$runner" "$seed"
    echo "$(date -Iseconds) END_WAVE seed=$seed" >>"$dapg_status"
done

echo "$(date -Iseconds) QUEUE_COMPLETE" >>"$dapg_status"
