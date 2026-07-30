#!/usr/bin/env bash
set -euo pipefail

root=/root/autodl-tmp/radar_champion
status="$root/logs/fair_ablation/kradar_sbd_queue.status"
echo "$(date -Iseconds) QUEUED" >>"$status"
for module in sbd05 sbd10 sbd20; do
    echo "$(date -Iseconds) START module=$module seed=2028" >>"$status"
    "$root/run_candidate_one.sh" 3 "$module" kradar 2028
    echo "$(date -Iseconds) END module=$module seed=2028" >>"$status"
done
echo "$(date -Iseconds) COMPLETE" >>"$status"
