#!/usr/bin/env python3
from __future__ import annotations

import glob
import math
import re
from collections import defaultdict
from pathlib import Path


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
FORMAL_RE = re.compile(
    r"qformal_(iou\d+p\d+_a\d+p\d+_p\d+p\d+_u\d+p\d+)_"
    r"(astyx|truckscenes|v2xradarv|kradar)_seed(2026|2027)_gpu"
)
SCREEN_RE = re.compile(
    r"aeq_stable_bevgate_(iou\d+p\d+_a\d+p\d+_p\d+p\d+_u\d+p\d+)_"
    r"(astyx|truckscenes|v2xradarv|kradar)_seed2028_gpu"
)


def read_ap(path: str) -> float | None:
    matches = AP_RE.findall(Path(path).read_text(errors="ignore"))
    return float(matches[-1]) if matches else None


values: dict[str, dict[tuple[str, int], float]] = defaultdict(dict)
for path in glob.glob(str(LOG_DIR / "qformal_*_seed202[67]_gpu*.log")):
    match = FORMAL_RE.search(Path(path).name)
    ap = read_ap(path)
    if match and ap is not None:
        config, dataset, seed = match.groups()
        values[config][(dataset, int(seed))] = ap
for path in glob.glob(str(LOG_DIR / "aeq_stable_bevgate_*_seed2028_gpu*.log")):
    match = SCREEN_RE.search(Path(path).name)
    ap = read_ap(path)
    if match and ap is not None:
        config, dataset = match.groups()
        values[config][(dataset, 2028)] = ap

rows = []
available_keys = set.intersection(
    *(set(config_values) for config_values in values.values())
) if values else set()
available_datasets = tuple(
    dataset
    for dataset in DATASETS
    if all((dataset, seed) in available_keys for seed in (2026, 2027, 2028))
)
available_baselines = {
    key: baseline
    for key, baseline in BASELINES.items()
    if key[0] in available_datasets
}

for config, config_values in values.items():
    if not available_baselines or not all(key in config_values for key in available_baselines):
        continue
    gains = {
        key: config_values[key] - baseline
        for key, baseline in available_baselines.items()
    }
    dataset_means = {
        dataset: sum(gains[(dataset, seed)] for seed in (2026, 2027, 2028)) / 3
        for dataset in available_datasets
    }
    positive = sum(gain > 0 for gain in gains.values())
    worst = min(gains.values())
    min_mean = min(dataset_means.values())
    rows.append((positive, min_mean, worst, config, dataset_means, gains))

rows.sort(reverse=True)
for positive, min_mean, worst, config, dataset_means, gains in rows[:24]:
    means = " ".join(
        f"{dataset}={dataset_means[dataset]:+.4f}"
        for dataset in available_datasets
    )
    print(
        f"{config} positive={positive}/12 min_mean={min_mean:+.4f} "
        f"worst={worst:+.4f} {means}"
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
