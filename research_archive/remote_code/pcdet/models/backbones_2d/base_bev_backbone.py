import numpy as np
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


class SEGate2D(nn.Module):
    def __init__(self, channels, reduction=8, residual=True):
        super().__init__()
        hidden = max(channels // reduction, 8)
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Conv2d(channels, hidden, kernel_size=1, bias=False),
            nn.ReLU(inplace=True),
            nn.Conv2d(hidden, channels, kernel_size=1, bias=True),
        )
        self.residual = residual

    def forward(self, x):
        gate = torch.sigmoid(self.fc(self.pool(x)))
        if self.residual:
            return x * (1.0 + gate)
        return x * gate


class StableSEGate2D(nn.Module):
    """Near-identity channel gate with a learnable bounded residual scale."""

    def __init__(self, channels, reduction=8, init_scale=0.1):
        super().__init__()
        hidden = max(channels // reduction, 8)
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Conv2d(channels, hidden, kernel_size=1, bias=False),
            nn.ReLU(inplace=True),
            nn.Conv2d(hidden, channels, kernel_size=1, bias=True),
        )
        self.residual_scale = LearnableResidualScale(init_scale)

    def forward(self, x):
        centered_gate = 2.0 * torch.sigmoid(self.fc(self.pool(x))) - 1.0
        return x * (1.0 + self.residual_scale() * centered_gate)


class RadarChannelContrastGate(nn.Module):
    """Identity-initialized channel gate using radar response mean and contrast."""

    def __init__(self, channels, reduction=8, init_scale=0.0):
        super().__init__()
        hidden = max(channels // reduction, 8)
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Conv2d(2 * channels, hidden, kernel_size=1, bias=False),
            nn.SiLU(inplace=True),
            nn.Conv2d(hidden, channels, kernel_size=1, bias=True),
        )
        nn.init.zeros_(self.fc[-1].bias)
        self.residual_scale = LearnableResidualScale(init_scale)

    def forward(self, x):
        mean = self.pool(x)
        second_moment = self.pool(x.square())
        contrast = (second_moment - mean.square()).clamp_min(1e-6).sqrt()
        centered_gate = torch.tanh(self.fc(torch.cat((mean, contrast), dim=1)))
        return x * (1.0 + self.residual_scale() * centered_gate)


class MultiScaleBEVContext(nn.Module):
    """Lightweight residual context aggregation for sparse radar BEV maps."""

    def __init__(self, channels, hidden_channels=32, dilations=(1, 2, 4), init_scale=0.1):
        super().__init__()
        hidden_channels = max(8, int(hidden_channels))
        self.reduce = nn.Sequential(
            nn.Conv2d(channels, hidden_channels, kernel_size=1, bias=False),
            nn.BatchNorm2d(hidden_channels, eps=1e-3, momentum=0.01),
            nn.ReLU(inplace=True),
        )
        self.branches = nn.ModuleList(
            [
                nn.Sequential(
                    nn.Conv2d(
                        hidden_channels,
                        hidden_channels,
                        kernel_size=3,
                        padding=int(dilation),
                        dilation=int(dilation),
                        groups=hidden_channels,
                        bias=False,
                    ),
                    nn.BatchNorm2d(hidden_channels, eps=1e-3, momentum=0.01),
                    nn.ReLU(inplace=True),
                )
                for dilation in dilations
            ]
        )
        self.fuse = nn.Sequential(
            nn.Conv2d(
                hidden_channels * len(dilations),
                channels,
                kernel_size=1,
                bias=False,
            ),
            nn.BatchNorm2d(channels, eps=1e-3, momentum=0.01),
        )
        self.residual_scale = LearnableResidualScale(init_scale)

    def forward(self, x):
        reduced = self.reduce(x)
        context = self.fuse(torch.cat([branch(reduced) for branch in self.branches], dim=1))
        return x + self.residual_scale() * context


