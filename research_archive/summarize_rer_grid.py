#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path("/root/autodl-tmp/radar_champion/results")
DATASETS = ("astyx", "truckscenes", "v2xradarv", "kradar")
INPUT_AP = {
    "astyx": 35.6059,
    "truckscenes": 16.2348,
    "v2xradarv": 42.5422,
}

tables = {}
for dataset in DATASETS:
    path = ROOT / f"rer_grid_{dataset}_seed2028.json"
    if path.exists():
        tables[dataset] = {
            row["config"]: float(row["ap"])
            for row in json.loads(path.read_text(encoding="utf-8"))
        }

common = set.intersection(*(set(table) for table in tables.values()))
rows = []
for config in common:
    gains = {
        dataset: tables[dataset][config] - INPUT_AP[dataset]
        for dataset in tables
    }
    rows.append((min(gains.values()), sum(gains.values()) / len(gains), config, gains))

rows.sort(reverse=True)
for min_gain, mean_gain, config, gains in rows[:40]:
    formatted = " ".join(f"{dataset}={gain:+.4f}" for dataset, gain in gains.items())
    print(
        f"{config} min={min_gain:+.4f} mean={mean_gain:+.4f} {formatted}"
    )
