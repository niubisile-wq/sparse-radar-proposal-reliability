#!/usr/bin/env bash
set -euo pipefail

root=/root/autodl-tmp/radar_champion
status="$root/logs/fair_ablation/kradar_candidate_v3_queue.status"
echo "$(date -Iseconds) QUEUED" >>"$status"
for module in dapg3 msbc3 range3; do
    echo "$(date -Iseconds) START module=$module seed=2028" >>"$status"
    "$root/run_candidate_one.sh" 3 "$module" kradar 2028
    echo "$(date -Iseconds) END module=$module seed=2028" >>"$status"
done
echo "$(date -Iseconds) COMPLETE" >>"$status"
