#!/usr/bin/env bash
set -euo pipefail

root=/root/autodl-tmp/radar_champion
while pgrep -f 'tools/train.py.*[f]air_bevgate_replay5_kradar_seed2028' >/dev/null; do
  sleep 20
done
"$root/eval_bevgate_replay_one.sh" 3 kradar 2028 5
cd "$root"
./run_bevgate_replay10_one.sh 3 kradar 2028
"$root/eval_bevgate_replay_one.sh" 3 kradar 2028 10
