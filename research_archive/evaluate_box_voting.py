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
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--vote_iou', type=float, required=True)
    parser.add_argument('--strength', type=float, required=True)
    parser.add_argument('--score_power', type=float, default=1.0)
    parser.add_argument('--only_lower_score_neighbors', action='store_true')
    parser.add_argument('--mode', choices=('xy', 'xyz', 'all'), default='all')
    parser.add_argument('--residual_count', type=int, default=50)
    parser.add_argument('--workers', type=int, default=1)
    parser.add_argument('--set', dest='set_cfgs', nargs=argparse.REMAINDER)
    return parser.parse_args()


def circular_box_mean(boxes, weights):
    weights = weights.astype(np.float64)
    weights /= max(weights.sum(), 1e-12)
    mean = np.sum(boxes.astype(np.float64) * weights[:, None], axis=0)
    mean[6] = 0.5 * np.arctan2(
        np.sum(weights * np.sin(2.0 * boxes[:, 6])),
        np.sum(weights * np.cos(2.0 * boxes[:, 6])),
    )
    return mean.astype(np.float32)


def refresh_annotation(anno, boxes):
    output = dict(anno)
    output['boxes_3d'] = boxes.astype(np.float32)
    output['dimensions'] = boxes[:, 3:6].astype(np.float32)
    output['location'] = boxes[:, :3].astype(np.float32)
    output['rotation_y'] = boxes[:, 6].astype(np.float32)
    return output


def main():
    args = parse_args()
    cfg_from_yaml_file(args.cfg_file, cfg)
    if args.set_cfgs:
        cfg_from_list(args.set_cfgs, cfg)
    with Path(args.input).open('rb') as stream:
        annos = pickle.load(stream)

    output_annos = []
    voted_boxes = 0
    neighbor_links = 0
    for anno in annos:
        boxes = np.asarray(anno['boxes_3d'], dtype=np.float32).reshape(-1, 7)
        scores = np.asarray(anno['score'], dtype=np.float32).reshape(-1)
        primary_count = max(0, len(boxes) - args.residual_count)
        refined = boxes.copy()
        if primary_count > 1:
            primary = boxes[:primary_count]
            with torch.no_grad():
                ious = iou3d_nms_utils.boxes_iou3d_gpu(
                    torch.from_numpy(primary).cuda(),
                    torch.from_numpy(primary).cuda(),
                ).cpu().numpy()
            for index in range(primary_count):
                neighbors = np.flatnonzero(ious[index] >= args.vote_iou)
                if args.only_lower_score_neighbors:
                    neighbors = neighbors[
                        scores[neighbors] <= scores[index] + 1e-12
                    ]
                if len(neighbors) <= 1:
                    continue
                weights = np.maximum(scores[neighbors], 1e-8) ** args.score_power
                consensus = circular_box_mean(primary[neighbors], weights)
                if args.mode == 'xy':
                    dims = np.asarray([0, 1])
                elif args.mode == 'xyz':
                    dims = np.asarray([0, 1, 2])
                else:
                    dims = np.arange(6)
                refined[index, dims] = (
                    (1.0 - args.strength) * primary[index, dims]
                    + args.strength * consensus[dims]
                )
                angles = np.asarray([primary[index, 6], consensus[6]])
                angle_weights = np.asarray([1.0 - args.strength, args.strength])
                refined[index, 6] = 0.5 * np.arctan2(
                    np.sum(angle_weights * np.sin(2.0 * angles)),
                    np.sum(angle_weights * np.cos(2.0 * angles)),
                )
                voted_boxes += 1
                neighbor_links += len(neighbors) - 1
        output_annos.append(refresh_annotation(anno, refined))

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
        output_annos, cfg.CLASS_NAMES,
        eval_metric=cfg.MODEL.POST_PROCESSING.EVAL_METRIC,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('wb') as stream:
        pickle.dump(output_annos, stream)
    print(f'voted_boxes={voted_boxes} neighbor_links={neighbor_links}')
    print(result_str)
    print(result_dict)
    print('Evaluation done.')


if __name__ == '__main__':
    main()
