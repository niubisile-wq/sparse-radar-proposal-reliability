import math

import torch
import torch.nn as nn


class LearnableResidualScale(nn.Module):
    """Leaf module so OpenPCDet's flattened optimizer includes the scale."""

    def __init__(self, init_scale=0.0):
        super().__init__()
        init_scale = min(max(float(init_scale), -0.99), 0.99)
        self.raw = nn.Parameter(
            torch.tensor([math.atanh(init_scale)], dtype=torch.float32)
        )

    def forward(self):
        return torch.tanh(self.raw).squeeze(0)


class DensityAwarePillarGate(nn.Module):
    """Residual pillar recalibration using local, scene, and density evidence.

    The module starts close to an identity mapping. This preserves a trained
    PointPillars representation at initialization while allowing the network
    to learn dataset-robust pillar importance without quadratic attention.
    """

    def __init__(self, model_cfg, input_channels, **kwargs):
        super().__init__()
        rng_state = torch.get_rng_state()
        self.model_cfg = model_cfg
        self.num_point_features = input_channels
        hidden_channels = int(
            self.model_cfg.get("HIDDEN_CHANNELS", max(input_channels // 2, 16))
        )
        self.max_points_per_voxel = float(
            self.model_cfg.get("MAX_POINTS_PER_VOXEL", 32)
        )
        init_scale = float(self.model_cfg.get("INIT_RESIDUAL_SCALE", 0.0))

        self.norm = nn.LayerNorm(input_channels)
        self.gate = nn.Sequential(
            nn.Linear(input_channels * 2 + 1, hidden_channels),
            nn.GELU(),
            nn.Linear(hidden_channels, input_channels),
            nn.Sigmoid(),
        )
        self.residual_scale = LearnableResidualScale(init_scale)
        torch.set_rng_state(rng_state)

    def forward(self, batch_dict):
        pillar_features = batch_dict["pillar_features"]
        coords = batch_dict["voxel_coords"]
        if pillar_features.numel() == 0:
            return batch_dict

        normalized = self.norm(pillar_features)
        batch_indices = coords[:, 0].long()
        scene_context = torch.zeros_like(normalized)
        for batch_index in torch.unique(batch_indices):
            mask = batch_indices == batch_index
            selected = torch.nonzero(mask, as_tuple=False).flatten()
            context = normalized.index_select(0, selected).mean(
                dim=0, keepdim=True
            )
            scene_context.index_copy_(0, selected, context.expand(selected.numel(), -1))

        point_counts = batch_dict.get("voxel_num_points")
        if point_counts is None:
            density = torch.ones(
                (pillar_features.shape[0], 1),
                dtype=pillar_features.dtype,
                device=pillar_features.device,
            )
        else:
            density = torch.log1p(point_counts.to(pillar_features.dtype)).unsqueeze(-1)
            density = density / math.log1p(self.max_points_per_voxel)
            density = density.clamp_(0.0, 1.0)

        gate = 2.0 * self.gate(
            torch.cat((normalized, scene_context, density), dim=-1)
        ) - 1.0
        scale = self.residual_scale()
        batch_dict["pillar_features"] = pillar_features * (1.0 + scale * gate)
        return batch_dict