class RangeAwareSpatialGate(nn.Module):
    """Spatial BEV recalibration conditioned on radar range and feature evidence."""

    def __init__(self, kernel_size=7, init_scale=0.1):
        super().__init__()
        if kernel_size % 2 != 1:
            raise ValueError("RangeAwareSpatialGate kernel_size must be odd")
        self.gate = nn.Conv2d(
            3, 1, kernel_size=kernel_size, padding=kernel_size // 2, bias=True
        )
        nn.init.zeros_(self.gate.bias)
        self.residual_scale = LearnableResidualScale(init_scale)

    def forward(self, x):
        height, width = x.shape[-2:]
        lateral = torch.linspace(-1.0, 1.0, height, device=x.device, dtype=x.dtype)
        forward = torch.linspace(0.0, 1.0, width, device=x.device, dtype=x.dtype)
        range_map = torch.sqrt(
            lateral[:, None].square() + forward[None, :].square()
        )
        range_map = range_map.clamp_max_(1.0).expand(x.shape[0], 1, height, width)
        mean_map = x.mean(dim=1, keepdim=True)
        max_map = x.amax(dim=1, keepdim=True)
        gate = torch.sigmoid(self.gate(torch.cat((mean_map, max_map, range_map), dim=1)))
        return x * (1.0 + self.residual_scale() * gate)


