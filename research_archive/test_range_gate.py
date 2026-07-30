import torch

from pcdet.models.backbones_2d.base_bev_backbone import RangeAwareSpatialGate


module = RangeAwareSpatialGate(kernel_size=7, init_scale=0.1)
features = torch.randn(2, 64, 20, 24)
result = module(features)
assert result.shape == features.shape
assert torch.isfinite(result).all()
assert not torch.equal(result, features)
print("RANGE_GATE_FORWARD_OK", tuple(result.shape), float(module.residual_scale.tanh()))
