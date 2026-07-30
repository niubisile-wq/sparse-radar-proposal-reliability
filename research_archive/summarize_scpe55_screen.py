#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/root/autodl-tmp/radar_champion")
LOGS = ROOT / "logs/fair_ablation"
M3_SEED2028 = {
    "astyx": 37.0318,
    "truckscenes": 17.4530,
    "v2xradarv": 42.5979,
    "kradar": None,
}
AP_RE = re.compile(r"AP_R40@3D IoU 0\.50:\s*([0-9.]+)")


all_complete = True
all_pass = True
for dataset, reference in M3_SEED2028.items():
    paths = sorted(
        LOGS.glob(f"eval_rdar_scpe55_{dataset}_seed2028_gpu*.log")
    )
    if not paths:
        print(f"{dataset}: pending")
        all_complete = False
        all_pass = False
        continue
    values = AP_RE.findall(paths[-1].read_text(errors="ignore"))
    if not values:
        print(f"{dataset}: running")
        all_complete = False
        all_pass = False
        continue
    ap = float(values[-1])
    if reference is None:
        print(f"{dataset}: AP={ap:.4f}, M3 reference pending")
        all_complete = False
        all_pass = False
        continue
    gain = ap - reference
    passed = gain >= 1.0
    all_pass &= passed
    print(f"{dataset}: AP={ap:.4f} gain={gain:+.4f} seed_gate={passed}")

print(f"scpe55_complete={all_complete} seed2028_gate={all_pass}")
