#!/usr/bin/env bash
set -euo pipefail

root=/root/autodl-tmp/radar_champion
status="$root/logs/fair_ablation/kradar_candidate_queue.status"
echo "$(date -Iseconds) QUEUED" >>"$status"
while pgrep -f "tools/train.py.*fair_pointpillars_kradar_seed2028" >/dev/null; do
    sleep 10
done
for module in dapg2 msbc2 range2; do
    echo "$(date -Iseconds) START module=$module seed=2028" >>"$status"
    "$root/run_candidate_one.sh" 3 "$module" kradar 2028
    echo "$(date -Iseconds) END module=$module seed=2028" >>"$status"
done
echo "$(date -Iseconds) COMPLETE" >>"$status"
