import torch
from easydict import EasyDict

from pcdet.models.backbones_3d.vfe.pillar_vfe import PillarVFE


common = dict(
    USE_NORM=True,
    WITH_DISTANCE=False,
    USE_ABSLOTE_XYZ=True,
    USE_VELOCITY_DECOMPOSITION=True,
    VELOCITY_COMP_INDEX=4,
    RCS_INDEX=3,
    NUM_FILTERS=[64],
)
pvd = PillarVFE(
    EasyDict(common),
    num_point_features=5,
    voxel_size=[0.25, 0.25, 5.0],
    point_cloud_range=[0, -25, -3, 60, 25, 2],
)
drav = PillarVFE(
    EasyDict(
        **common,
        USE_DOPPLER_RELIABILITY_GATE=True,
        DOPPLER_GATE_HIDDEN=16,
        DOPPLER_GATE_MAX_RANGE=60.0,
        DOPPLER_GATE_RCS_SCALE=20.0,
        DOPPLER_GATE_VELOCITY_SCALE=10.0,
        DOPPLER_GATE_DISPERSION_SCALE=5.0,
    ),
    num_point_features=5,
    voxel_size=[0.25, 0.25, 5.0],
    point_cloud_range=[0, -25, -3, 60, 25, 2],
)
missing, unexpected = drav.load_state_dict(pvd.state_dict(), strict=False)

voxels = torch.randn(3, 4, 5)
voxels[:, :, 0] = voxels[:, :, 0].abs() * 20.0 + 1.0
counts = torch.tensor([4, 3, 2])
coords = torch.tensor([[0, 0, 4, 8], [0, 0, 20, 40], [0, 0, 60, 120]])
batch = {
    "voxels": voxels,
    "voxel_num_points": counts,
    "voxel_coords": coords,
}
pvd.eval()
drav.eval()
with torch.no_grad():
    pvd_output = pvd(dict(batch))["pillar_features"]
    drav_output = drav(dict(batch))["pillar_features"]
max_difference = float((pvd_output - drav_output).abs().max())

drav.train()
training_output = drav(dict(batch))["pillar_features"]
training_output.square().mean().backward()
gate_gradient = drav.doppler_reliability_gate[-1].weight.grad
print(
    "missing=", missing,
    "unexpected=", unexpected,
    "initial_max_difference=", max_difference,
    "finite_output=", bool(torch.isfinite(training_output).all()),
    "finite_gate_gradient=", bool(torch.isfinite(gate_gradient).all()),
    "gate_gradient_norm=", float(gate_gradient.norm()),
)
