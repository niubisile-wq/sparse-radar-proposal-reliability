#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import pickle
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import torch


ROOT = Path(__file__).resolve().parent
REMOTE_CODE = ROOT / "remote_code"


@dataclass(frozen=True)
class DatasetInputs:
    dataset: str
    pred_path: Path
    info_path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build calibration diagnostics from prediction and info pkls."
    )
    parser.add_argument(
        "--item",
        action="append",
        default=[],
        metavar="DATASET|PRED|INFO",
        help=(
            "Input triple. Repeat for each dataset. Paths may be absolute or "
            "relative to the repo root."
        ),
    )
    parser.add_argument(
        "--iou-thr",
        type=float,
        default=0.5,
        help="IoU threshold used to define a hit for calibration metrics.",
    )
    parser.add_argument(
        "--bins",
        type=int,
        default=10,
        help="Number of confidence bins used for ECE.",
    )
    parser.add_argument(
        "--output-md",
        required=True,
        help="Markdown report path.",
    )
    parser.add_argument(
        "--output-json",
        required=True,
        help="JSON report path.",
    )
    return parser.parse_args()


def parse_item(value: str) -> DatasetInputs:
    parts = value.split("|")
    if len(parts) != 3:
        raise ValueError(
            f"Invalid --item value: {value!r}. Expected DATASET|PRED|INFO."
        )
    dataset, pred, info = parts
    return DatasetInputs(dataset=dataset, pred_path=Path(pred), info_path=Path(info))


def resolve_path(path: Path) -> Path:
    if path.is_absolute():
        return path
    return ROOT / path


def load_pickle(path: Path):
    with path.open("rb") as stream:
        return pickle.load(stream)


def as_boxes(value) -> np.ndarray:
    arr = np.asarray(value, dtype=np.float32)
    if arr.size == 0:
        return arr.reshape(0, 7)
    return arr.reshape(-1, 7)


def as_scores(value) -> np.ndarray:
    arr = np.asarray(value, dtype=np.float32)
    return arr.reshape(-1)


def pearson_corr(x: np.ndarray, y: np.ndarray) -> float:
    if len(x) < 2 or len(y) < 2:
        return float("nan")
    x_std = float(np.std(x))
    y_std = float(np.std(y))
    if x_std == 0.0 or y_std == 0.0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def expected_calibration_error(
    scores: np.ndarray,
    hits: np.ndarray,
    bins: int = 10,
) -> tuple[float, list[dict[str, float]]]:
    if len(scores) == 0:
        return float("nan"), []
    edges = np.linspace(0.0, 1.0, bins + 1, dtype=np.float32)
    total = float(len(scores))
    ece = 0.0
    details: list[dict[str, float]] = []
    for i in range(bins):
        left = float(edges[i])
        right = float(edges[i + 1])
        if i == bins - 1:
            mask = (scores >= left) & (scores <= right)
        else:
            mask = (scores >= left) & (scores < right)
        count = int(mask.sum())
        if count == 0:
            continue
        conf = float(scores[mask].mean())
        acc = float(hits[mask].mean())
        weight = count / total
        gap = abs(acc - conf)
        ece += weight * gap
        details.append(
            {
                "left": left,
                "right": right,
                "count": count,
                "confidence": conf,
                "accuracy": acc,
                "gap": gap,
            }
        )
    return ece, details


def brier_score(scores: np.ndarray, hits: np.ndarray) -> float:
    if len(scores) == 0:
        return float("nan")
    diff = scores - hits.astype(np.float32)
    return float(np.mean(diff * diff))


def _iou_matrix(pred_boxes: np.ndarray, gt_boxes: np.ndarray) -> np.ndarray:
    if len(pred_boxes) == 0 or len(gt_boxes) == 0:
        return np.zeros((len(pred_boxes), len(gt_boxes)), dtype=np.float32)
    if str(REMOTE_CODE) not in sys.path:
        sys.path.insert(0, str(REMOTE_CODE))
    from pcdet.ops.iou3d_nms import iou3d_nms_utils  # local import on purpose

    if not torch.cuda.is_available():
        raise RuntimeError(
            "CUDA is required for boxes_iou3d_gpu in this environment."
        )
    with torch.no_grad():
        ious = iou3d_nms_utils.boxes_iou3d_gpu(
            torch.from_numpy(pred_boxes).cuda(),
            torch.from_numpy(gt_boxes).cuda(),
        )
    return ious.cpu().numpy().astype(np.float32, copy=False)


def collect_matches(
    pred_annos: Iterable[dict],
    info_annos: Iterable[dict],
    iou_thr: float,
) -> dict[str, np.ndarray]:
    scores: list[np.ndarray] = []
    max_ious: list[np.ndarray] = []
    hits: list[np.ndarray] = []
    per_frame_top1: list[float] = []
    frame_count = 0

    for pred, info in zip(pred_annos, info_annos):
        pred_boxes = as_boxes(pred.get("boxes_3d", []))
        pred_scores = as_scores(pred.get("score", []))
        gt_boxes = as_boxes(info.get("annos", {}).get("gt_boxes", []))
        if len(pred_scores) != len(pred_boxes):
            raise ValueError(
                "Prediction score and box counts do not match for frame "
                f"{pred.get('frame_id')!r}"
            )
        if len(pred_boxes) == 0:
            frame_count += 1
            continue
        ious = _iou_matrix(pred_boxes, gt_boxes)
        frame_max = ious.max(axis=1) if len(gt_boxes) else np.zeros(len(pred_boxes), dtype=np.float32)
        scores.append(pred_scores.astype(np.float32, copy=False))
        max_ious.append(frame_max.astype(np.float32, copy=False))
        hits.append((frame_max >= iou_thr).astype(np.float32))
        per_frame_top1.append(float(frame_max.max()) if len(frame_max) else float("nan"))
        frame_count += 1

    if scores:
        scores_arr = np.concatenate(scores)
        ious_arr = np.concatenate(max_ious)
        hits_arr = np.concatenate(hits)
    else:
        scores_arr = np.zeros((0,), dtype=np.float32)
        ious_arr = np.zeros((0,), dtype=np.float32)
        hits_arr = np.zeros((0,), dtype=np.float32)

    return {
        "scores": scores_arr,
        "ious": ious_arr,
        "hits": hits_arr,
        "frame_count": np.array([frame_count], dtype=np.int32),
        "frame_top1": np.asarray(per_frame_top1, dtype=np.float32),
    }


