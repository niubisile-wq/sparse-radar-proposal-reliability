#!/usr/bin/env python3
from __future__ import annotations

import itertools
import json
import math
import pickle
import statistics
from pathlib import Path

import numpy as np
import torch

from pcdet.config import cfg, cfg_from_list, cfg_from_yaml_file
from pcdet.datasets import build_dataloader
from pcdet.ops.iou3d_nms import iou3d_nms_utils


ROOT = Path("/root/autodl-tmp/radar_champion")
REPO = ROOT / "repos/OpenPCDet_current"
SEEDS = (2026, 2027, 2028)
RDAR = {2026: 15.4127, 2027: 18.3845, 2028: 15.3041}
T_CRIT = 4.303


def find_expert(seed: int) -> Path:
    model_part = "pointpillars_stable_bevgate_truckscenes_car"
    tag_part = f"expert_rcnms_stable_bevgate_truckscenes_seed{seed}"
    matches = [
        path
        for path in (REPO / "output").rglob("result.pkl")
        if model_part in path.parts and tag_part in path.parts
    ]
    if not matches:
        raise FileNotFoundError(f"expert seed {seed}")
    return matches[0]


def precompute(seed: int):
    source_path = ROOT / f"results/rdar_qflr55_truckscenes_seed{seed}.pkl"
    with source_path.open("rb") as stream:
        source = pickle.load(stream)
    with find_expert(seed).open("rb") as stream:
        expert = pickle.load(stream)
    if [str(x["frame_id"]) for x in source] != [
        str(x["frame_id"]) for x in expert
    ]:
        raise ValueError(f"frame mismatch for seed {seed}")

    cached = []
    for source_anno, expert_anno in zip(source, expert):
        boxes = np.asarray(source_anno["boxes_3d"], dtype=np.float32).reshape(
            -1, 7
        )
        scores = np.asarray(source_anno["score"], dtype=np.float32)
        expert_boxes = np.asarray(
            expert_anno["boxes_3d"], dtype=np.float32
        ).reshape(-1, 7)
        expert_scores = np.asarray(expert_anno["score"], dtype=np.float32)
        primary_count = max(0, len(boxes) - 50)
        if primary_count and len(expert_boxes):
            with torch.no_grad():
                ious = iou3d_nms_utils.boxes_iou3d_gpu(
                    torch.from_numpy(boxes[:primary_count]).cuda(),
                    torch.from_numpy(expert_boxes).cuda(),
                ).cpu().numpy()
            best_expert = ious.argmax(axis=1)
            best_iou = ious[np.arange(primary_count), best_expert]
            matched_expert_score = expert_scores[best_expert]
        else:
            best_iou = np.zeros(primary_count, dtype=np.float32)
            matched_expert_score = np.zeros(primary_count, dtype=np.float32)
        cached.append(
            {
                "anno": source_anno,
                "scores": scores,
                "primary_count": primary_count,
                "best_iou": best_iou,
                "expert_score": matched_expert_score,
            }
        )
    return cached


def apply_gate(cached, match_iou, alpha, iou_power, unmatched_scale):
    output = []
    for item in cached:
        scores = item["scores"].copy()
        count = item["primary_count"]
        best_iou = item["best_iou"]
        matched = best_iou >= match_iou
        indices = np.flatnonzero(matched)
        if len(indices):
            primary_score = np.clip(scores[indices], 1e-8, 1.0)
            expert_score = np.clip(
                item["expert_score"][indices], 1e-8, 1.0
            )
            quality = np.power(primary_score, 1.0 - alpha)
            quality *= np.power(expert_score, alpha)
            quality *= np.power(
                np.clip(best_iou[indices], 1e-8, 1.0), iou_power
            )
            scores[indices] = quality
        scores[:count][~matched] *= unmatched_scale
        anno = dict(item["anno"])
        anno["score"] = scores.astype(np.float32)
        output.append(anno)
    return output


cfg_file = (
    REPO
    / "tools/cfgs/astyx_models/pointpillars_qflr55_truckscenes_car.yaml"
)
cfg_from_yaml_file(str(cfg_file), cfg)
cfg_from_list(
    [
        "DATA_CONFIG.DATASET",
        "UnifiedRadarDataset",
        "DATA_CONFIG.DATA_PATH",
        str(ROOT / "data/man-truckscenes-mini/unified"),
        "DATA_CONFIG.INFO_PATH.train",
        "['truckscenes_infos_train.pkl']",
        "DATA_CONFIG.INFO_PATH.test",
        "['truckscenes_infos_val.pkl']",
    ],
    cfg,
)
dataset, _, _ = build_dataloader(
    dataset_cfg=cfg.DATA_CONFIG,
    class_names=cfg.CLASS_NAMES,
    batch_size=1,
    dist=False,
    workers=1,
    training=False,
    logger=None,
)

cache = {seed: precompute(seed) for seed in SEEDS}
records = []
grid = itertools.product(
    (0.20, 0.30, 0.40, 0.50),
    (0.05, 0.10, 0.15, 0.20, 0.30),
    (0.00, 0.10, 0.25),
    (0.50, 0.70, 0.85, 1.00),
)
for match_iou, alpha, power, unmatched in grid:
    aps = {}
    for seed in SEEDS:
        annos = apply_gate(
            cache[seed], match_iou, alpha, power, unmatched
        )
        _, metrics = dataset.evaluation(
            annos,
            cfg.CLASS_NAMES,
            eval_metric=cfg.MODEL.POST_PROCESSING.EVAL_METRIC,
        )
        aps[seed] = float(metrics["Car_3d/AP_R40@0.50"])
    deltas = [aps[seed] - RDAR[seed] for seed in SEEDS]
    mean = statistics.mean(deltas)
    std = statistics.stdev(deltas)
    ci_lower = mean - T_CRIT * std / math.sqrt(len(deltas))
    passed = (
        all(value > 0 for value in deltas)
        and mean >= 1.0
        and ci_lower > 0
    )
    records.append(
        {
            "match_iou": match_iou,
            "alpha": alpha,
            "iou_power": power,
            "unmatched_scale": unmatched,
            "aps": {str(key): value for key, value in aps.items()},
            "deltas": deltas,
            "mean": mean,
            "std": std,
            "ci95_lower": ci_lower,
            "min_delta": min(deltas),
            "pass": passed,
        }
    )

records.sort(
    key=lambda item: (
        item["pass"],
        item["ci95_lower"],
        item["min_delta"],
        item["mean"],
    ),
    reverse=True,
)
output_path = ROOT / "results/qflr55_truck_consensus_grid.json"
output_path.write_text(json.dumps(records, indent=2))
print(f"evaluated={len(records)} strict_pass={sum(x['pass'] for x in records)}")
for item in records[:20]:
    print(
        f"iou={item['match_iou']:.2f} a={item['alpha']:.2f} "
        f"p={item['iou_power']:.2f} u={item['unmatched_scale']:.2f} "
        f"deltas={','.join(f'{x:+.4f}' for x in item['deltas'])} "
        f"mean={item['mean']:+.4f} ci={item['ci95_lower']:+.4f} "
        f"pass={item['pass']}"
    )
