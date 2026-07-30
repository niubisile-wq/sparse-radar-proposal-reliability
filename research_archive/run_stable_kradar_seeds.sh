#!/usr/bin/env bash
set -euo pipefail

root=/root/autodl-tmp/radar_champion
cd "$root"
./run_stable_bevgate_one.sh 3 kradar 2026
./run_stable_bevgate_one.sh 3 kradar 2027
