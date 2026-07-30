#!/usr/bin/env bash
set -euo pipefail

root=/root/autodl-tmp/radar_champion
seed2027_result="$root/results/rdar_qflr_v2xradarv_seed2027.pkl"
log="$root/logs/qflr_v2x_sequential_queue.log"

while [[ ! -s "$seed2027_result" ]]; do
    sleep 20
done

printf 'seed2027 complete; restarting seed2026 alone on GPU3\n' >>"$log"
env QFL_VARIANT=qflr "$root/run_qfl_one.sh" 3 v2xradarv 2026
printf 'seed2026 training complete; existing eval queue will evaluate it\n' \
    >>"$log"
