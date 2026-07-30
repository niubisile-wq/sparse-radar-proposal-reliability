#!/usr/bin/env bash
set -euo pipefail

root=/root/autodl-tmp/radar_champion
previous_status="$root/logs/fair_ablation/dapg_queue.status"
status="$root/logs/fair_ablation/msbc_queue.status"
runner="$root/run_fair_msbc_seed.sh"

echo "$(date -Iseconds) QUEUED msbc_seeds=2026,2027,2028" >>"$status"
until grep -q 'QUEUE_COMPLETE' "$previous_status" 2>/dev/null; do
    sleep 20
done
for seed in 2026 2027 2028; do
    echo "$(date -Iseconds) START_WAVE seed=$seed" >>"$status"
    bash "$runner" "$seed"
    echo "$(date -Iseconds) END_WAVE seed=$seed" >>"$status"
done
echo "$(date -Iseconds) QUEUE_COMPLETE" >>"$status"
