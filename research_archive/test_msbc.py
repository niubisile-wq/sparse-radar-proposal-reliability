import torch

from pcdet.models.backbones_2d.base_bev_backbone import MultiScaleBEVContext


module = MultiScaleBEVContext(
    channels=64,
    hidden_channels=16,
    dilations=(1, 2, 4),
    init_scale=0.1,
)
features = torch.randn(2, 64, 20, 24)
result = module(features)
assert result.shape == features.shape
assert torch.isfinite(result).all()
assert not torch.equal(result, features)
print("MSBC_FORWARD_OK", tuple(result.shape), float(module.residual_scale.tanh()))
