import torch
from easydict import EasyDict

from pcdet.models.backbones_2d.base_bev_backbone import BaseBEVBackbone
from pcdet.models.backbones_3d.density_aware_pillar_gate import (
    DensityAwarePillarGate,
)
from tools.train_utils.optimization import build_optimizer


OPTIM_CFG = EasyDict(
    {
        "OPTIMIZER": "adam_onecycle",
        "LR": 0.003,
        "WEIGHT_DECAY": 0.01,
        "BETAS": (0.9, 0.99),
    }
)


def bev_cfg(candidate=None):
    cfg = {
        "LAYER_NUMS": [1, 1, 1],
        "LAYER_STRIDES": [2, 2, 2],
        "NUM_FILTERS": [16, 32, 64],
        "UPSAMPLE_STRIDES": [1, 2, 4],
        "NUM_UPSAMPLE_FILTERS": [32, 32, 32],
        "USE_BEV_ATTENTION": False,
    }
    if candidate == "msbc2":
        cfg.update(
            {
                "USE_MS_BEV_CONTEXT": True,
                "MS_BEV_HIDDEN_CHANNELS": 16,
                "MS_BEV_DILATIONS": [1, 2, 4],
                "MS_BEV_INIT_RESIDUAL_SCALE": 0.0,
            }
        )
    elif candidate == "range2":
        cfg.update(
            {
                "USE_RANGE_AWARE_SPATIAL_GATE": True,
                "RANGE_GATE_KERNEL_SIZE": 7,
                "RANGE_GATE_INIT_RESIDUAL_SCALE": 0.0,
            }
        )
    elif candidate == "sbd10":
        cfg.update({"BEV_FEATURE_DROPOUT_P": 0.10})
    return EasyDict(cfg)


def build_bev(candidate=None):
    torch.manual_seed(2028)
    backbone = BaseBEVBackbone(bev_cfg(candidate), input_channels=8)
    head = torch.nn.Conv2d(backbone.num_bev_features, 6, 1)
    return backbone, head


base, base_head = build_bev()
x = torch.randn(2, 8, 40, 40)
base.eval()
base_out = base({"spatial_features": x.clone()})["spatial_features_2d"]
for name in ("msbc2", "range2"):
    candidate, head = build_bev(name)
    candidate.eval()
    out = candidate({"spatial_features": x.clone()})["spatial_features_2d"]
    assert max(
        (left - right).abs().max().item()
        for left, right in zip(base_head.state_dict().values(), head.state_dict().values())
    ) == 0.0
    assert (base_out - out).abs().max().item() == 0.0
    scale_module = (
        candidate.ms_bev_context.residual_scale
        if name == "msbc2"
        else candidate.range_aware_spatial_gate.residual_scale
    )
    optimizer = build_optimizer(candidate, OPTIM_CFG)
    optimized = {
        id(parameter)
        for group in optimizer.opt.param_groups
        for parameter in group["params"]
    }
    assert id(scale_module.raw) in optimized
    candidate.train()
    optimizer.zero_grad()
    candidate({"spatial_features": x.clone()})[
        "spatial_features_2d"
    ].square().mean().backward()
    before = scale_module.raw.detach().clone()
    optimizer.step()
    assert not torch.equal(before, scale_module.raw.detach())

dropout_candidate, dropout_head = build_bev("sbd10")
dropout_candidate.eval()
dropout_eval = dropout_candidate({"spatial_features": x.clone()})[
    "spatial_features_2d"
]
assert max(
    (left - right).abs().max().item()
    for left, right in zip(
        base_head.state_dict().values(), dropout_head.state_dict().values()
    )
) == 0.0
assert (base_out - dropout_eval).abs().max().item() == 0.0
dropout_candidate.train()
dropout_train = dropout_candidate({"spatial_features": x.clone()})[
    "spatial_features_2d"
]
assert (base_out - dropout_train).abs().max().item() > 0.0

torch.manual_seed(2028)
dapg_base_head = torch.nn.Linear(64, 7)
torch.manual_seed(2028)
dapg = DensityAwarePillarGate(
    EasyDict(
        {
            "HIDDEN_CHANNELS": 32,
            "MAX_POINTS_PER_VOXEL": 32,
            "INIT_RESIDUAL_SCALE": 0.0,
        }
    ),
    input_channels=64,
)
dapg_head = torch.nn.Linear(64, 7)
assert max(
    (left - right).abs().max().item()
    for left, right in zip(
        dapg_base_head.state_dict().values(), dapg_head.state_dict().values()
    )
) == 0.0

pillar_features = torch.randn(12, 64, requires_grad=True)
coords = torch.zeros(12, 4, dtype=torch.int32)
coords[6:, 0] = 1
batch = {
    "pillar_features": pillar_features,
    "voxel_coords": coords,
    "voxel_num_points": torch.arange(1, 13),
}
output = dapg(batch)["pillar_features"]
assert (output - pillar_features).abs().max().item() == 0.0
output.square().mean().backward()
assert dapg.residual_scale.raw.grad.abs().item() > 0.0
optimizer = build_optimizer(dapg, OPTIM_CFG)
optimized = {
    id(parameter)
    for group in optimizer.opt.param_groups
    for parameter in group["params"]
}
assert id(dapg.residual_scale.raw) in optimized
before = dapg.residual_scale.raw.detach().clone()
optimizer.step()
assert not torch.equal(before, dapg.residual_scale.raw.detach())
print("DAPG_MSBC_RANGE_SBD_RNG_NEUTRAL_IDENTITY_OK")
