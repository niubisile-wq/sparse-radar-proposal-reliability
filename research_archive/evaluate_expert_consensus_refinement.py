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
    parser.add_argument('--beta', type=float, required=True)
    parser.add_argument('--residual_count', type=int, default=50)
    parser.add_argument('--workers', type=int, default=1)
    parser.add_argument('--set', dest='set_cfgs', nargs=argparse.REMAINDER)
    return parser.parse_args()


def interpolate_box(primary, expert, beta):
    result = primary.copy().astype(np.float64)
    result[:6] = (1.0 - beta) * primary[:6] + beta * expert[:6]
    result[6] = 0.5 * np.arctan2(
        (1.0 - beta) * np.sin(2.0 * primary[6])
        + beta * np.sin(2.0 * expert[6]),
        (1.0 - beta) * np.cos(2.0 * primary[6])
        + beta * np.cos(2.0 * expert[6]),
    )
    return result.astype(np.float32)


def refresh(anno, boxes):
    output = dict(anno)
    output['boxes_3d'] = boxes
    output['dimensions'] = boxes[:, 3:6].copy()
    output['location'] = boxes[:, :3].copy()
    output['rotation_y'] = boxes[:, 6].copy()
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
    refined_count = 0
    for rdar_anno, expert_anno in zip(rdar_annos, expert_annos):
        boxes = np.asarray(rdar_anno['boxes_3d'], dtype=np.float32).reshape(-1, 7)
        expert_boxes = np.asarray(
            expert_anno['boxes_3d'], dtype=np.float32
        ).reshape(-1, 7)
        primary_count = max(0, len(boxes) - args.residual_count)
        refined = boxes.copy()
        if primary_count and len(expert_boxes):
            with torch.no_grad():
                ious = iou3d_nms_utils.boxes_iou3d_gpu(
                    torch.from_numpy(boxes[:primary_count]).cuda(),
                    torch.from_numpy(expert_boxes).cuda(),
                ).cpu().numpy()
            best_expert = ious.argmax(axis=1)
            best_iou = ious[np.arange(primary_count), best_expert]
            for index in np.flatnonzero(best_iou >= args.match_iou):
                refined[index] = interpolate_box(
                    boxes[index],
                    expert_boxes[best_expert[index]],
                    args.beta,
                )
                refined_count += 1
        output_annos.append(refresh(rdar_anno, refined))

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
    pickle.dump(output_annos, output.open('wb'))
    print(f'refined_primary_boxes={refined_count}')
    print(result_str)
    print(result_dict)
    print('Evaluation done.')


if __name__ == '__main__':
    main()
