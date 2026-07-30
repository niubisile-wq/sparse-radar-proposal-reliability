import torch
import torch.nn as nn

from .pillar_vfe import PillarVFE


class PillarVFEPhysicalResidual(PillarVFE):
    """PillarVFE with a sensor-calibrated RCS/Doppler residual path.

    The ordinary geometry/attribute PFN remains unchanged.  A second path
    standardizes radar-specific attributes within each frame, encodes them
    independently, and adds a bounded, zero-initialized residual to the pillar
    feature.  Zero initialization makes the module exactly equal to PillarVFE
    at the start of optimization.
    """

    def __init__(
        self,
        model_cfg,
        num_point_features,
        voxel_size,
        point_cloud_range,
        grid_size=None,
        **kwargs,
    ):
        super().__init__(
            model_cfg=model_cfg,
            num_point_features=num_point_features,
            voxel_size=voxel_size,
            point_cloud_range=point_cloud_range,
            grid_size=grid_size,
            **kwargs,
        )
        self.physical_rcs_index = int(model_cfg.get("PHYSICAL_RCS_INDEX", 3))
        self.physical_velocity_index = int(
            model_cfg.get("PHYSICAL_VELOCITY_INDEX", 4)
        )
        self.physical_std_floor = float(model_cfg.get("PHYSICAL_STD_FLOOR", 1e-3))
        self.physical_residual_alpha = float(
            model_cfg.get("PHYSICAL_RESIDUAL_ALPHA", 0.25)
        )
        hidden = int(model_cfg.get("PHYSICAL_HIDDEN_CHANNELS", 16))
        output_channels = self.get_output_feature_dim()

        self.physical_point_encoder = nn.Sequential(
            nn.Linear(4, hidden, bias=False),
            nn.BatchNorm1d(hidden, eps=1e-3, momentum=0.01),
            nn.ReLU(inplace=True),
            nn.Linear(hidden, hidden, bias=False),
            nn.BatchNorm1d(hidden, eps=1e-3, momentum=0.01),
            nn.ReLU(inplace=True),
        )
        self.physical_pillar_projection = nn.Linear(
            hidden * 2, output_channels, bias=True
        )
        self.physical_gate = nn.Linear(output_channels * 2, output_channels)

        # Preserve the verified PillarVFE function exactly at initialization.
        nn.init.zeros_(self.physical_pillar_projection.weight)
        nn.init.zeros_(self.physical_pillar_projection.bias)
        nn.init.zeros_(self.physical_gate.weight)
        nn.init.zeros_(self.physical_gate.bias)

    def _frame_standardize(self, values, valid_mask, batch_ids):
        normalized = torch.zeros_like(values)
        for batch_id in torch.unique(batch_ids):
            pillar_mask = batch_ids == batch_id
            point_mask = valid_mask[pillar_mask]
            frame_values = values[pillar_mask][point_mask]
            if frame_values.numel() == 0:
                continue
            mean = frame_values.mean()
            std = frame_values.std(unbiased=False).clamp(
                min=self.physical_std_floor
            )
            normalized[pillar_mask] = (values[pillar_mask] - mean) / std
        return normalized

    def forward(self, batch_dict, **kwargs):
        voxel_features = batch_dict["voxels"]
        voxel_num_points = batch_dict["voxel_num_points"]
        coords = batch_dict["voxel_coords"]

        max_points = voxel_features.shape[1]
        valid_mask = self.get_paddings_indicator(
            voxel_num_points, max_points, axis=0
        )
        batch_ids = coords[:, 0].long()

        rcs = voxel_features[:, :, self.physical_rcs_index]
        radial_velocity = voxel_features[:, :, self.physical_velocity_index]
        z_rcs = self._frame_standardize(rcs, valid_mask, batch_ids)
        z_velocity = self._frame_standardize(
            radial_velocity, valid_mask, batch_ids
        )
        abs_velocity = z_velocity.abs()
        physical_descriptor = torch.stack(
            [z_rcs, z_velocity, abs_velocity, z_rcs * abs_velocity], dim=-1
        )

        num_voxels, num_points, _ = physical_descriptor.shape
        encoded = self.physical_point_encoder(
            physical_descriptor.reshape(num_voxels * num_points, 4)
        ).reshape(num_voxels, num_points, -1)

        mask = valid_mask.unsqueeze(-1)
        encoded_sum = (encoded * mask.type_as(encoded)).sum(dim=1)
        encoded_mean = encoded_sum / voxel_num_points.type_as(encoded).unsqueeze(
            -1
        ).clamp(min=1)
        encoded_max = encoded.masked_fill(~mask, -1e4).max(dim=1).values
        physical_feature = self.physical_pillar_projection(
            torch.cat([encoded_max, encoded_mean], dim=-1)
        )

        batch_dict = super().forward(batch_dict, **kwargs)
        geometry_feature = batch_dict["pillar_features"]
        gate = torch.sigmoid(
            self.physical_gate(
                torch.cat([geometry_feature, physical_feature], dim=-1)
            )
        )
        batch_dict["pillar_features"] = (
            geometry_feature
            + self.physical_residual_alpha
            * gate
            * torch.tanh(physical_feature)
        )
        return batch_dict
