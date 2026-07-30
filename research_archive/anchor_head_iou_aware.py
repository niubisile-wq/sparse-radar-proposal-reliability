import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from ...ops.iou3d_nms import iou3d_nms_utils
from .anchor_head_template import AnchorHeadTemplate


class AnchorHeadIoUAware(AnchorHeadTemplate):
    """Anchor head with localization-quality-aware confidence ranking.

    The auxiliary branch predicts the 3D IoU of each positive decoded box.
    At inference, classification probability and predicted IoU are fused in
    probability space before NMS.  This keeps classification and localization
    supervision separate while making the final ranking localization-aware.
    """

    def __init__(self, model_cfg, input_channels, num_class, class_names,
                 grid_size, point_cloud_range,
                 predict_boxes_when_training=True, **kwargs):
        super().__init__(
            model_cfg=model_cfg,
            num_class=num_class,
            class_names=class_names,
            grid_size=grid_size,
            point_cloud_range=point_cloud_range,
            predict_boxes_when_training=predict_boxes_when_training,
        )
        self.num_anchors_per_location = sum(self.num_anchors_per_location)
        self.iou_loss_weight = float(self.model_cfg.get('IOU_LOSS_WEIGHT', 1.0))
        self.iou_fusion_alpha = float(self.model_cfg.get('IOU_FUSION_ALPHA', 0.5))

        self.conv_cls = nn.Conv2d(
            input_channels,
            self.num_anchors_per_location * self.num_class,
            kernel_size=1,
        )
        self.conv_box = nn.Conv2d(
            input_channels,
            self.num_anchors_per_location * self.box_coder.code_size,
            kernel_size=1,
        )
        self.conv_iou = nn.Conv2d(
            input_channels,
            self.num_anchors_per_location,
            kernel_size=1,
        )

        if self.model_cfg.get('USE_DIRECTION_CLASSIFIER', None) is not None:
            self.conv_dir_cls = nn.Conv2d(
                input_channels,
                self.num_anchors_per_location * self.model_cfg.NUM_DIR_BINS,
                kernel_size=1,
            )
        else:
            self.conv_dir_cls = None
        self.init_weights()

    def init_weights(self):
        pi = 0.01
        nn.init.constant_(self.conv_cls.bias, -np.log((1 - pi) / pi))
        nn.init.normal_(self.conv_box.weight, mean=0, std=0.001)
        nn.init.normal_(self.conv_iou.weight, mean=0, std=0.001)
        nn.init.constant_(self.conv_iou.bias, 0.0)

    def _get_flat_anchors(self, batch_size):
        if isinstance(self.anchors, list):
            if self.use_multihead:
                anchors = torch.cat([
                    anchor.permute(3, 4, 0, 1, 2, 5).contiguous().view(
                        -1, anchor.shape[-1]
                    )
                    for anchor in self.anchors
                ], dim=0)
            else:
                anchors = torch.cat(self.anchors, dim=-3)
        else:
            anchors = self.anchors
        return anchors.view(1, -1, anchors.shape[-1]).repeat(batch_size, 1, 1)

    def get_iou_layer_loss(self):
        box_preds = self.forward_ret_dict['box_preds']
        iou_preds = self.forward_ret_dict['iou_preds']
        reg_targets = self.forward_ret_dict['box_reg_targets']
        labels = self.forward_ret_dict['box_cls_labels']
        batch_size = int(box_preds.shape[0])
        positives = labels > 0

        anchors = self._get_flat_anchors(batch_size)
        box_preds = box_preds.view(batch_size, -1, self.box_coder.code_size)
        iou_preds = iou_preds.view(batch_size, -1)

        pred_boxes = self.box_coder.decode_torch(box_preds, anchors)
        target_boxes = self.box_coder.decode_torch(reg_targets, anchors)
        flat_pos = positives.reshape(-1)
        if not flat_pos.any():
            zero = iou_preds.sum() * 0.0
            return zero, {'rpn_loss_iou': 0.0}

        with torch.no_grad():
            aligned_iou = iou3d_nms_utils.boxes_aligned_iou3d_gpu(
                pred_boxes.reshape(-1, pred_boxes.shape[-1])[flat_pos, :7].detach(),
                target_boxes.reshape(-1, target_boxes.shape[-1])[flat_pos, :7].detach(),
            ).reshape(-1).clamp(min=0.0, max=1.0)
            # CIA-SSD/CenterHead convention: regress IoU from [0, 1] to [-1, 1].
            iou_targets = aligned_iou * 2.0 - 1.0

        positive_preds = iou_preds.reshape(-1)[flat_pos]
        iou_loss = F.smooth_l1_loss(
            positive_preds, iou_targets, reduction='mean'
        ) * self.iou_loss_weight
        return iou_loss, {'rpn_loss_iou': iou_loss.item()}

    def get_loss(self):
        base_loss, tb_dict = super().get_loss()
        iou_loss, iou_tb = self.get_iou_layer_loss()
        total_loss = base_loss + iou_loss
        tb_dict.update(iou_tb)
        tb_dict['rpn_loss'] = total_loss.item()
        return total_loss, tb_dict

    def _fuse_confidence(self, cls_preds, iou_preds):
        cls_prob = torch.sigmoid(cls_preds)
        iou_prob = ((iou_preds.clamp(min=-1.0, max=1.0) + 1.0) * 0.5)
        iou_prob = iou_prob.unsqueeze(-1)
        alpha = self.iou_fusion_alpha
        fused = cls_prob.pow(1.0 - alpha) * iou_prob.pow(alpha)
        fused = fused.clamp(min=1e-6, max=1.0 - 1e-6)
        return torch.log(fused / (1.0 - fused))

    def forward(self, data_dict):
        spatial_features_2d = data_dict['spatial_features_2d']
        cls_preds = self.conv_cls(spatial_features_2d)
        box_preds = self.conv_box(spatial_features_2d)
        iou_preds = self.conv_iou(spatial_features_2d)

        cls_preds = cls_preds.permute(0, 2, 3, 1).contiguous()
        box_preds = box_preds.permute(0, 2, 3, 1).contiguous()
        iou_preds = iou_preds.permute(0, 2, 3, 1).contiguous()
        self.forward_ret_dict['cls_preds'] = cls_preds
        self.forward_ret_dict['box_preds'] = box_preds
        self.forward_ret_dict['iou_preds'] = iou_preds

        if self.conv_dir_cls is not None:
            dir_cls_preds = self.conv_dir_cls(spatial_features_2d)
            dir_cls_preds = dir_cls_preds.permute(0, 2, 3, 1).contiguous()
            self.forward_ret_dict['dir_cls_preds'] = dir_cls_preds
        else:
            dir_cls_preds = None

        if self.training:
            self.forward_ret_dict.update(
                self.assign_targets(gt_boxes=data_dict['gt_boxes'])
            )

        if not self.training or self.predict_boxes_when_training:
            batch_cls_preds, batch_box_preds = self.generate_predicted_boxes(
                batch_size=data_dict['batch_size'],
                cls_preds=cls_preds,
                box_preds=box_preds,
                dir_cls_preds=dir_cls_preds,
            )
            batch_iou_preds = iou_preds.view(data_dict['batch_size'], -1)
            batch_cls_preds = self._fuse_confidence(
                batch_cls_preds, batch_iou_preds
            )
            data_dict['batch_cls_preds'] = batch_cls_preds
            data_dict['batch_box_preds'] = batch_box_preds
            data_dict['cls_preds_normalized'] = False

        return data_dict
