#!/usr/bin/env bash
set -euo pipefail

root="/root/autodl-tmp/稀疏雷达提案可靠性四模块论文实验全量冻结映像_20260727_000030"
log_dir="$root/logs/fair_ablation"
status="$log_dir/gpu_relay_monitor.status"
mkdir -p "$log_dir"

tasks=(
  "stack stable_bevgate_dapg astyx 5623"
  "stack stable_bevgate_dapg truckscenes 5623"
  "stack stable_bevgate_dapg v2xradarv 5623"
  "stack stable_bevgate_dapg kradar 5623"
  "stack stable_bevgate_dapg_msbc astyx 5623"
  "stack stable_bevgate_dapg_msbc truckscenes 5623"
  "stack stable_bevgate_dapg_msbc v2xradarv 5623"
  "stack stable_bevgate_dapg_msbc kradar 5623"
  "stack stable_four_modules astyx 5623"
  "stack stable_four_modules truckscenes 5623"
  "stack stable_four_modules v2xradarv 5623"
  "stack stable_four_modules kradar 5623"
  "iou iouaware astyx 5623"
  "iou iouaware truckscenes 5623"
  "iou iouaware v2xradarv 5623"
  "iou iouaware kradar 5623"
)

log() {
  printf '[%s] %s\n' "$(date '+%F %T')" "$*" | tee -a "$status"
}

free_gpus() {
  nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader,nounits \
    | awk -F, '{
        gsub(/^[ \t]+|[ \t]+$/, "", $1);
        gsub(/^[ \t]+|[ \t]+$/, "", $2);
        gsub(/^[ \t]+|[ \t]+$/, "", $3);
        if ($2+0 < 500 && $3+0 < 10) print $1
      }'
}

launch_task() {
  local gpu="$1"
  local kind="$2"
  local module="$3"
  local dataset="$4"
  local seed="$5"
  local tag
  tag="fair_${module}_${dataset}_seed${seed}"
  case "$kind" in
    stack)
      nohup bash "$root/run_stable_module_stack_one.sh" "$gpu" "$dataset" "$seed" "$module" \
        >"$log_dir/${tag}_gpu${gpu}.launch.log" 2>&1 &
      ;;
    iou)
      nohup bash "$root/run_iouaware_one.sh" "$gpu" "$dataset" "$seed" \
        >"$log_dir/${tag}_gpu${gpu}.launch.log" 2>&1 &
      ;;
    *)
      echo "unsupported kind: $kind" >&2
      return 2
      ;;
  esac
  log "launch gpu=$gpu kind=$kind module=$module dataset=$dataset seed=$seed"
}

log "monitor start"
cursor=0
while (( cursor < ${#tasks[@]} )); do
  mapfile -t free < <(free_gpus)
  if (( ${#free[@]} == 0 )); then
    log "no free gpu; sleep"
    sleep 60
    continue
  fi

  for gpu in "${free[@]}"; do
    if (( cursor >= ${#tasks[@]} )); then
      break
    fi
    read -r kind module dataset seed <<<"${tasks[$cursor]}"
    cursor=$((cursor + 1))
    launch_task "$gpu" "$kind" "$module" "$dataset" "$seed"
  done

  sleep 60
done

log "monitor queue empty"
