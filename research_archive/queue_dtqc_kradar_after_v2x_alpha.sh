#!/usr/bin/env bash
set -euo pipefail

root=/root/autodl-tmp/radar_champion
for tag in 25 35 65 75; do
    result="$root/results/rdar_dtqca${tag}_v2xradarv_seed2028.pkl"
    while [[ ! -s "$result" ]]; do
        sleep 15
    done
done

cd "$root"
QFL_VARIANT=dtqc ./run_qfl_one.sh 3 kradar 2028 &
QFL_VARIANT=dtqc ./queue_variant_eval_lane.sh 3 kradar 2028 dtqc &
wait
