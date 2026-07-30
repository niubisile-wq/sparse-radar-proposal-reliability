import torch

from ...utils import loss_utils
from .anchor_head_single import AnchorHeadSingle


class AnchorHeadCornerAware(AnchorHeadSingle):
    """PointPillars head with coupled 3D corner-consistency supervision."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.corner_loss_weight = float(
            self.model_cfg.get('CORNER_LOSS_WEIGHT', 1.0)
        )

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

    def get_corner_layer_loss(self):
        box_preds = self.forward_ret_dict['box_preds']
        reg_targets = self.forward_ret_dict['box_reg_targets']
        labels = self.forward_ret_dict['box_cls_labels']
        batch_size = int(box_preds.shape[0])
        positives = labels > 0
        if not positives.any():
            zero = box_preds.sum() * 0.0
            return zero, {'rpn_loss_corner': 0.0}

        anchors = self._get_flat_anchors(batch_size)
        box_preds = box_preds.view(batch_size, -1, self.box_coder.code_size)
        pred_boxes = self.box_coder.decode_torch(box_preds, anchors)
        target_boxes = self.box_coder.decode_torch(reg_targets, anchors)
        flat_pos = positives.reshape(-1)
        corner_loss = loss_utils.get_corner_loss_lidar(
            pred_boxes.reshape(-1, pred_boxes.shape[-1])[flat_pos, :7],
            target_boxes.reshape(-1, target_boxes.shape[-1])[flat_pos, :7],
        ).mean() * self.corner_loss_weight
        return corner_loss, {'rpn_loss_corner': corner_loss.item()}

    def get_loss(self):
        base_loss, tb_dict = super().get_loss()
        corner_loss, corner_tb = self.get_corner_layer_loss()
        total_loss = base_loss + corner_loss
        tb_dict.update(corner_tb)
        tb_dict['rpn_loss'] = total_loss.item()
        return total_loss, tb_dict
