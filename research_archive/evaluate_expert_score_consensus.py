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
    parser.add_argument(
        '--mode',
        choices=('logit', 'geometric', 'bonus'),
        required=True,
    )
    parser.add_argument('--residual_count', type=int, default=50)
    parser.add_argument('--workers', type=int, default=1)
    parser.add_argument('--set', dest='set_cfgs', nargs=argparse.REMAINDER)
    return parser.parse_args()


def logit(prob):
    prob = np.clip(prob, 1e-5, 1.0 - 1e-5)
    return np.log(prob / (1.0 - prob))


def sigmoid(value):
    return 1.0 / (1.0 + np.exp(-value))


def calibrate(primary, expert, iou, alpha, mode):
    if mode == 'logit':
        return sigmoid(
            (1.0 - alpha) * logit(primary) + alpha * logit(expert)
        )
    if mode == 'geometric':
        return np.power(
            np.clip(primary, 1e-8, 1.0),
            1.0 - alpha,
        ) * np.power(np.clip(expert, 1e-8, 1.0), alpha)
    # A conservative consensus bonus: a weak expert cannot erase primary
    # confidence, while high score and high IoU jointly improve ranking.
    return primary * (1.0 + alpha * expert * iou)


def refresh_scores(anno, scores):
    output = dict(anno)
    output['score'] = scores.astype(np.float32)
    return output


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
    calibrated_count = 0
    for rdar_anno, expert_anno in zip(rdar_annos, expert_annos):
        boxes = np.asarray(rdar_anno['boxes_3d'], dtype=np.float32).reshape(-1, 7)
        scores = np.asarray(rdar_anno['score'], dtype=np.float32).copy()
        expert_boxes = np.asarray(
            expert_anno['boxes_3d'], dtype=np.float32
        ).reshape(-1, 7)
        expert_scores = np.asarray(
            expert_anno['score'], dtype=np.float32
        )
        primary_count = max(0, len(boxes) - args.residual_count)
        if primary_count and len(expert_boxes):
            with torch.no_grad():
                ious = iou3d_nms_utils.boxes_iou3d_gpu(
                    torch.from_numpy(boxes[:primary_count]).cuda(),
                    torch.from_numpy(expert_boxes).cuda(),
                ).cpu().numpy()
            best_expert = ious.argmax(axis=1)
            best_iou = ious[np.arange(primary_count), best_expert]
            selected = np.flatnonzero(best_iou >= args.match_iou)
            if len(selected):
                scores[selected] = calibrate(
                    scores[selected],
                    expert_scores[best_expert[selected]],
                    best_iou[selected],
                    args.alpha,
                    args.mode,
                )
                calibrated_count += len(selected)
        output_annos.append(refresh_scores(rdar_anno, scores))

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
    with output.open('wb') as stream:
        pickle.dump(output_annos, stream)
    print(f'calibrated_primary_boxes={calibrated_count}')
    print(result_str)
    print(result_dict)
    print('Evaluation done.')


if __name__ == '__main__':
    main()
