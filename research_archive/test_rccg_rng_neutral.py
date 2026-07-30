import torch
from easydict import EasyDict

from pcdet.models.backbones_2d.base_bev_backbone import BaseBEVBackbone


def make_cfg(enabled):
    return EasyDict(
        {
            "LAYER_NUMS": [1, 1, 1],
            "LAYER_STRIDES": [2, 2, 2],
            "NUM_FILTERS": [16, 32, 64],
            "UPSAMPLE_STRIDES": [1, 2, 4],
            "NUM_UPSAMPLE_FILTERS": [32, 32, 32],
            "USE_BEV_ATTENTION": False,
            "USE_RADAR_CHANNEL_CONTRAST_GATE": enabled,
            "RADAR_CHANNEL_GATE_REDUCTION": 8,
            "RADAR_CHANNEL_GATE_INIT_SCALE": 0.0,
        }
    )


def build(enabled):
    torch.manual_seed(2028)
    backbone = BaseBEVBackbone(make_cfg(enabled), input_channels=8)
    downstream_head = torch.nn.Conv2d(backbone.num_bev_features, 6, 1)
    return backbone, downstream_head


baseline, baseline_head = build(False)
candidate, candidate_head = build(True)

head_delta = max(
    (left - right).abs().max().item()
    for left, right in zip(baseline_head.state_dict().values(), candidate_head.state_dict().values())
)
common_delta = max(
    (baseline.state_dict()[name] - value).abs().max().item()
    for name, value in candidate.state_dict().items()
    if name in baseline.state_dict()
)

baseline.eval()
candidate.eval()
x = torch.randn(2, 8, 40, 40)
baseline_out = baseline({"spatial_features": x.clone()})["spatial_features_2d"]
candidate_out = candidate({"spatial_features": x.clone()})["spatial_features_2d"]
identity_delta = (baseline_out - candidate_out).abs().max().item()

candidate.train()
loss = candidate({"spatial_features": x.clone()})["spatial_features_2d"].square().mean()
loss.backward()
scale_grad = candidate.radar_channel_contrast_gate.residual_scale.grad.abs().item()

assert common_delta == 0.0, common_delta
assert head_delta == 0.0, head_delta
assert identity_delta == 0.0, identity_delta
assert scale_grad > 0.0, scale_grad
print(
    "RCCG_RNG_NEUTRAL_OK "
    f"common_delta={common_delta:.1f} "
    f"head_delta={head_delta:.1f} "
    f"identity_delta={identity_delta:.1f} "
    f"scale_grad={scale_grad:.6g}"
)
