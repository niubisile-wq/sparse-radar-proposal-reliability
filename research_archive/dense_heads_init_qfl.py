from .anchor_head_multi import AnchorHeadMulti
from .anchor_head_single import AnchorHeadSingle
from .anchor_head_iou_aware import AnchorHeadIoUAware
from .anchor_head_corner_aware import AnchorHeadCornerAware
from .anchor_head_quality_focal import AnchorHeadQualityFocal
from .anchor_head_dual_target_consensus import AnchorHeadDualTargetConsensus
from .anchor_head_template import AnchorHeadTemplate
from .point_head_box import PointHeadBox
from .point_head_simple import PointHeadSimple
from .point_intra_part_head import PointIntraPartOffsetHead
from .center_head import CenterHead
from .voxelnext_head import VoxelNeXtHead
from .transfusion_head import TransFusionHead

__all__ = {
    "AnchorHeadTemplate": AnchorHeadTemplate,
    "AnchorHeadSingle": AnchorHeadSingle,
    "AnchorHeadIoUAware": AnchorHeadIoUAware,
    "AnchorHeadCornerAware": AnchorHeadCornerAware,
    "AnchorHeadQualityFocal": AnchorHeadQualityFocal,
    "AnchorHeadDualTargetConsensus": AnchorHeadDualTargetConsensus,
    "PointIntraPartOffsetHead": PointIntraPartOffsetHead,
    "PointHeadSimple": PointHeadSimple,
    "PointHeadBox": PointHeadBox,
    "AnchorHeadMulti": AnchorHeadMulti,
    "CenterHead": CenterHead,
    "VoxelNeXtHead": VoxelNeXtHead,
    "TransFusionHead": TransFusionHead,
}
