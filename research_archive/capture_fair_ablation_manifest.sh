#!/usr/bin/env bash
set -euo pipefail

root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"
out="$root/results/fair_ablation_manifest_$(date +%Y%m%d_%H%M%S).txt"
mkdir -p "$root/results"

{
    echo "captured_at=$(date -Iseconds)"
    echo "hostname=$(hostname)"
    echo "repo=$repo"
    echo
    echo "[git]"
    git -C "$repo" rev-parse HEAD
    git -C "$repo" status --short \
        pcdet/models/backbones_2d/base_bev_backbone.py \
        pcdet/models/backbones_3d/__init__.py \
        pcdet/models/backbones_3d/density_aware_pillar_gate.py \
        tools/cfgs/astyx_models
    echo
    echo "[runtime]"
    "$root/envs/radar310/bin/python" --version
    "$root/envs/radar310/bin/python" -c \
        'import torch, numpy, yaml; print("torch", torch.__version__); print("cuda", torch.version.cuda); print("numpy", numpy.__version__); print("yaml", yaml.__version__)'
    nvidia-smi --query-gpu=index,name,driver_version,memory.total \
        --format=csv,noheader
    echo
    echo "[sha256]"
    sha256sum \
        "$repo/pcdet/models/backbones_2d/base_bev_backbone.py" \
        "$repo/pcdet/models/backbones_3d/__init__.py" \
        "$repo/pcdet/models/backbones_3d/density_aware_pillar_gate.py" \
        "$repo"/tools/cfgs/astyx_models/pointpillars_bevgate_*_car.yaml \
        "$repo"/tools/cfgs/astyx_models/pointpillars_four_modules_*_car.yaml \
        "$root"/run_fair_*_seed.sh \
        "$root"/queue_*_after_*.sh \
        "$root/collect_fair_ablation.py"
} >"$out"

echo "$out"
