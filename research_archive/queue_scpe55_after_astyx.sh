#!/usr/bin/env bash
set -euo pipefail

root=/root/autodl-tmp/radar_champion
result="$root/results/rdar_scpe55_astyx_seed2028.pkl"
eval_log="$root/logs/fair_ablation/eval_rdar_scpe55_astyx_seed2028_gpu0.log"
queue_log="$root/logs/scpe55_screen_queue.log"

while [[ ! -s "$result" ]]; do
    sleep 20
done

ap="$(
    grep 'AP_R40@3D IoU 0.50' "$eval_log" |
        tail -1 | awk '{print $NF}'
)"
if ! awk -v value="$ap" 'BEGIN { exit !(value >= 38.0318) }'; then
    printf 'Astyx rejected: AP=%s, required>=38.0318\n' "$ap" >>"$queue_log"
    exit 0
fi

printf 'Astyx passed: AP=%s; launching TruckScenes and V2X screens\n' \
    "$ap" >>"$queue_log"

env QFL_VARIANT=scpe55 "$root/run_qfl_one.sh" \
    1 truckscenes 2028 &
truck_pid=$!
env QFL_VARIANT=scpe55 "$root/run_qfl_one.sh" \
    2 v2xradarv 2028 &
v2x_pid=$!

"$root/queue_variant_eval_lane.sh" 1 truckscenes 2028 scpe55 &
truck_eval_pid=$!
"$root/queue_variant_eval_lane.sh" 2 v2xradarv 2028 scpe55 &
v2x_eval_pid=$!

wait "$truck_pid" "$v2x_pid"
wait "$truck_eval_pid" "$v2x_eval_pid"
printf 'TruckScenes and V2X screens completed\n' >>"$queue_log"
