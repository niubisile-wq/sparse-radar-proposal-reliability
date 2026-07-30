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
    parser.add_argument('--expert', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--cross_iou', type=float, required=True)
    parser.add_argument('--score_thresh', type=float, required=True)
    parser.add_argument('--score_scale', type=float, required=True)
    parser.add_argument('--max_add', type=int, default=20)
    parser.add_argument('--residual_count', type=int, default=50)
    parser.add_argument('--workers', type=int, default=1)
    parser.add_argument('--set', dest='set_cfgs', nargs=argparse.REMAINDER)
    return parser.parse_args()


def append_selected(base_anno, expert_anno, selected, score_scale):
    output = {}
    base_count = len(np.asarray(base_anno['score']))
    expert_count = len(np.asarray(expert_anno['score']))
    for key, base_value in base_anno.items():
        expert_value = expert_anno.get(key)
        if (
            isinstance(base_value, np.ndarray)
            and isinstance(expert_value, np.ndarray)
            and base_value.ndim >= 1
            and expert_value.ndim >= 1
            and len(base_value) == base_count
            and len(expert_value) == expert_count
        ):
            addition = expert_value[selected].copy()
            if key == 'score':
                addition = addition.astype(np.float32) * score_scale
            output[key] = np.concatenate((base_value, addition), axis=0)
        else:
            output[key] = base_value
    return output


def main():
    args = parse_args()
    cfg_from_yaml_file(args.cfg_file, cfg)
    if args.set_cfgs:
        cfg_from_list(args.set_cfgs, cfg)
    annos = pickle.load(Path(args.input).open('rb'))
    expert_annos = pickle.load(Path(args.expert).open('rb'))
    if [str(x['frame_id']) for x in annos] != [
        str(x['frame_id']) for x in expert_annos
    ]:
        raise ValueError('frame mismatch')

    output_annos = []
    recovered_count = 0
    for anno, expert_anno in zip(annos, expert_annos):
        boxes = np.asarray(anno['boxes_3d'], dtype=np.float32).reshape(-1, 7)
        expert_boxes = np.asarray(
            expert_anno['boxes_3d'], dtype=np.float32
        ).reshape(-1, 7)
        expert_scores = np.asarray(expert_anno['score'], dtype=np.float32)
        primary_count = max(0, len(boxes) - args.residual_count)
        if len(expert_boxes) == 0:
            output_annos.append(dict(anno))
            continue
        if primary_count:
            with torch.no_grad():
                ious = iou3d_nms_utils.boxes_iou3d_gpu(
                    torch.from_numpy(expert_boxes).cuda(),
                    torch.from_numpy(boxes[:primary_count]).cuda(),
                ).cpu().numpy()
            max_iou = ious.max(axis=1)
        else:
            max_iou = np.zeros(len(expert_boxes), dtype=np.float32)
        selected = np.flatnonzero(
            (max_iou < args.cross_iou)
            & (expert_scores >= args.score_thresh)
        )
        if len(selected) > args.max_add:
            order = np.argsort(-expert_scores[selected], kind='stable')
            selected = selected[order[:args.max_add]]
        output_annos.append(
            append_selected(anno, expert_anno, selected, args.score_scale)
        )
        recovered_count += len(selected)

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
    print(f'recovered_expert_boxes={recovered_count}')
    print(result_str)
    print(result_dict)
    print('Evaluation done.')


if __name__ == '__main__':
    main()
