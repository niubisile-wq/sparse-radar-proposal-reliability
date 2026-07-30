import torch
import torch.nn.functional as F

from ...ops.iou3d_nms import iou3d_nms_utils
from .anchor_head_single import AnchorHeadSingle


class AnchorHeadQualityFocal(AnchorHeadSingle):
    """Single-stage anchor head with 3D-IoU soft classification targets.

    Positive classification targets are the aligned 3D IoU between the
    current decoded box and its assigned target.  Quality-focal modulation
    then trains one confidence to express both object presence and
    localization quality, avoiding a second inference branch.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quality_focal_beta = float(
            self.model_cfg.get("QUALITY_FOCAL_BETA", 2.0)
        )
        self.quality_iou_power = float(
            self.model_cfg.get("QUALITY_IOU_POWER", 1.0)
        )
        self.quality_target_floor = float(
            self.model_cfg.get("QUALITY_TARGET_FLOOR", 0.0)
        )
        self.quality_objectness_residual = float(
            self.model_cfg.get("QUALITY_OBJECTNESS_RESIDUAL", 0.0)
        )
        self.quality_binary_mix = float(
            self.model_cfg.get("QUALITY_BINARY_MIX", 0.0)
        )

    def _get_flat_anchors(self, batch_size):
        if isinstance(self.anchors, list):
            if self.use_multihead:
                anchors = torch.cat(
                    [
                        anchor.permute(3, 4, 0, 1, 2, 5)
                        .contiguous()
                        .view(-1, anchor.shape[-1])
                        for anchor in self.anchors
                    ],
                    dim=0,
                )
            else:
                anchors = torch.cat(self.anchors, dim=-3)
        else:
            anchors = self.anchors
        return anchors.view(1, -1, anchors.shape[-1]).repeat(
            batch_size, 1, 1
        )

    def get_cls_layer_loss(self):
        cls_preds = self.forward_ret_dict["cls_preds"]
        box_preds = self.forward_ret_dict["box_preds"]
        reg_targets = self.forward_ret_dict["box_reg_targets"]
        labels = self.forward_ret_dict["box_cls_labels"]
        batch_size = int(cls_preds.shape[0])

        cared = labels >= 0
        positives = labels > 0
        negatives = labels == 0
        cls_weights = (negatives.float() + positives.float())
        pos_normalizer = positives.sum(1, keepdim=True).float()
        cls_weights /= torch.clamp(pos_normalizer, min=1.0)

        logits = cls_preds.view(batch_size, -1, self.num_class)
        targets = torch.zeros_like(logits)
        flat_positive = positives.reshape(-1)
        if flat_positive.any():
            anchors = self._get_flat_anchors(batch_size)
            decoded_predictions = self.box_coder.decode_torch(
                box_preds.view(batch_size, -1, self.box_coder.code_size),
                anchors,
            )
            decoded_targets = self.box_coder.decode_torch(reg_targets, anchors)
            with torch.no_grad():
                aligned_iou = iou3d_nms_utils.boxes_aligned_iou3d_gpu(
                    decoded_predictions.reshape(
                        -1, decoded_predictions.shape[-1]
                    )[flat_positive, :7].detach(),
                    decoded_targets.reshape(-1, decoded_targets.shape[-1])[
                        flat_positive, :7
                    ].detach(),
                ).reshape(-1)
                aligned_iou = aligned_iou.clamp(0.0, 1.0)
                aligned_iou = aligned_iou.pow(self.quality_iou_power)
                if self.quality_objectness_residual > 0:
                    residual = self.quality_objectness_residual
                    aligned_iou = residual + (1.0 - residual) * aligned_iou
                if self.quality_target_floor > 0:
                    aligned_iou = aligned_iou.clamp(
                        min=self.quality_target_floor
                    )
            targets.reshape(-1, self.num_class)[flat_positive, 0] = aligned_iou

        targets *= cared.unsqueeze(-1).type_as(targets)
        probabilities = torch.sigmoid(logits)
        modulation = torch.abs(targets - probabilities).pow(
            self.quality_focal_beta
        )
        loss = F.binary_cross_entropy_with_logits(
            logits, targets, reduction="none"
        )
        loss = loss * modulation * cls_weights.unsqueeze(-1)
        cls_loss = loss.sum() / batch_size
        cls_loss *= self.model_cfg.LOSS_CONFIG.LOSS_WEIGHTS["cls_weight"]
        if self.quality_binary_mix > 0:
            quality_loss = cls_loss
            binary_loss, _ = super().get_cls_layer_loss()
            mix = self.quality_binary_mix
            cls_loss = mix * binary_loss + (1.0 - mix) * quality_loss
        return cls_loss, {"rpn_loss_cls": cls_loss.item()}
