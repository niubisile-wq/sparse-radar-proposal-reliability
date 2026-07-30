#!/usr/bin/env bash
set -euo pipefail

root=/root/autodl-tmp/radar_champion
result="$root/results/rdar_qflr55_kradar_seed2028.pkl"
log="$root/logs/qflr55_kradar_formal_queue.log"

while [[ ! -s "$result" ]]; do
    sleep 20
done

ap="$(
    grep 'AP_R40@3D IoU 0.50' \
        "$root/logs/fair_ablation/eval_rdar_qflr55_kradar_seed2028_gpu3.log" \
        | tail -1 | awk '{print $NF}'
)"
if ! awk -v value="$ap" 'BEGIN { exit !(value >= 53.0271) }'; then
    printf 'seed2028 rejected: AP=%s, required>=53.0271\n' "$ap" >>"$log"
    exit 0
fi

printf 'seed2028 passed: AP=%s; starting formal seeds\n' "$ap" >>"$log"
for seed in 2026 2027; do
    env QFL_VARIANT=qflr55 "$root/run_qfl_one.sh" 3 kradar "$seed"
    "$root/eval_qfl_rdar_one.sh" 3 kradar "$seed" qflr55
    printf 'completed seed=%s\n' "$seed" >>"$log"
done
