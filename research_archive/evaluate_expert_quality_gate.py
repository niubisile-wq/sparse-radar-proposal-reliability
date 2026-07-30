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


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg_file', required=True)
    parser.add_argument('--rdar', required=True)
    parser.add_argument('--expert', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--match_iou', type=float, required=True)
    parser.add_argument('--alpha', type=float, required=True)
    parser.add_argument('--iou_power', type=float, required=True)
    parser.add_argument('--unmatched_scale', type=float, required=True)
    parser.add_argument('--residual_count', type=int, default=50)
    parser.add_argument('--workers', type=int, default=1)
    parser.add_argument('--set', dest='set_cfgs', nargs=argparse.REMAINDER)
    return parser.parse_args()


def main():
    args = parse_args()
    cfg_from_yaml_file(args.cfg_file, cfg)
    if args.set_cfgs:
        cfg_from_list(args.set_cfgs, cfg)
    rdar_annos = pickle.load(Path(args.rdar).open('rb'))
    expert_annos = pickle.load(Path(args.expert).open('rb'))
    if [str(x['frame_id']) for x in rdar_annos] != [
        str(x['frame_id']) for x in expert_annos
    ]:
        raise ValueError('frame mismatch')

    output_annos = []
    matched_count = 0
    unmatched_count = 0
    for rdar_anno, expert_anno in zip(rdar_annos, expert_annos):
        boxes = np.asarray(rdar_anno['boxes_3d'], dtype=np.float32).reshape(-1, 7)
        scores = np.asarray(rdar_anno['score'], dtype=np.float32).copy()
        expert_boxes = np.asarray(
            expert_anno['boxes_3d'], dtype=np.float32
        ).reshape(-1, 7)
        expert_scores = np.asarray(expert_anno['score'], dtype=np.float32)
        primary_count = max(0, len(boxes) - args.residual_count)
        if primary_count:
            if len(expert_boxes):
                with torch.no_grad():
                    ious = iou3d_nms_utils.boxes_iou3d_gpu(
                        torch.from_numpy(boxes[:primary_count]).cuda(),
                        torch.from_numpy(expert_boxes).cuda(),
                    ).cpu().numpy()
                best_expert = ious.argmax(axis=1)
                best_iou = ious[np.arange(primary_count), best_expert]
            else:
                best_expert = np.zeros(primary_count, dtype=np.int64)
                best_iou = np.zeros(primary_count, dtype=np.float32)
            matched = best_iou >= args.match_iou
            unmatched = ~matched
            indices = np.flatnonzero(matched)
            if len(indices):
                primary_score = np.clip(scores[indices], 1e-8, 1.0)
                consensus_score = np.clip(
                    expert_scores[best_expert[indices]], 1e-8, 1.0
                )
                quality = np.power(primary_score, 1.0 - args.alpha)
                quality *= np.power(consensus_score, args.alpha)
                quality *= np.power(
                    np.clip(best_iou[indices], 1e-8, 1.0),
                    args.iou_power,
                )
                scores[indices] = quality
                matched_count += len(indices)
            scores[:primary_count][unmatched] *= args.unmatched_scale
            unmatched_count += int(unmatched.sum())
        output = dict(rdar_anno)
        output['score'] = scores.astype(np.float32)
        output_annos.append(output)

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
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open('wb') as stream:
        pickle.dump(output_annos, stream)
    print(f'matched_primary_boxes={matched_count}')
    print(f'unmatched_primary_boxes={unmatched_count}')
    print(result_str)
    print(result_dict)
    print('Evaluation done.')


if __name__ == '__main__':
    main()