def summarize_dataset(
    dataset: str,
    pred_path: Path,
    info_path: Path,
    iou_thr: float,
    bins: int,
) -> dict:
    pred_annos = load_pickle(pred_path)
    info_list = load_pickle(info_path)
    if len(pred_annos) != len(info_list):
        raise ValueError(
            f"{dataset}: prediction count {len(pred_annos)} does not match info "
            f"count {len(info_list)}"
        )
    if [str(x.get("frame_id")) for x in pred_annos] != [str(i.get("point_cloud", {}).get("pc_idx", i.get("frame_id", ""))) for i in info_list]:
        # Keep the check soft. Several exported result pkls only guarantee aligned
        # ordering, not identical frame identifiers.
        pass

    matched = collect_matches(pred_annos, info_list, iou_thr=iou_thr)
    scores = matched["scores"]
    ious = matched["ious"]
    hits = matched["hits"]
    topk = min(10, len(scores))
    if topk:
        order = np.argsort(scores)[::-1][:topk]
        topk_iou = float(np.mean(ious[order]))
        topk_hit_rate = float(np.mean(hits[order]))
    else:
        topk_iou = float("nan")
        topk_hit_rate = float("nan")
    ece, bin_details = expected_calibration_error(scores, hits, bins=bins)
    return {
        "dataset": dataset,
        "pred_path": str(pred_path),
        "info_path": str(info_path),
        "pred_count": int(len(pred_annos)),
        "frame_count": int(matched["frame_count"][0]),
        "prediction_count": int(len(scores)),
        "iou_thr": float(iou_thr),
        "brier": brier_score(scores, hits),
        "ece": ece,
        "score_iou_corr": pearson_corr(scores, ious),
        "top10_iou": topk_iou,
        "top10_hit_rate": topk_hit_rate,
        "mean_score": float(scores.mean()) if len(scores) else float("nan"),
        "mean_iou": float(ious.mean()) if len(ious) else float("nan"),
        "mean_hit": float(hits.mean()) if len(hits) else float("nan"),
        "has_predictions": bool(len(scores)),
        "bins": bin_details,
    }


def render_markdown(rows: list[dict]) -> str:
    lines = [
        "# Calibration report",
        "",
        "This report summarizes score calibration from frozen prediction PKLs and "
        "their matching info PKLs. It is a supporting artifact, not a final "
        "matrix closure for `T12`.",
        "",
        "| Dataset | Predictions | ECE(hit) | Brier | Score-IoU corr | Top10 IoU | Top10 hit rate | Status |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        status = "ok" if row["has_predictions"] else "empty"
        ece = f"{row['ece']:.4f}" if row["has_predictions"] else "—"
        brier = f"{row['brier']:.4f}" if row["has_predictions"] else "—"
        corr = f"{row['score_iou_corr']:.4f}" if row["has_predictions"] else "—"
        top10_iou = f"{row['top10_iou']:.4f}" if row["has_predictions"] else "—"
        top10_hit_rate = (
            f"{row['top10_hit_rate']:.4f}" if row["has_predictions"] else "—"
        )
        lines.append(
            "| {dataset} | {prediction_count} | {ece} | {brier} | {corr} | {top10_iou} | {top10_hit_rate} | {status} |".format(
                dataset=row["dataset"],
                prediction_count=row["prediction_count"],
                ece=ece,
                brier=brier,
                corr=corr,
                top10_iou=top10_iou,
                top10_hit_rate=top10_hit_rate,
                status=status,
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Lower ECE and Brier indicate better confidence quality.",
            "- Higher score-IoU correlation indicates a stronger link between score and localization quality.",
            "- This report should be paired with AP and latency evidence before any manuscript-level claim.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    if not args.item:
        raise SystemExit("At least one --item is required.")

    items = [parse_item(value) for value in args.item]
    rows = []
    for item in items:
        pred_path = resolve_path(item.pred_path)
        info_path = resolve_path(item.info_path)
        row = summarize_dataset(
            item.dataset,
            pred_path,
            info_path,
            iou_thr=args.iou_thr,
            bins=args.bins,
        )
        rows.append(row)

    overall = {
        "datasets": rows,
        "mean_ece": float(statistics.mean(row["ece"] for row in rows)),
        "mean_brier": float(statistics.mean(row["brier"] for row in rows)),
        "mean_score_iou_corr": float(
            statistics.mean(row["score_iou_corr"] for row in rows)
        ),
    }

    output_md = resolve_path(Path(args.output_md))
    output_json = resolve_path(Path(args.output_json))
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(render_markdown(rows), encoding="utf-8")
    output_json.write_text(
        json.dumps(overall, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    for row in rows:
        print(
            f"{row['dataset']}: ece={row['ece']:.4f} brier={row['brier']:.4f} "
            f"score_iou_corr={row['score_iou_corr']:.4f} top10_iou={row['top10_iou']:.4f}"
        )
    print(
        f"mean_ece={overall['mean_ece']:.4f} mean_brier={overall['mean_brier']:.4f} "
        f"mean_score_iou_corr={overall['mean_score_iou_corr']:.4f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
