#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import pickle
from pathlib import Path

import numpy as np
import torch

from pcdet.config import cfg, cfg_from_list, cfg_from_yaml_file
from pcdet.datasets import build_dataloader
from pcdet.ops.roiaware_pool3d import roiaware_pool3d_utils


MIXES = {
    "count": ("count",),
    "count_center": ("count", "center"),
    "count_rcs": ("count", "rcs"),
    "count_doppler": ("count", "doppler"),
    "count_center_rcs": ("count", "center", "rcs"),
    "all": ("count", "center", "rcs", "doppler"),
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cfg_file", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output_json", required=True)
    parser.add_argument("--select_config")
    parser.add_argument("--output")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--set", dest="set_cfgs", nargs=argparse.REMAINDER)
    return parser.parse_args()


def positive_rank(values: np.ndarray, supported: np.ndarray) -> np.ndarray:
    result = np.zeros(len(values), dtype=np.float32)
    indices = np.flatnonzero(supported)
    if not len(indices):
        return result
    unique, inverse = np.unique(values[indices], return_inverse=True)
    result[indices] = (inverse.astype(np.float32) + 1.0) / len(unique)
    return result


def feature_ranks(points: np.ndarray, boxes: np.ndarray, range_power: float):
    if not len(boxes):
        return {name: np.zeros(0, dtype=np.float32) for name in ("count", "center", "rcs", "doppler")}
    point_xyz = torch.from_numpy(points[:, :3]).float()
    box_tensor = torch.from_numpy(boxes).float()
    masks = roiaware_pool3d_utils.points_in_boxes_cpu(point_xyz, box_tensor).numpy().astype(bool)
    counts = masks.sum(axis=1).astype(np.float32)
    supported = counts > 0
    ranges = np.linalg.norm(boxes[:, :2], axis=1)
    compensated = counts * np.power(np.maximum(ranges, 5.0) / 20.0, range_power)

    inner_boxes = boxes.copy()
    inner_boxes[:, 3:5] *= 0.60
    inner_masks = roiaware_pool3d_utils.points_in_boxes_cpu(
        point_xyz, torch.from_numpy(inner_boxes).float()
    ).numpy().astype(bool)
    inner_counts = inner_masks.sum(axis=1).astype(np.float32)
    centrality = inner_counts / np.maximum(counts, 1.0)

    median_rcs = np.zeros(len(boxes), dtype=np.float32)
    doppler_coherence = np.zeros(len(boxes), dtype=np.float32)
    for index in np.flatnonzero(supported):
        selected = points[masks[index]]
        median_rcs[index] = float(np.median(selected[:, 3]))
        velocity = selected[:, 4]
        mad = float(np.median(np.abs(velocity - np.median(velocity))))
        doppler_coherence[index] = 1.0 / (1.0 + mad)

    return {
        "count": positive_rank(compensated, supported),
        "center": positive_rank(centrality, supported),
        "rcs": positive_rank(median_rcs, supported),
        "doppler": positive_rank(doppler_coherence, counts >= 2),
    }


def apply_scores(annos, evidence_by_frame, transform: str, alpha: float):
    output = []
    for anno, evidence in zip(annos, evidence_by_frame):
        scores = np.asarray(anno["score"], dtype=np.float32)
        if transform == "mul":
            updated = scores * (1.0 + alpha * evidence)
        elif transform == "logit":
            clipped = np.clip(scores, 1e-6, 1.0 - 1e-6)
            logits = np.log(clipped / (1.0 - clipped)) + alpha * evidence
            updated = 1.0 / (1.0 + np.exp(-logits))
        else:
            raise ValueError(transform)
        updated_anno = dict(anno)
        updated_anno["score"] = np.clip(updated, 1e-8, 1.0).astype(np.float32)
        output.append(updated_anno)
    return output


def main():
    args = parse_args()
    cfg_from_yaml_file(args.cfg_file, cfg)
    if args.set_cfgs:
        cfg_from_list(args.set_cfgs, cfg)
    annos = pickle.load(Path(args.input).open("rb"))
    dataset, _, _ = build_dataloader(
        dataset_cfg=cfg.DATA_CONFIG,
        class_names=cfg.CLASS_NAMES,
        batch_size=1,
        dist=False,
        workers=args.workers,
        training=False,
        logger=None,
    )

    feature_cache = {}
    for power in (0.0, 1.0, 2.0):
        per_frame = []
        for anno in annos:
            boxes = np.asarray(anno["boxes_3d"], dtype=np.float32).reshape(-1, 7)
            points = dataset.get_pointcloud(str(anno["frame_id"]), "radar")
            per_frame.append(feature_ranks(points, boxes, power))
        feature_cache[power] = per_frame

    rows = []
    selected_output = None
    for power, frame_features in feature_cache.items():
        for mix_name, feature_names in MIXES.items():
            evidence_by_frame = [
                np.mean(np.stack([features[name] for name in feature_names]), axis=0)
                for features in frame_features
            ]
            for transform, alphas in (
                ("mul", (0.025, 0.05, 0.10, 0.20, 0.40, 0.80)),
                ("logit", (0.05, 0.10, 0.20, 0.40, 0.80, 1.60)),
            ):
                for alpha in alphas:
                    tag = (
                        f"rer_{mix_name}_p{power:.1f}_{transform}_a{alpha:.3f}"
                        .replace(".", "p")
                    )
                    output_annos = apply_scores(
                        annos, evidence_by_frame, transform, alpha
                    )
                    _, result_dict = dataset.evaluation(
                        output_annos,
                        cfg.CLASS_NAMES,
                        eval_metric=cfg.MODEL.POST_PROCESSING.EVAL_METRIC,
                    )
                    ap = float(result_dict["Car_3d/AP_R40@0.50"])
                    rows.append({"config": tag, "ap": ap})
                    print(f"{tag} AP={ap:.6f}", flush=True)
                    if args.select_config == tag:
                        selected_output = output_annos

    rows.sort(key=lambda item: item["ap"], reverse=True)
    Path(args.output_json).write_text(
        json.dumps(rows, indent=2), encoding="utf-8"
    )
    if args.select_config:
        if selected_output is None:
            raise ValueError(f"Unknown select_config: {args.select_config}")
        if not args.output:
            raise ValueError("--output is required with --select_config")
        with Path(args.output).open("wb") as stream:
            pickle.dump(selected_output, stream)
    print("TOP")
    for row in rows[:20]:
        print(f"{row['config']} AP={row['ap']:.6f}")


if __name__ == "__main__":
    main()