class BaseBEVBackbone(nn.Module):
    def __init__(self, model_cfg, input_channels):
        super().__init__()
        self.model_cfg = model_cfg
        self.align_feature_maps = self.model_cfg.get('ALIGN_FEATURE_MAPS', False)
        self.use_bev_attention = self.model_cfg.get('USE_BEV_ATTENTION', False)
        self.bev_attention_reduction = max(1, int(self.model_cfg.get('BEV_ATTENTION_REDUCTION', 8)))
        self.bev_attention_residual = self.model_cfg.get('BEV_ATTENTION_RESIDUAL', True)
        self.use_ms_bev_context = self.model_cfg.get('USE_MS_BEV_CONTEXT', False)
        self.use_range_aware_spatial_gate = self.model_cfg.get(
            'USE_RANGE_AWARE_SPATIAL_GATE', False
        )
        self.use_stable_bev_gate = self.model_cfg.get('USE_STABLE_BEV_GATE', False)
        self.use_radar_channel_contrast_gate = self.model_cfg.get(
            'USE_RADAR_CHANNEL_CONTRAST_GATE', False
        )
        self.bev_feature_dropout_p = float(
            self.model_cfg.get('BEV_FEATURE_DROPOUT_P', 0.0)
        )
        if not 0.0 <= self.bev_feature_dropout_p < 1.0:
            raise ValueError('BEV_FEATURE_DROPOUT_P must be in [0, 1)')

        if self.model_cfg.get('LAYER_NUMS', None) is not None:
            assert len(self.model_cfg.LAYER_NUMS) == len(self.model_cfg.LAYER_STRIDES) == len(self.model_cfg.NUM_FILTERS)
            layer_nums = self.model_cfg.LAYER_NUMS
            layer_strides = self.model_cfg.LAYER_STRIDES
            num_filters = self.model_cfg.NUM_FILTERS
        else:
            layer_nums = layer_strides = num_filters = []

        if self.model_cfg.get('UPSAMPLE_STRIDES', None) is not None:
            assert len(self.model_cfg.UPSAMPLE_STRIDES) == len(self.model_cfg.NUM_UPSAMPLE_FILTERS)
            num_upsample_filters = self.model_cfg.NUM_UPSAMPLE_FILTERS
            upsample_strides = self.model_cfg.UPSAMPLE_STRIDES
        else:
            upsample_strides = num_upsample_filters = []

        num_levels = len(layer_nums)
        c_in_list = [input_channels, *num_filters[:-1]]
        self.blocks = nn.ModuleList()
        self.deblocks = nn.ModuleList()
        for idx in range(num_levels):
            cur_layers = [
                nn.ZeroPad2d(1),
                nn.Conv2d(
                    c_in_list[idx], num_filters[idx], kernel_size=3,
                    stride=layer_strides[idx], padding=0, bias=False
                ),
                nn.BatchNorm2d(num_filters[idx], eps=1e-3, momentum=0.01),
                nn.ReLU()
            ]
            for k in range(layer_nums[idx]):
                cur_layers.extend([
                    nn.Conv2d(num_filters[idx], num_filters[idx], kernel_size=3, padding=1, bias=False),
                    nn.BatchNorm2d(num_filters[idx], eps=1e-3, momentum=0.01),
                    nn.ReLU()
                ])
            self.blocks.append(nn.Sequential(*cur_layers))
            if len(upsample_strides) > 0:
                stride = upsample_strides[idx]
                if stride > 1 or (stride == 1 and not self.model_cfg.get('USE_CONV_FOR_NO_STRIDE', False)):
                    self.deblocks.append(nn.Sequential(
                        nn.ConvTranspose2d(
                            num_filters[idx], num_upsample_filters[idx],
                            upsample_strides[idx],
                            stride=upsample_strides[idx], bias=False
                        ),
                        nn.BatchNorm2d(num_upsample_filters[idx], eps=1e-3, momentum=0.01),
                        nn.ReLU()
                    ))
                else:
                    stride = np.round(1 / stride).astype(int)
                    self.deblocks.append(nn.Sequential(
                        nn.Conv2d(
                            num_filters[idx], num_upsample_filters[idx],
                            stride,
                            stride=stride, bias=False
                        ),
                        nn.BatchNorm2d(num_upsample_filters[idx], eps=1e-3, momentum=0.01),
                        nn.ReLU()
                    ))

        c_in = sum(num_upsample_filters)
        if len(upsample_strides) > num_levels:
            self.deblocks.append(nn.Sequential(
                nn.ConvTranspose2d(c_in, c_in, upsample_strides[-1], stride=upsample_strides[-1], bias=False),
                nn.BatchNorm2d(c_in, eps=1e-3, momentum=0.01),
                nn.ReLU(),
            ))

        if self.use_bev_attention:
            self.bev_attention = SEGate2D(c_in, self.bev_attention_reduction, self.bev_attention_residual)
        else:
            self.bev_attention = None

        if self.use_stable_bev_gate:
            self.stable_bev_gate = StableSEGate2D(
                c_in,
                reduction=max(1, int(self.model_cfg.get('STABLE_BEV_GATE_REDUCTION', 8))),
                init_scale=self.model_cfg.get('STABLE_BEV_GATE_INIT_SCALE', 0.1),
            )
        else:
            self.stable_bev_gate = None

        if self.use_radar_channel_contrast_gate:
            # Preserve the global CPU RNG stream so all downstream baseline layers,
            # especially the dense head, receive exactly the same initialization.
            with torch.random.fork_rng(devices=[], enabled=True):
                self.radar_channel_contrast_gate = RadarChannelContrastGate(
                    c_in,
                    reduction=max(
                        1,
                        int(self.model_cfg.get('RADAR_CHANNEL_GATE_REDUCTION', 8)),
                    ),
                    init_scale=self.model_cfg.get(
                        'RADAR_CHANNEL_GATE_INIT_SCALE', 0.0
                    ),
                )
        else:
            self.radar_channel_contrast_gate = None

        if self.use_ms_bev_context:
            with torch.random.fork_rng(devices=[], enabled=True):
                self.ms_bev_context = MultiScaleBEVContext(
                    c_in,
                    hidden_channels=self.model_cfg.get('MS_BEV_HIDDEN_CHANNELS', 32),
                    dilations=tuple(self.model_cfg.get('MS_BEV_DILATIONS', [1, 2, 4])),
                    init_scale=self.model_cfg.get('MS_BEV_INIT_RESIDUAL_SCALE', 0.0),
                )
        else:
            self.ms_bev_context = None

        if self.use_range_aware_spatial_gate:
            with torch.random.fork_rng(devices=[], enabled=True):
                self.range_aware_spatial_gate = RangeAwareSpatialGate(
                    kernel_size=self.model_cfg.get('RANGE_GATE_KERNEL_SIZE', 7),
                    init_scale=self.model_cfg.get('RANGE_GATE_INIT_RESIDUAL_SCALE', 0.0),
                )
        else:
            self.range_aware_spatial_gate = None

        self.bev_feature_dropout = (
            nn.Dropout2d(p=self.bev_feature_dropout_p)
            if self.bev_feature_dropout_p > 0.0
            else None
        )

        self.num_bev_features = c_in

    def forward(self, data_dict):
        """
        Args:
            data_dict:
                spatial_features
        Returns:
        """
        spatial_features = data_dict['spatial_features']
        ups = []
        ret_dict = {}
        x = spatial_features
        for i in range(len(self.blocks)):
            x = self.blocks[i](x)

            stride = int(spatial_features.shape[2] / x.shape[2])
            ret_dict['spatial_features_%dx' % stride] = x
            if len(self.deblocks) > 0:
                ups.append(self.deblocks[i](x))
            else:
                ups.append(x)

        if self.align_feature_maps and len(ups) > 1:
            target_h = min(feat.shape[-2] for feat in ups)
            target_w = min(feat.shape[-1] for feat in ups)
            ups = [
                feat[
                    ...,
                    (feat.shape[-2] - target_h) // 2:(feat.shape[-2] - target_h) // 2 + target_h,
                    (feat.shape[-1] - target_w) // 2:(feat.shape[-1] - target_w) // 2 + target_w
                ]
                for feat in ups
            ]

        if len(ups) > 1:
            x = torch.cat(ups, dim=1)
        elif len(ups) == 1:
            x = ups[0]

        if len(self.deblocks) > len(self.blocks):
            x = self.deblocks[-1](x)

        if self.bev_attention is not None:
            x = self.bev_attention(x)

        if self.stable_bev_gate is not None:
            x = self.stable_bev_gate(x)
        if self.radar_channel_contrast_gate is not None:
            x = self.radar_channel_contrast_gate(x)

        if self.ms_bev_context is not None:
            x = self.ms_bev_context(x)

        if self.range_aware_spatial_gate is not None:
            x = self.range_aware_spatial_gate(x)

        if self.bev_feature_dropout is not None:
            x = self.bev_feature_dropout(x)

        data_dict['spatial_features_2d'] = x

        return data_dict


