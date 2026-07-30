#!/usr/bin/env bash
set -euo pipefail

root=/root/autodl-tmp/radar_champion
py="$root/envs/radar310/bin/python"
status="$root/results/physics_context_factorial_watcher.status"
mkdir -p "$root/results"
cd "$root"

gate_status() {
  local variant="$1"
  shift
  set +e
  "$py" evaluate_variant_gate.py "$variant" "$@" >/dev/null 2>&1
  local result=$?
  set -e
  echo "$result"
}

wait_for_initial_factorial() {
  while true; do
    local pending=0
    [[ "$(gate_status pvd --mode screen)" -ne 2 ]] || pending=1
    [[ "$(gate_status drav --mode screen)" -ne 2 ]] || pending=1
    [[ "$(gate_status pvd_rgpc --reference-variant pvd --mode screen)" \
      -ne 2 ]] || pending=1
    if [[ "$pending" -eq 0 ]]; then
      return
    fi
    sleep 30
  done
}

wait_for_gate_completion() {
  local variant="$1"
  shift
  while true; do
    local result
    result="$(gate_status "$variant" "$@")"
    if [[ "$result" -ne 2 ]]; then
      echo "$result"
      return 0
    fi
    sleep 30
  done
}

echo "waiting_initial_factorial $(date -Iseconds)" >"$status"
wait_for_initial_factorial

set +e
"$py" evaluate_variant_gate.py pvd --mode screen
pvd_screen=$?
"$py" evaluate_variant_gate.py drav --mode screen
drav_screen=$?
"$py" evaluate_variant_gate.py pvd_rgpc \
  --reference-variant pvd --mode screen
rgpc_on_pvd_screen=$?
set -e
{
  echo "initial_complete $(date -Iseconds)"
  echo "pvd_vs_rdar=$pvd_screen"
  echo "drav_vs_rdar=$drav_screen"
  echo "pvd_rgpc_vs_pvd=$rgpc_on_pvd_screen"
} >"$status"

if [[ "$drav_screen" -eq 0 ]] \
  && [[ ! -e "$root/results/drav_formal.launched" ]]; then
  ./launch_variant_formal.sh drav
  touch "$root/results/drav_formal.launched"
  echo "drav_formal_launched $(date -Iseconds)" >>"$status"
fi

if [[ "$drav_screen" -eq 0 && "$rgpc_on_pvd_screen" -eq 0 ]] \
  && [[ ! -e "$root/results/drav_rgpc_screen.launched" ]]; then
  ./launch_variant_screen.sh drav_rgpc
  touch "$root/results/drav_rgpc_screen.launched"
  echo "drav_rgpc_screen_launched $(date -Iseconds)" >>"$status"

  drav_rgpc_screen="$(
    wait_for_gate_completion drav_rgpc \
      --reference-variant drav --mode screen
  )"
  echo "drav_rgpc_vs_drav=$drav_rgpc_screen" >>"$status"
  if [[ "$drav_rgpc_screen" -eq 0 ]] \
    && [[ ! -e "$root/results/drav_rgpc_formal.launched" ]]; then
    ./launch_variant_formal.sh drav_rgpc
    touch "$root/results/drav_rgpc_formal.launched"
    echo "drav_rgpc_formal_launched $(date -Iseconds)" >>"$status"
  fi
fi

# Produce formal reports as soon as all required paired seeds exist. A failed
# screen simply leaves the corresponding formal stage unlaunched.
if [[ -e "$root/results/drav_formal.launched" ]]; then
  drav_formal_gate="$(
    wait_for_gate_completion drav --mode formal
  )"
  echo "drav_formal_gate=$drav_formal_gate" >>"$status"
fi
if [[ -e "$root/results/drav_rgpc_formal.launched" ]]; then
  drav_rgpc_formal_gate="$(
    wait_for_gate_completion drav_rgpc \
      --reference-variant drav --mode formal
  )"
  echo "drav_rgpc_formal_gate=$drav_rgpc_formal_gate" >>"$status"
fi
echo "watcher_finished $(date -Iseconds)" >>"$status"
