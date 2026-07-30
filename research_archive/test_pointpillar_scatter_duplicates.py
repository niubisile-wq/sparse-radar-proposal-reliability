import numpy as np
import torch
from easydict import EasyDict

from pcdet.models.backbones_2d.map_to_bev.pointpillar_scatter import PointPillarScatter


scatter = PointPillarScatter(
    EasyDict({"NUM_BEV_FEATURES": 2}), grid_size=np.array([4, 3, 1])
)
features = torch.tensor(
    [[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]], requires_grad=True
)
coords = torch.tensor(
    [
        [0, 0, 1, 2],
        [0, 0, 1, 2],
        [0, 0, 2, 3],
    ],
    dtype=torch.int32,
)
output = scatter(
    {"pillar_features": features, "voxel_coords": coords}
)["spatial_features"]

assert output.shape == (1, 2, 3, 4)
assert torch.equal(output[0, :, 1, 2], features[1])
assert torch.equal(output[0, :, 2, 3], features[2])
output.square().sum().backward()
assert features.grad is not None
assert torch.equal(features.grad[0], torch.zeros(2))
assert torch.all(features.grad[1:] != 0)
print("POINTPILLAR_DUPLICATE_SCATTER_FORWARD_BACKWARD_OK")
