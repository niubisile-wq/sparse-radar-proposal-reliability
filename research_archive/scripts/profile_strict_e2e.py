#!/usr/bin/env python3
"""Profile the strict route end-to-end in one process.

This is intentionally a profiling script rather than part of the training or
evaluation path.  It loads the primary and expert detectors in one Python
process, runs batch-1 samples, and measures the actual sequential route:
primary H2D/forward -> expert H2D/forward -> IoU gate -> box voting.
"""
from __future__ import annotations

import argparse
import copy
import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch
from easydict import EasyDict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT))
from pcdet.config import cfg_from_yaml_file  # noqa: E402
from pcdet.datasets import build_dataloader  # noqa: E402
from pcdet.models import build_network, load_data_to_gpu  # noqa: E402
from pcdet.ops.iou3d_nms import iou3d_nms_utils  # noqa: E402
from pcdet.utils import common_utils  # noqa: E402


def load_cfg(path: str):
    config = EasyDict()
    cfg_from_yaml_file(path, config)
    return config


def configure_candidate_rich_output(config):
    """Expose the retained proposal budget used by the strict offline route."""
    post = config.MODEL.POST_PROCESSING
    if "SCORE_THRESH" in post:
        post.SCORE_THRESH = 0.0
    nms = post.NMS_CONFIG
    if "NMS_PRE_MAXSIZE" in nms:
        nms.NMS_PRE_MAXSIZE = 500
    if "NMS_POST_MAXSIZE" in nms:
        nms.NMS_POST_MAXSIZE = 500
    if "MAX_OBJ_PER_SAMPLE" in post:
        post.MAX_OBJ_PER_SAMPLE = 500


def circular_box_mean(boxes, weights):
    weights = weights.astype(np.float64)
    weights /= max(weights.sum(), 1e-12)
    mean = np.sum(boxes.astype(np.float64) * weights[:, None], axis=0)
    mean[6] = 0.5 * np.arctan2(
        np.sum(weights * np.sin(2.0 * boxes[:, 6])),
        np.sum(weights * np.cos(2.0 * boxes[:, 6])),
    )
    return mean.astype(np.float32)


def run_gate_and_vote(primary, expert, match_iou=0.24, alpha=0.40,
                      iou_power=1.0, unmatched_scale=0.85,
                      vote_iou=0.55, vote_strength=0.50,
                      residual_count=50):
    boxes = primary["pred_boxes"].detach()
    scores = primary.get("pred_scores", primary.get("score")).detach()
    expert_boxes = expert["pred_boxes"].detach()
    expert_scores = expert.get("pred_scores", expert.get("score")).detach()
    primary_count = max(0, int(boxes.shape[0]) - residual_count)

    if primary_count and expert_boxes.shape[0]:
        ious = iou3d_nms_utils.boxes_iou3d_gpu(
            boxes[:primary_count], expert_boxes
        )
        best_iou, best_expert = ious.max(dim=1)
        matched = best_iou >= match_iou
        if matched.any():
            ids = torch.nonzero(matched, as_tuple=False).flatten()
            ps = scores[ids].clamp_min(1e-8)
            es = expert_scores[best_expert[ids]].clamp_min(1e-8)
            quality = ps.pow(1.0 - alpha) * es.pow(alpha)
            quality = quality * best_iou[ids].clamp_min(1e-8).pow(iou_power)
            scores = scores.clone()
            scores[ids] = quality
        unmatched = ~matched
        if unmatched.any():
            scores = scores.clone()
            scores[:primary_count][unmatched] *= unmatched_scale

    # Voting is run on the primary proposals after gate score refinement.
    refined = boxes.clone()
    if primary_count > 1:
        primary_boxes = refined[:primary_count]
        primary_scores = scores[:primary_count]
        ious = iou3d_nms_utils.boxes_iou3d_gpu(primary_boxes, primary_boxes)
        for index in range(primary_count):
            neighbors = torch.nonzero(ious[index] >= vote_iou, as_tuple=False).flatten()
            if neighbors.numel() <= 1:
                continue
            nb = primary_boxes[neighbors].detach().cpu().numpy()
            nw = primary_scores[neighbors].detach().cpu().numpy()
            consensus = torch.from_numpy(circular_box_mean(nb, np.maximum(nw, 1e-8))).to(
                refined.device, dtype=refined.dtype
            )
            dims = torch.arange(6, device=refined.device)
            refined[index, dims] = (1.0 - vote_strength) * primary_boxes[index, dims] + vote_strength * consensus[dims]
            angles = torch.stack((primary_boxes[index, 6], consensus[6]))
            aw = torch.tensor([1.0 - vote_strength, vote_strength], device=refined.device, dtype=refined.dtype)
            refined[index, 6] = 0.5 * torch.atan2((aw * torch.sin(2.0 * angles)).sum(), (aw * torch.cos(2.0 * angles)).sum())

    # Force all asynchronous GPU work and CPU conversions into the measured
    # post-processing endpoint before returning.
    torch.cuda.synchronize()
    return refined, scores


