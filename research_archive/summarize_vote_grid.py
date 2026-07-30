#!/usr/bin/env python3
from __future__ import annotations

import glob
import re
from collections import defaultdict
from pathlib import Path

import numpy as np


LOG_DIR = Path("/root/autodl-tmp/radar_champion/logs/fair_ablation")
BASELINES = {
    ("astyx", 2026): 32.7281,
    ("astyx", 2027): 31.4220,
    ("astyx", 2028): 34.3540,
    ("truckscenes", 2026): 15.4127,
    ("truckscenes", 2027): 18.3845,
    ("truckscenes", 2028): 15.3041,
    ("v2xradarv", 2026): 40.7802,
    ("v2xradarv", 2027): 42.9899,
    ("v2xradarv", 2028): 41.3385,
    ("kradar", 2026): 51.3450,
    ("kradar", 2027): 48.1767,
    ("kradar", 2028): 52.0271,
}
DATASETS = ("astyx", "truckscenes", "v2xradarv", "kradar")
AP_RE = re.compile(r"AP_R40@3D IoU 0\.50:\s*([0-9.]+)")
FILE_RE = re.compile(
    r"(m3rob_q15p25_viou\d+p\d+_s\d+p\d+)_"
    r"(astyx|truckscenes|v2xradarv|kradar)_seed(2026|2027|2028)_gpu"
)
T_CRIT_95_DF2 = 4.303


values: dict[str, dict[tuple[str, int], float]] = defaultdict(dict)
for path in glob.glob(str(LOG_DIR / "m3rob_*_seed202[678]_gpu*.log")):
    match = FILE_RE.search(Path(path).name)
    ap_matches = AP_RE.findall(Path(path).read_text(errors="ignore"))
    if match and ap_matches:
        config, dataset, seed = match.groups()
        values[config][(dataset, int(seed))] = float(ap_matches[-1])

available_datasets = tuple(
    dataset
    for dataset in DATASETS
    if all(
        any((dataset, seed) in config_values for config_values in values.values())
        for seed in (2026, 2027, 2028)
    )
)
required_keys = {
    (dataset, seed)
    for dataset in available_datasets
    for seed in (2026, 2027, 2028)
}
rows = []
for config, config_values in values.items():
    if not all(key in config_values for key in required_keys):
        continue
    gains = {
        key: config_values[key] - BASELINES[key]
        for key in required_keys
    }
    stats = {}
    for dataset in available_datasets:
        vector = np.asarray(
            [gains[(dataset, seed)] for seed in (2026, 2027, 2028)],
            dtype=float,
        )
        mean = float(vector.mean())
        lower = mean - T_CRIT_95_DF2 * float(vector.std(ddof=1)) / np.sqrt(3)
        stats[dataset] = (mean, lower, float(vector.min()))
    positive = sum(value > 0 for value in gains.values())
    min_mean = min(item[0] for item in stats.values())
    min_lower = min(item[1] for item in stats.values())
    rows.append((positive, min_mean, min_lower, config, stats, gains))

rows.sort(reverse=True)
for positive, min_mean, min_lower, config, stats, gains in rows:
    means = " ".join(
        f"{dataset}=mean{stats[dataset][0]:+.4f}/lo{stats[dataset][1]:+.4f}"
        for dataset in available_datasets
    )
    print(
        f"{config} positive={positive}/{len(required_keys)} "
        f"min_mean={min_mean:+.4f} min_CI_lower={min_lower:+.4f} {means}"
    )
    print(
        "  "
        + " ".join(
            f"{dataset}["
            + ",".join(f"{gains[(dataset, seed)]:+.4f}" for seed in (2026, 2027, 2028))
            + "]"
            for dataset in available_datasets
        )
    )
