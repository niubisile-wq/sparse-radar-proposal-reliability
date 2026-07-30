#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


LOG_DIR = Path("/root/autodl-tmp/radar_champion/logs/fair_ablation")
VARIANTS = ("qfl", "qflf", "qflr", "qflr75", "qflh")
DATASETS = ("astyx", "truckscenes", "v2xradarv", "kradar")
RDAR = {
    "astyx": 34.3540,
    "truckscenes": 15.3041,
    "v2xradarv": 41.3385,
    "kradar": 52.0271,
}
AP_RE = re.compile(r"AP_R40@3D IoU 0\.50:\s*([0-9.]+)")


for variant in VARIANTS:
    cells = []
    passed = True
    for dataset in DATASETS:
        matches = list(
            LOG_DIR.glob(
                f"eval_rdar_{variant}_{dataset}_seed2028_gpu*.log"
            )
        )
        if not matches:
            cells.append(f"{dataset}=pending")
            passed = False
            continue
        values = AP_RE.findall(matches[-1].read_text(errors="ignore"))
        if not values:
            cells.append(f"{dataset}=running")
            passed = False
            continue
        ap = float(values[-1])
        gain = ap - RDAR[dataset]
        cells.append(f"{dataset}={ap:.4f}({gain:+.4f})")
        passed &= gain >= 1.0
    print(f"{variant}: {' '.join(cells)} seed2028_gate={passed}")
