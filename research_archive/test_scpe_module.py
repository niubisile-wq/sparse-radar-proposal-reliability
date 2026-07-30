import torch
from easydict import EasyDict

from pcdet.models.backbones_3d.vfe import PillarVFEPhysicalResidual


cfg = EasyDict(
    {
        "USE_NORM": True,
        "WITH_DISTANCE": False,
        "USE_ABSLOTE_XYZ": True,
        "NUM_FILTERS": [64],
        "PHYSICAL_RCS_INDEX": 3,
        "PHYSICAL_VELOCITY_INDEX": 4,
        "PHYSICAL_HIDDEN_CHANNELS": 16,
        "PHYSICAL_RESIDUAL_ALPHA": 0.25,
    }
)
module = PillarVFEPhysicalResidual(
    model_cfg=cfg,
    num_point_features=5,
    voxel_size=[0.25, 0.25, 5.0],
    point_cloud_range=[0, -25, -3, 60, 25, 2],
)
module.train()

torch.manual_seed(7)
voxels = torch.randn(4, 6, 5)
voxel_num_points = torch.tensor([6, 4, 5, 3])
coords = torch.tensor(
    [[0, 0, 1, 1], [0, 0, 2, 2], [1, 0, 1, 2], [1, 0, 2, 3]]
)
for index, count in enumerate(voxel_num_points.tolist()):
    voxels[index, count:] = 0

batch = {
    "voxels": voxels,
    "voxel_num_points": voxel_num_points,
    "voxel_coords": coords,
}
result = module(batch)["pillar_features"]
assert result.shape == (4, 64), result.shape
assert torch.isfinite(result).all()
result.sum().backward()
assert module.physical_pillar_projection.weight.grad is not None
print("SCPE_SMOKE_OK", tuple(result.shape))
