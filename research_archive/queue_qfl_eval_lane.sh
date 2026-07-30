#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET [WAIT_FOR_BOTH]}"
dataset="${2:?usage: $0 GPU DATASET [WAIT_FOR_BOTH]}"
wait_for_both="${3:-0}"
root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"
seed=2028

wait_checkpoint() {
  local variant="$1"
  while ! find "$repo/output" \
    -path "*pointpillars_${variant}_${dataset}_car/screen_${variant}_${dataset}_seed${seed}/ckpt/checkpoint_epoch_160.pth" \
    -print -quit | grep -q .; do
    sleep 20
  done
}

if [[ "$wait_for_both" == 1 ]]; then
  wait_checkpoint qfl
  wait_checkpoint qflf
  "$root/eval_qfl_rdar_one.sh" "$gpu" "$dataset" "$seed" qfl
  "$root/eval_qfl_rdar_one.sh" "$gpu" "$dataset" "$seed" qflf
else
  wait_checkpoint qfl
  "$root/eval_qfl_rdar_one.sh" "$gpu" "$dataset" "$seed" qfl
  wait_checkpoint qflf
  "$root/eval_qfl_rdar_one.sh" "$gpu" "$dataset" "$seed" qflf
fi
