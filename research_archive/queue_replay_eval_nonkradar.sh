#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET}"
dataset="${2:?usage: $0 GPU DATASET}"
root=/root/autodl-tmp/radar_champion

while pgrep -f "tools/train.py.*[f]air_bevgate_replay5_${dataset}_seed2028" >/dev/null; do
  sleep 20
done
"$root/eval_bevgate_replay_one.sh" "$gpu" "$dataset" 2028 5

while pgrep -f "tools/train.py.*[f]air_bevgate_replay10_${dataset}_seed2028" >/dev/null; do
  sleep 20
done
"$root/eval_bevgate_replay_one.sh" "$gpu" "$dataset" 2028 10
