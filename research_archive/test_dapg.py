import torch

from pcdet.models.backbones_3d.density_aware_pillar_gate import (
    DensityAwarePillarGate,
)


module = DensityAwarePillarGate(
    {
        "HIDDEN_CHANNELS": 32,
        "MAX_POINTS_PER_VOXEL": 32,
        "INIT_RESIDUAL_SCALE": 0.1,
    },
    input_channels=64,
)
features = torch.randn(12, 64)
batch = {
    "pillar_features": features.clone(),
    "voxel_coords": torch.tensor(
        [[0, 0, index, 0] for index in range(5)]
        + [[1, 0, index, 0] for index in range(7)]
    ),
    "voxel_num_points": torch.tensor([1, 2, 4, 8, 16, 3, 5, 7, 9, 12, 20, 32]),
}
result = module(batch)["pillar_features"]
assert result.shape == features.shape
assert torch.isfinite(result).all()
assert not torch.equal(result, features)
print("DAPG_FORWARD_OK", tuple(result.shape), float(module.residual_scale.tanh()))