class BaseBEVBackboneV1(nn.Module):
    def __init__(self, model_cfg, **kwargs):
        super().__init__()
        self.model_cfg = model_cfg
        self.align_feature_maps = self.model_cfg.get('ALIGN_FEATURE_MAPS', False)

        layer_nums = self.model_cfg.LAYER_NUMS
        num_filters = self.model_cfg.NUM_FILTERS
        assert len(layer_nums) == len(num_filters) == 2

        num_upsample_filters = self.model_cfg.NUM_UPSAMPLE_FILTERS
        upsample_strides = self.model_cfg.UPSAMPLE_STRIDES
        assert len(num_upsample_filters) == len(upsample_strides)

        num_levels = len(layer_nums)
        self.blocks = nn.ModuleList()
        self.deblocks = nn.ModuleList()
        for idx in range(num_levels):
            cur_layers = [
                nn.ZeroPad2d(1),
                nn.Conv2d(
                    num_filters[idx], num_filters[idx], kernel_size=3,
                    stride=1, padding=0, bias=False
                ),
                nn.BatchNorm2d(num_filters[idx], eps=1e-3, momentum=0.01),
                nn.ReLU()
            ]
            for k in range(layer_nums[idx]):
                cur_layers.extend([
                    nn.Conv2d(num_filters[idx], num_filters[idx], kernel_size=3, padding=1, bias=False),
                    nn.BatchNorm2d(num_filters[idx], eps=1e-3, momentum=0.01),
                    nn.ReLU()
                ])
            self.blocks.append(nn.Sequential(*cur_layers))
            if len(upsample_strides) > 0:
                stride = upsample_strides[idx]
                if stride >= 1:
                    self.deblocks.append(nn.Sequential(
                        nn.ConvTranspose2d(
                            num_filters[idx], num_upsample_filters[idx],
                            upsample_strides[idx],
                            stride=upsample_strides[idx], bias=False
                        ),
                        nn.BatchNorm2d(num_upsample_filters[idx], eps=1e-3, momentum=0.01),
                        nn.ReLU()
                    ))
                else:
                    stride = np.round(1 / stride).astype(int)
                    self.deblocks.append(nn.Sequential(
                        nn.Conv2d(
                            num_filters[idx], num_upsample_filters[idx],
                            stride,
                            stride=stride, bias=False
                        ),
                        nn.BatchNorm2d(num_upsample_filters[idx], eps=1e-3, momentum=0.01),
                        nn.ReLU()
                    ))

        c_in = sum(num_upsample_filters)
        if len(upsample_strides) > num_levels:
            self.deblocks.append(nn.Sequential(
                nn.ConvTranspose2d(c_in, c_in, upsample_strides[-1], stride=upsample_strides[-1], bias=False),
                nn.BatchNorm2d(c_in, eps=1e-3, momentum=0.01),
                nn.ReLU(),
            ))

        self.num_bev_features = c_in

    def forward(self, data_dict):
        """
        Args:
            data_dict:
                spatial_features
        Returns:
        """
        spatial_features = data_dict['multi_scale_2d_features']

        x_conv4 = spatial_features['x_conv4']
        x_conv5 = spatial_features['x_conv5']

        ups = [self.deblocks[0](x_conv4)]

        x = self.blocks[1](x_conv5)
        ups.append(self.deblocks[1](x))

        if self.align_feature_maps:
            target_h = min(feat.shape[-2] for feat in ups)
            target_w = min(feat.shape[-1] for feat in ups)
            ups = [
                feat[
                    ...,
                    (feat.shape[-2] - target_h) // 2:(feat.shape[-2] - target_h) // 2 + target_h,
                    (feat.shape[-1] - target_w) // 2:(feat.shape[-1] - target_w) // 2 + target_w
                ]
                for feat in ups
            ]

        x = torch.cat(ups, dim=1)
        x = self.blocks[0](x)

        data_dict['spatial_features_2d'] = x

        return data_dict


