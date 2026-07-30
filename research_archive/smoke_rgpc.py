import numpy as np
import torch
from easydict import EasyDict

from pcdet.models.backbones_3d.reliability_gated_pillar_context import (
    ReliabilityGatedPillarContext,
)


config = EasyDict(
    ATTN_CHANNELS=64,
    NUM_HEADS=8,
    FFN_CHANNELS=128,
    DROPOUT=0.0,
    MAX_POINTS_PER_PILLAR=32,
    INITIAL_RESIDUAL_GATE=0.1,
)
module = ReliabilityGatedPillarContext(
    config,
    64,
    grid_size=np.array([240, 200, 1]),
)
features = torch.randn(5, 64, requires_grad=True)
batch = {
    "pillar_features": features,
    "voxel_coords": torch.tensor(
        [
            [0, 0, 1, 2],
            [0, 0, 5, 7],
            [1, 0, 3, 4],
            [1, 0, 8, 9],
            [1, 0, 2, 1],
        ]
    ),
    "voxel_num_points": torch.tensor([2, 4, 8, 16, 32]),
}
output = module(batch)["pillar_features"]
output.square().mean().backward()
print(
    "shape=", tuple(output.shape),
    "finite_output=", bool(torch.isfinite(output).all()),
    "finite_gradient=", bool(torch.isfinite(features.grad).all()),
    "gate=", float(torch.sigmoid(module.residual_gate_logits).mean()),
)
