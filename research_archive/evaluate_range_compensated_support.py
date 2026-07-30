#!/usr/bin/env python3
from __future__ import annotations

import argparse
import pickle
from pathlib import Path

import numpy as np
import torch

from pcdet.config import cfg, cfg_from_list, cfg_from_yaml_file
from pcdet.datasets import build_dataloader
from pcdet.ops.roiaware_pool3d import roiaware_pool3d_utils


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg_file', required=True)
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--range_power', type=float, required=True)
    parser.add_argument('--support_scale', type=float, required=True)
    parser.add_argument('--alpha', type=float, required=True)
    parser.add_argument('--workers', type=int, default=1)
    parser.add_argument('--set', dest='set_cfgs', nargs=argparse.REMAINDER)
    return parser.parse_args()


def main():
    args = parse_args()
    cfg_from_yaml_file(args.cfg_file, cfg)
    if args.set_cfgs:
        cfg_from_list(args.set_cfgs, cfg)
    annos = pickle.load(Path(args.input).open('rb'))
    dataset, _, _ = build_dataloader(
        dataset_cfg=cfg.DATA_CONFIG,
        class_names=cfg.CLASS_NAMES,
        batch_size=1,
        dist=False,
        workers=args.workers,
        training=False,
        logger=None,
    )

    output_annos = []
    total_boxes = 0
    empty_boxes = 0
    for anno in annos:
        boxes = np.asarray(anno['boxes_3d'], dtype=np.float32).reshape(-1, 7)
        scores = np.asarray(anno['score'], dtype=np.float32).copy()
        frame_id = str(anno['frame_id'])
        points = dataset.get_pointcloud(frame_id, 'radar')
        if len(boxes):
            masks = roiaware_pool3d_utils.points_in_boxes_cpu(
                torch.from_numpy(points[:, :3]).float(),
                torch.from_numpy(boxes).float(),
            ).numpy()
            counts = masks.sum(axis=1).astype(np.float32)
            ranges = np.linalg.norm(boxes[:, :2], axis=1)
            compensated = counts * np.power(
                np.maximum(ranges, 5.0) / 20.0,
                args.range_power,
            )
            quality = 1.0 - np.exp(
                -compensated / max(args.support_scale, 1e-6)
            )
            quality = np.clip(quality, 1e-5, 1.0)
            scores = np.power(
                np.clip(scores, 1e-8, 1.0),
                1.0 - args.alpha,
            ) * np.power(quality, args.alpha)
            total_boxes += len(boxes)
            empty_boxes += int((counts == 0).sum())
        output = dict(anno)
        output['score'] = scores.astype(np.float32)
        output_annos.append(output)

    result_str, result_dict = dataset.evaluation(
        output_annos,
        cfg.CLASS_NAMES,
        eval_metric=cfg.MODEL.POST_PROCESSING.EVAL_METRIC,
    )
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open('wb') as stream:
        pickle.dump(output_annos, stream)
    print(f'total_boxes={total_boxes} empty_boxes={empty_boxes}')
    print(result_str)
    print(result_dict)
    print('Evaluation done.')


if __name__ == '__main__':
    main()
