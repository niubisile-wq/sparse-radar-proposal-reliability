import torch

from pcdet.models.backbones_2d.base_bev_backbone import StableSEGate2D


module = StableSEGate2D(channels=64, reduction=8, init_scale=0.1)
features = torch.randn(2, 64, 20, 24)
result = module(features)
assert result.shape == features.shape
assert torch.isfinite(result).all()
relative_change = (result - features).abs().mean() / features.abs().mean()
assert float(relative_change) < 0.1
print(
    "STABLE_BEV_GATE_FORWARD_OK",
    tuple(result.shape),
    float(module.residual_scale.tanh()),
    float(relative_change),
)
