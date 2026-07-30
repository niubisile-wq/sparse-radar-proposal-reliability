#!/usr/bin/env bash
set -euo pipefail

root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"
status="$root/logs/fair_ablation/rdar_kradar_resume_eval.status"
: >"$status"

cd "$root"
for seed in 2027 2028; do
    checkpoint=""
    while [[ -z "$checkpoint" ]]; do
        checkpoint="$(
            find "$repo/output" \
                -path "*pointpillars_taac_kradar_car/fair_taac_kradar_seed${seed}/ckpt/checkpoint_epoch_160.pth" \
                -print -quit
        )"
        [[ -n "$checkpoint" ]] || sleep 10
    done

    echo "$(date -Iseconds) START taac_rcnms seed=$seed" >>"$status"
    ./eval_taac_rcnms_one.sh 0 kradar "$seed"
    echo "$(date -Iseconds) END taac_rcnms seed=$seed" >>"$status"

    echo "$(date -Iseconds) START rdar seed=$seed" >>"$status"
    ./eval_rdar_one.sh 0 kradar "$seed"
    echo "$(date -Iseconds) END rdar seed=$seed" >>"$status"
done