class BasicBlock(nn.Module):
    expansion: int = 1

    def __init__(
        self,
        inplanes: int,
        planes: int,
        stride: int = 1,
        padding: int = 1,
        downsample: bool = False,
    ) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(inplanes, planes, kernel_size=3, stride=stride, padding=padding, bias=False)
        self.bn1 = nn.BatchNorm2d(planes, eps=1e-3, momentum=0.01)
        self.relu1 = nn.ReLU()
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes, eps=1e-3, momentum=0.01)
        self.relu2 = nn.ReLU()
        self.downsample = downsample
        if self.downsample:
            self.downsample_layer = nn.Sequential(
                nn.Conv2d(inplanes, planes, kernel_size=1, stride=stride, padding=0, bias=False),
                nn.BatchNorm2d(planes, eps=1e-3, momentum=0.01)
            )
        self.stride = stride

    def forward(self, x):
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu1(out)

        out = self.conv2(out)
        out = self.bn2(out)

        if self.downsample:
            identity = self.downsample_layer(x)

        out += identity
        out = self.relu2(out)

        return out


class BaseBEVResBackbone(nn.Module):
    def __init__(self, model_cfg, input_channels):
        super().__init__()
        self.model_cfg = model_cfg
        self.use_bev_attention = self.model_cfg.get('USE_BEV_ATTENTION', False)
        self.bev_attention_reduction = max(1, int(self.model_cfg.get('BEV_ATTENTION_REDUCTION', 8)))
        self.bev_attention_residual = self.model_cfg.get('BEV_ATTENTION_RESIDUAL', True)

        if self.model_cfg.get('LAYER_NUMS', None) is not None:
            assert len(self.model_cfg.LAYER_NUMS) == len(self.model_cfg.LAYER_STRIDES) == len(self.model_cfg.NUM_FILTERS)
            layer_nums = self.model_cfg.LAYER_NUMS
            layer_strides = self.model_cfg.LAYER_STRIDES
            num_filters = self.model_cfg.NUM_FILTERS
        else:
            layer_nums = layer_strides = num_filters = []

        if self.model_cfg.get('UPSAMPLE_STRIDES', None) is not None:
            assert len(self.model_cfg.UPSAMPLE_STRIDES) == len(self.model_cfg.NUM_UPSAMPLE_FILTERS)
            num_upsample_filters = self.model_cfg.NUM_UPSAMPLE_FILTERS
            upsample_strides = self.model_cfg.UPSAMPLE_STRIDES
        else:
            upsample_strides = num_upsample_filters = []

        num_levels = len(layer_nums)
        c_in_list = [input_channels, *num_filters[:-1]]
        self.blocks = nn.ModuleList()
        self.deblocks = nn.ModuleList()
        for idx in range(num_levels):
            cur_layers = [
                # nn.ZeroPad2d(1),
                BasicBlock(c_in_list[idx], num_filters[idx], layer_strides[idx], 1, True)
            ]
            for k in range(layer_nums[idx]):
                cur_layers.extend([
                    BasicBlock(num_filters[idx], num_filters[idx])
                ])
            self.blocks.append(nn.Sequential(*cur_layers))
            if len(upsample_strides) > 0:
                stride = upsample_strides[idx]
                if stride >= 1:
                    self.deblocks.append(nn.Sequential(
                        nn.ConvTranspose2d(
                            num_filters[idx], num_upsample_filters[idx],
                            upsample_strides[idx],
                            stride=upsample_strides[idx], bias=False
                        ),
                        nn.BatchNorm2d(num_upsample_filters[idx], eps=1e-3, momentum=0.01),
                        nn.ReLU()
                    ))
                else:
                    stride = np.round(1 / stride).astype(int)
                    self.deblocks.append(nn.Sequential(
                        nn.Conv2d(
                            num_filters[idx], num_upsample_filters[idx],
                            stride,
                            stride=stride, bias=False
                        ),
                        nn.BatchNorm2d(num_upsample_filters[idx], eps=1e-3, momentum=0.01),
                        nn.ReLU()
                    ))

        c_in = sum(num_upsample_filters) if len(num_upsample_filters) > 0 else sum(num_filters)
        if len(upsample_strides) > num_levels:
            self.deblocks.append(nn.Sequential(
                nn.ConvTranspose2d(c_in, c_in, upsample_strides[-1], stride=upsample_strides[-1], bias=False),
                nn.BatchNorm2d(c_in, eps=1e-3, momentum=0.01),
                nn.ReLU(),
            ))

        if self.use_bev_attention:
            self.bev_attention = SEGate2D(c_in, self.bev_attention_reduction, self.bev_attention_residual)
        else:
            self.bev_attention = None

        self.num_bev_features = c_in

    def forward(self, data_dict):
        """
        Args:
            data_dict:
                spatial_features
        Returns:
        """
        spatial_features = data_dict['spatial_features']
        ups = []
        ret_dict = {}
        x = spatial_features
        for i in range(len(self.blocks)):
            x = self.blocks[i](x)

            stride = int(spatial_features.shape[2] / x.shape[2])
            ret_dict['spatial_features_%dx' % stride] = x
            if len(self.deblocks) > 0:
                ups.append(self.deblocks[i](x))
            else:
                ups.append(x)

        if len(ups) > 1:
            x = torch.cat(ups, dim=1)
        elif len(ups) == 1:
            x = ups[0]

        if len(self.deblocks) > len(self.blocks):
            x = self.deblocks[-1](x)

        if self.bev_attention is not None:
            x = self.bev_attention(x)

        data_dict['spatial_features_2d'] = x

        return data_dict
