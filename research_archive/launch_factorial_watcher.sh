#!/usr/bin/env bash
set -euo pipefail
cd /root/autodl-tmp/radar_champion
nohup ./watch_physics_context_factorial.sh \
  >logs/fair_ablation/physics_context_factorial_watcher.out 2>&1 &
echo "physics/context watcher launched."
