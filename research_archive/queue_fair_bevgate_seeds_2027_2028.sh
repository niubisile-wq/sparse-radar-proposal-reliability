#!/usr/bin/env bash
set -euo pipefail

root=/root/autodl-tmp/radar_champion
runner="$root/run_fair_baseline_bevgate_seed2026.sh"
queue_log="$root/logs/fair_ablation/seed_queue.status"

echo "$(date -Iseconds) QUEUED seeds=2027,2028 waiting_for=2026" >>"$queue_log"

while pgrep -f 'tools/train.py.*fair_.*seed2026' >/dev/null; do
    sleep 20
done

echo "$(date -Iseconds) START_WAVE seed=2027" >>"$queue_log"
bash "$runner" 2027
echo "$(date -Iseconds) END_WAVE seed=2027" >>"$queue_log"

echo "$(date -Iseconds) START_WAVE seed=2028" >>"$queue_log"
bash "$runner" 2028
echo "$(date -Iseconds) END_WAVE seed=2028" >>"$queue_log"

echo "$(date -Iseconds) QUEUE_COMPLETE" >>"$queue_log"
