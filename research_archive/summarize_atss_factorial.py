#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/root/autodl-tmp/radar_champion")
LOGS = ROOT / "logs/fair_ablation"
SEED = 2028
DATASETS = ("astyx", "truckscenes", "v2xradarv", "kradar")
VARIANTS = ("atss", "qflr55atss", "dtqcatss")
REFERENCE = {
    "astyx": 34.3540,
    "truckscenes": 15.3041,
    "v2xradarv": 41.3385,
    "kradar": 52.0271,
}
AP_RE = re.compile(r"AP_R40@3D IoU 0\.50:\s*([0-9.]+)")


def read_ap(variant: str, dataset: str):
    paths = sorted(
        LOGS.glob(
            f"eval_rdar_{variant}_{dataset}_seed{SEED}_gpu*.log"
        )
    )
    if not paths:
        return None
    values = AP_RE.findall(paths[-1].read_text(errors="ignore"))
    return float(values[-1]) if values else None


print("| Variant | Astyx | TruckScenes | V2X-Radar-V | K-Radar |")
print("|---|---:|---:|---:|---:|")
print("| RDAR reference | 34.3540 | 15.3041 | 41.3385 | 52.0271 |")
for variant in VARIANTS:
    cells = []
    for dataset in DATASETS:
        ap = read_ap(variant, dataset)
        if ap is None:
            cells.append("pending")
        else:
            cells.append(f"{ap:.4f} ({ap - REFERENCE[dataset]:+.4f})")
    print(f"| {variant} | " + " | ".join(cells) + " |")
