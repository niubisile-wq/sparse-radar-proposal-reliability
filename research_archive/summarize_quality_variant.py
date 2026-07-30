#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import re
import statistics
from pathlib import Path


ROOT = Path("/root/autodl-tmp/radar_champion")
LOGS = ROOT / "logs/fair_ablation"
SEEDS = (2026, 2027, 2028)
BASELINE = {
    "astyx": {2026: 32.7281, 2027: 31.4220, 2028: 34.3540},
    "truckscenes": {2026: 15.4127, 2027: 18.3845, 2028: 15.3041},
    "v2xradarv": {2026: 40.7802, 2027: 42.9899, 2028: 41.3385},
    "kradar": {2026: 51.3450, 2027: 48.1767, 2028: 52.0271},
}
AP_RE = re.compile(r"AP_R40@3D IoU 0\.50:\s*([0-9.]+)")
T_CRIT = 4.303


parser = argparse.ArgumentParser()
parser.add_argument("variant")
args = parser.parse_args()


def read_ap(dataset, seed):
    paths = sorted(
        LOGS.glob(
            f"eval_rdar_{args.variant}_{dataset}_seed{seed}_gpu*.log"
        )
    )
    if not paths:
        return None
    values = AP_RE.findall(paths[-1].read_text(errors="ignore"))
    return float(values[-1]) if values else None


all_complete = True
all_pass = True
for dataset, baseline_by_seed in BASELINE.items():
    aps = {seed: read_ap(dataset, seed) for seed in SEEDS}
    deltas = {
        seed: aps[seed] - baseline_by_seed[seed]
        for seed in SEEDS
        if aps[seed] is not None
    }
    cells = " ".join(
        f"s{seed}={aps[seed]:.4f}({deltas[seed]:+.4f})"
        if aps[seed] is not None
        else f"s{seed}=pending"
        for seed in SEEDS
    )
    complete = len(deltas) == 3
    all_complete &= complete
    if not complete:
        print(f"{dataset}: {cells} formal_gate=pending")
        all_pass = False
        continue
    values = list(deltas.values())
    mean = statistics.mean(values)
    std = statistics.stdev(values)
    ci_lower = mean - T_CRIT * std / math.sqrt(3)
    passed = (
        all(value > 0 for value in values)
        and mean >= 1.0
        and ci_lower > 0
    )
    all_pass &= passed
    print(
        f"{dataset}: {cells} mean={mean:+.4f} std={std:.4f} "
        f"ci95_lower={ci_lower:+.4f} formal_gate={passed}"
    )

print(
    f"variant={args.variant} complete={all_complete} "
    f"all_datasets_formal_gate={all_pass}"
)