def timed_forward(model, batch):
    load_data_to_gpu(batch)
    torch.cuda.synchronize()
    begin = time.perf_counter()
    with torch.no_grad():
        pred_dicts, _ = model(batch)
    torch.cuda.synchronize()
    return pred_dicts[0], (time.perf_counter() - begin) * 1000.0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--primary_cfg", required=True)
    parser.add_argument("--primary_ckpt", required=True)
    parser.add_argument("--expert_cfg", required=True)
    parser.add_argument("--expert_ckpt", required=True)
    parser.add_argument("--samples", type=int, default=12)
    parser.add_argument("--warmup", type=int, default=3)
    parser.add_argument("--workers", type=int, default=0)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    torch.cuda.set_device(0)
    torch.backends.cudnn.benchmark = False
    primary_cfg = load_cfg(args.primary_cfg)
    expert_cfg = load_cfg(args.expert_cfg)
    configure_candidate_rich_output(primary_cfg)
    configure_candidate_rich_output(expert_cfg)
    logger = common_utils.create_logger()
    dataset, loader, _ = build_dataloader(
        dataset_cfg=primary_cfg.DATA_CONFIG,
        class_names=primary_cfg.CLASS_NAMES,
        batch_size=1,
        dist=False,
        workers=args.workers,
        training=False,
        logger=logger,
    )
    primary = build_network(primary_cfg.MODEL, len(primary_cfg.CLASS_NAMES), dataset)
    expert = build_network(expert_cfg.MODEL, len(expert_cfg.CLASS_NAMES), dataset)
    primary.load_params_from_file(filename=args.primary_ckpt, logger=logger, to_cpu=False)
    expert.load_params_from_file(filename=args.expert_ckpt, logger=logger, to_cpu=False)
    primary.cuda().eval()
    expert.cuda().eval()
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()

    rows = []
    iterator = iter(loader)
    total_needed = args.warmup + args.samples
    for idx in range(total_needed):
        raw = next(iterator)
        batch_primary = copy.deepcopy(raw)
        batch_expert = copy.deepcopy(raw)
        torch.cuda.synchronize()
        start = time.perf_counter()
        load_start = time.perf_counter()
        p, p_ms = timed_forward(primary, batch_primary)
        after_primary = time.perf_counter()
        e, e_ms = timed_forward(expert, batch_expert)
        after_expert = time.perf_counter()
        _, _ = run_gate_and_vote(p, e)
        torch.cuda.synchronize()
        end = time.perf_counter()
        row = {
            "frame_id": str(raw.get("frame_id", [idx])[0]),
            "primary_box_count": int(p["pred_boxes"].shape[0]),
            "expert_box_count": int(e["pred_boxes"].shape[0]),
            "primary_count_after_residual_exclusion": max(0, int(p["pred_boxes"].shape[0]) - 50),
            "primary_forward_ms": p_ms,
            "expert_forward_ms": e_ms,
            "h2d_and_framework_ms": (after_primary - load_start) * 1000.0 - p_ms + (after_expert - after_primary) * 1000.0 - e_ms,
            "gate_vote_ms": (end - after_expert) * 1000.0,
            "total_e2e_ms": (end - start) * 1000.0,
        }
        if idx >= args.warmup:
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)

    def stats(key):
        values = np.asarray([r[key] for r in rows], dtype=np.float64)
        return {"mean_ms": float(values.mean()), "std_ms": float(values.std(ddof=1)) if len(values) > 1 else 0.0,
                "min_ms": float(values.min()), "max_ms": float(values.max())}

    peak_mb = torch.cuda.max_memory_allocated() / (1024.0 ** 2)
    result = {
        "primary_cfg": args.primary_cfg,
        "expert_cfg": args.expert_cfg,
        "primary_ckpt": args.primary_ckpt,
        "expert_ckpt": args.expert_ckpt,
        "device": torch.cuda.get_device_name(0),
        "warmup": args.warmup,
        "samples": len(rows),
        "timing": {key: stats(key) for key in ("primary_forward_ms", "expert_forward_ms", "h2d_and_framework_ms", "gate_vote_ms", "total_e2e_ms")},
        "fps_from_mean_e2e": 1000.0 / stats("total_e2e_ms")["mean_ms"],
        "peak_memory_allocated_mb": float(peak_mb),
        "scope": "same-process sequential batch-1 primary + expert + IoU gate + box voting; profiling endpoint includes H2D and Python orchestration but excludes dataset prefetch wait",
        "rows": rows,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("device", "samples", "timing", "fps_from_mean_e2e", "peak_memory_allocated_mb")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
