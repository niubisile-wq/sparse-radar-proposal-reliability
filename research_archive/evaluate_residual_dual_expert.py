#!/usr/bin/env python3
from __future__ import annotations

import argparse
import pickle
from pathlib import Path

import numpy as np
import torch

from pcdet.config import cfg, cfg_from_list, cfg_from_yaml_file
from pcdet.datasets import build_dataloader
from pcdet.ops.iou3d_nms import iou3d_nms_utils


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cfg_file", required=True)
    parser.add_argument("--primary", required=True)
    parser.add_argument("--residual", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--match_iou", type=float, default=0.10)
    parser.add_argument("--residual_topk", type=int, default=50)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--set", dest="set_cfgs", nargs=argparse.REMAINDER)
    return parser.parse_args()


def fused_box(primary: np.ndarray, residual: np.ndarray, p_score: float, r_score: float) -> np.ndarray:
    weights = np.asarray([max(p_score, 1e-6), max(r_score, 1e-6)], dtype=np.float64)
    weights /= weights.sum()
    result = weights[0] * primary.astype(np.float64) + weights[1] * residual.astype(np.float64)

    # A 3D box heading is pi-periodic. Average in doubled-angle space so
    # equivalent headings near 0 and pi do not cancel each other.
    angles = np.asarray([primary[6], residual[6]], dtype=np.float64)
    sin_value = np.sum(weights * np.sin(2.0 * angles))
    cos_value = np.sum(weights * np.cos(2.0 * angles))
    result[6] = 0.5 * np.arctan2(sin_value, cos_value)
    return result.astype(np.float32)


def build_annotation(frame_id, boxes: np.ndarray, scores: np.ndarray) -> dict:
    count = boxes.shape[0]
    return {
        "name": np.full(count, "Car", dtype="<U3"),
        "score": scores.astype(np.float32),
        "boxes_3d": boxes.astype(np.float32),
        "frame_id": frame_id,
        "truncated": np.zeros(count, dtype=np.float32),
        "occluded": np.zeros(count, dtype=np.float32),
        "alpha": np.zeros(count, dtype=np.float32),
        "bbox": np.zeros((count, 4), dtype=np.float32),
        "dimensions": boxes[:, 3:6].astype(np.float32),
        "location": boxes[:, :3].astype(np.float32),
        "rotation_y": boxes[:, 6].astype(np.float32),
    }


def main() -> None:
    args = parse_args()
    cfg_from_yaml_file(args.cfg_file, cfg)
    if args.set_cfgs:
        cfg_from_list(args.set_cfgs, cfg)

    with Path(args.primary).open("rb") as stream:
        primary_annos = pickle.load(stream)
    with Path(args.residual).open("rb") as stream:
        residual_annos = pickle.load(stream)
    if len(primary_annos) != len(residual_annos):
        raise ValueError("The two experts produced a different number of frames")

    primary_ids = [str(anno["frame_id"]) for anno in primary_annos]
    residual_ids = [str(anno["frame_id"]) for anno in residual_annos]
    if primary_ids != residual_ids:
        raise ValueError("Frame order differs between the two experts")

    all_primary_scores = np.concatenate(
        [np.asarray(anno["score"], dtype=np.float32) for anno in primary_annos]
    )
    positive_scores = all_primary_scores[all_primary_scores > 0]
    if not positive_scores.size:
        raise ValueError("Primary expert produced no positive scores")
    residual_ceiling = float(positive_scores.min()) * 0.5

    output_annos = []
    matched_count = 0
    residual_count = 0
    for primary_anno, residual_anno in zip(primary_annos, residual_annos):
        p_boxes = np.asarray(primary_anno["boxes_3d"], dtype=np.float32).reshape(-1, 7)
        p_scores = np.asarray(primary_anno["score"], dtype=np.float32).reshape(-1)
        r_boxes = np.asarray(residual_anno["boxes_3d"], dtype=np.float32).reshape(-1, 7)
        r_scores = np.asarray(residual_anno["score"], dtype=np.float32).reshape(-1)
        if args.residual_topk > 0 and len(r_scores) > args.residual_topk:
            keep = np.argsort(-r_scores, kind="stable")[: args.residual_topk]
            r_boxes = r_boxes[keep]
            r_scores = r_scores[keep]

        additions = []
        if len(r_boxes):
            if len(p_boxes):
                with torch.no_grad():
                    ious = iou3d_nms_utils.boxes_iou3d_gpu(
                        torch.from_numpy(r_boxes).cuda(),
                        torch.from_numpy(p_boxes).cuda(),
                    ).cpu().numpy()
                best_primary = ious.argmax(axis=1)
                best_iou = ious[np.arange(len(r_boxes)), best_primary]
            else:
                best_primary = np.zeros(len(r_boxes), dtype=np.int64)
                best_iou = np.zeros(len(r_boxes), dtype=np.float32)

            for index, residual_box in enumerate(r_boxes):
                if len(p_boxes) and best_iou[index] >= args.match_iou:
                    primary_index = int(best_primary[index])
                    additions.append(
                        fused_box(
                            p_boxes[primary_index],
                            residual_box,
                            float(p_scores[primary_index]),
                            float(r_scores[index]),
                        )
                    )
                    matched_count += 1
                else:
                    additions.append(residual_box)
                residual_count += 1

        if additions:
            addition_boxes = np.asarray(additions, dtype=np.float32).reshape(-1, 7)
            max_residual_score = max(float(r_scores.max()), 1e-12)
            addition_scores = residual_ceiling * (
                0.5 + 0.5 * r_scores / max_residual_score
            )
            boxes = np.concatenate([p_boxes, addition_boxes], axis=0)
            scores = np.concatenate([p_scores, addition_scores.astype(np.float32)])
        else:
            boxes, scores = p_boxes, p_scores
        output_annos.append(build_annotation(primary_anno["frame_id"], boxes, scores))

    dataset, _, _ = build_dataloader(
        dataset_cfg=cfg.DATA_CONFIG,
        class_names=cfg.CLASS_NAMES,
        batch_size=1,
        dist=False,
        workers=args.workers,
        training=False,
        logger=None,
    )
    result_str, result_dict = dataset.evaluation(
        output_annos,
        cfg.CLASS_NAMES,
        eval_metric=cfg.MODEL.POST_PROCESSING.EVAL_METRIC,
    )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as stream:
        pickle.dump(output_annos, stream)
    print(f"residual_boxes={residual_count} matched_boxes={matched_count}")
    print(result_str)
    print(result_dict)
    print("Evaluation done.")


if __name__ == "__main__":
    main()
