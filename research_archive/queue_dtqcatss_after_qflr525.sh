#!/usr/bin/env bash
set -euo pipefail

root=/root/autodl-tmp/radar_champion
for dataset in astyx truckscenes v2xradarv; do
    while [[ ! -s "$root/results/rdar_qflr525_${dataset}_seed2028.pkl" ]]; do
        sleep 15
    done
done

cd "$root"
for dataset in astyx truckscenes v2xradarv; do
    QFL_VARIANT=dtqcatss ./run_qfl_one.sh 0 "$dataset" 2028 &
    QFL_VARIANT=dtqcatss ./queue_variant_eval_lane.sh \
        0 "$dataset" 2028 dtqcatss &
done
wait
