import torch
import torch.nn as nn

from .anchor_head_quality_focal import AnchorHeadQualityFocal


class AnchorHeadDualTargetConsensus(AnchorHeadQualityFocal):
    """Decouple objectness preservation from localization-quality ranking.

    The quality branch uses the residual IoU target inherited from
    ``AnchorHeadQualityFocal``.  A second branch keeps the original binary
    objectness objective.  Their probabilities are fused geometrically at
    inference, so a box must be supported by both semantic/object evidence
    and localization quality without forcing the two targets into one logit.
    """

    def __init__(
        self,
        model_cfg,
        input_channels,
        num_class,
        class_names,
        grid_size,
        point_cloud_range,
        predict_boxes_when_training=True,
        **kwargs,
    ):
        super().__init__(
            model_cfg=model_cfg,
            input_channels=input_channels,
            num_class=num_class,
            class_names=class_names,
            grid_size=grid_size,
            point_cloud_range=point_cloud_range,
            predict_boxes_when_training=predict_boxes_when_training,
            **kwargs,
        )
        self.objectness_loss_weight = float(
            self.model_cfg.get("OBJECTNESS_LOSS_WEIGHT", 0.5)
        )
        self.quality_fusion_alpha = float(
            self.model_cfg.get("QUALITY_FUSION_ALPHA", 0.5)
        )
        self.conv_objectness = nn.Conv2d(
            input_channels,
            self.num_anchors_per_location * self.num_class,
            kernel_size=1,
        )
        # Match the prior of the standard classification head.
        nn.init.constant_(self.conv_objectness.bias, self.conv_cls.bias[0].item())

    def get_objectness_layer_loss(self):
        objectness_preds = self.forward_ret_dict["objectness_preds"]
        labels = self.forward_ret_dict["box_cls_labels"]
        batch_size = int(objectness_preds.shape[0])

        cared = labels >= 0
        positives = labels > 0
        negatives = labels == 0
        weights = (positives.float() + negatives.float())
        weights /= torch.clamp(
            positives.sum(1, keepdim=True).float(), min=1.0
        )

        targets = torch.zeros(
            *list(labels.shape),
            self.num_class + 1,
            dtype=objectness_preds.dtype,
            device=objectness_preds.device,
        )
        safe_labels = (labels * cared.type_as(labels)).long()
        targets.scatter_(-1, safe_labels.unsqueeze(-1), 1.0)
        targets = targets[..., 1:]

        logits = objectness_preds.view(batch_size, -1, self.num_class)
        loss = self.cls_loss_func(logits, targets, weights=weights).sum()
        loss = loss / batch_size
        loss *= (
            self.model_cfg.LOSS_CONFIG.LOSS_WEIGHTS["cls_weight"]
            * self.objectness_loss_weight
        )
        return loss, {"rpn_loss_objectness": loss.item()}

    def get_loss(self):
        quality_loss, tb_dict = self.get_cls_layer_loss()
        objectness_loss, obj_tb = self.get_objectness_layer_loss()
        box_loss, box_tb = self.get_box_reg_layer_loss()
        total_loss = quality_loss + objectness_loss + box_loss
        tb_dict.update(obj_tb)
        tb_dict.update(box_tb)
        tb_dict["rpn_loss"] = total_loss.item()
        return total_loss, tb_dict

    def _fuse_logits(self, quality_logits, objectness_logits):
        quality_prob = torch.sigmoid(quality_logits)
        objectness_prob = torch.sigmoid(objectness_logits)
        alpha = self.quality_fusion_alpha
        fused = quality_prob.pow(alpha) * objectness_prob.pow(1.0 - alpha)
        fused = fused.clamp(min=1e-6, max=1.0 - 1e-6)
        return torch.log(fused / (1.0 - fused))

    def forward(self, data_dict):
        # The parent constructs quality logits, boxes, targets and decoded
        # predictions.  Replace only the confidence used downstream.
        spatial_features_2d = data_dict["spatial_features_2d"]
        objectness_preds = self.conv_objectness(spatial_features_2d)
        objectness_preds = objectness_preds.permute(0, 2, 3, 1).contiguous()
        self.forward_ret_dict["objectness_preds"] = objectness_preds

        data_dict = super().forward(data_dict)
        self.forward_ret_dict["objectness_preds"] = objectness_preds

        if not self.training or self.predict_boxes_when_training:
            quality_logits = data_dict["batch_cls_preds"]
            objectness_logits = objectness_preds.view(
                data_dict["batch_size"], -1, self.num_class
            )
            data_dict["batch_cls_preds"] = self._fuse_logits(
                quality_logits, objectness_logits
            )
            data_dict["cls_preds_normalized"] = False
        return data_dict
