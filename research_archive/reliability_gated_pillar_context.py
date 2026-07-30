"""Reliability-gated, geometry-aware context for sparse radar pillars.

The module keeps the original pillar representation as an identity path.  A
global context branch uses metric pillar coordinates and return density as a
positional/reliability embedding for attention queries and keys.  Its output is
mixed back through a learnable channel-wise gate initialized to 0.1, avoiding
the destructive feature replacement used by a plain PillarAttention block.
"""

import math

import torch
import torch.nn as nn


class ReliabilityGatedPillarContext(nn.Module):
    def __init__(
        self,
        model_cfg,
        input_channels,
        grid_size=None,
        voxel_size=None,
        point_cloud_range=None,
        **kwargs,
    ):
        super().__init__()
        self.model_cfg = model_cfg
        self.num_point_features = input_channels
        self.channels = int(model_cfg.get("ATTN_CHANNELS", input_channels))
        if self.channels != input_channels:
            raise ValueError(
                "ReliabilityGatedPillarContext currently requires "
                "ATTN_CHANNELS == input_channels for its identity path"
            )

        num_heads = int(model_cfg.get("NUM_HEADS", 8))
        ffn_channels = int(model_cfg.get("FFN_CHANNELS", self.channels * 2))
        dropout = float(model_cfg.get("DROPOUT", 0.0))
        max_points = float(model_cfg.get("MAX_POINTS_PER_PILLAR", 32))
        self.density_log_scale = math.log1p(max_points)

        if grid_size is None:
            raise ValueError("grid_size is required for metric positional encoding")
        grid_tensor = torch.as_tensor(grid_size, dtype=torch.float32)
        self.register_buffer(
            "grid_xy",
            grid_tensor[:2].clamp(min=1).view(1, 1, 2),
            persistent=False,
        )

        # Inputs: normalized BEV x/y and log-normalized pillar return count.
        self.position_reliability_embedding = nn.Sequential(
            nn.Linear(3, self.channels, bias=True),
            nn.GELU(),
            nn.Linear(self.channels, self.channels, bias=True),
        )
        self.attention = nn.MultiheadAttention(
            embed_dim=self.channels,
            num_heads=num_heads,
            dropout=dropout,
            batch_first=True,
        )
        self.norm1 = nn.LayerNorm(self.channels)
        self.ffn = nn.Sequential(
            nn.Linear(self.channels, ffn_channels),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(ffn_channels, self.channels),
        )
        self.norm2 = nn.LayerNorm(self.channels)

        initial_gate = float(model_cfg.get("INITIAL_RESIDUAL_GATE", 0.1))
        if not 0.0 < initial_gate < 1.0:
            raise ValueError("INITIAL_RESIDUAL_GATE must lie in (0, 1)")
        initial_logit = math.log(initial_gate / (1.0 - initial_gate))
        self.residual_gate_logits = nn.Parameter(
            torch.full((self.channels,), initial_logit)
        )

    def forward(self, batch_dict):
        pillar_features = batch_dict["pillar_features"]
        coords = batch_dict["voxel_coords"]
        point_counts = batch_dict["voxel_num_points"].to(pillar_features.dtype)
        batch_size = int(coords[:, 0].max().item()) + 1

        counts = [(coords[:, 0] == index).sum().item() for index in range(batch_size)]
        max_pillars = max(counts)
        padded = pillar_features.new_zeros(
            (batch_size, max_pillars, self.channels)
        )
        geometry = pillar_features.new_zeros((batch_size, max_pillars, 3))
        padding_mask = torch.ones(
            (batch_size, max_pillars),
            dtype=torch.bool,
            device=pillar_features.device,
        )

        grid_xy = self.grid_xy.to(device=pillar_features.device)
        for batch_index, count in enumerate(counts):
            selected = coords[:, 0] == batch_index
            padded[batch_index, :count] = pillar_features[selected]

            xy = torch.stack(
                [
                    coords[selected, 3].to(pillar_features.dtype),
                    coords[selected, 2].to(pillar_features.dtype),
                ],
                dim=-1,
            )
            xy = 2.0 * ((xy + 0.5) / grid_xy.squeeze(0)) - 1.0
            density = (
                torch.log1p(point_counts[selected])
                / max(self.density_log_scale, 1e-6)
            ).clamp(0.0, 1.0)
            geometry[batch_index, :count, :2] = xy
            geometry[batch_index, :count, 2] = density
            padding_mask[batch_index, :count] = False

        embedding = self.position_reliability_embedding(geometry)
        query_key = padded + embedding
        attention_output, _ = self.attention(
            query_key,
            query_key,
            padded,
            key_padding_mask=padding_mask,
            need_weights=False,
        )
        context = self.norm1(padded + attention_output)
        context = self.norm2(context + self.ffn(context))

        gate = torch.sigmoid(self.residual_gate_logits).view(1, 1, -1)
        mixed = padded + gate * (context - padded)
        batch_dict["pillar_features"] = torch.cat(
            [mixed[index, :count] for index, count in enumerate(counts)],
            dim=0,
        )
        return batch_dict
