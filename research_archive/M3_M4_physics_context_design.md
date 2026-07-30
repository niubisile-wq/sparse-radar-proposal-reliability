# M3/M4 physics-and-context design

## Scientific problem

Radar-only PointPillars currently treats radial Doppler velocity as an ordinary
scalar and aggregates each pillar independently before the BEV backbone. This
creates two avoidable losses:

1. radial velocity has a sensor-centric direction that is not explicit in the
   BEV Cartesian representation;
2. an extremely sparse pillar has insufficient local evidence to infer object
   extent and heading, while unconstrained global attention can mix unrelated
   or unreliable clutter.

The two candidate modules address these losses sequentially and remain
orthogonal to RC-NMS/RDAR, which operate only after prediction.

## M3 candidate: PVD diagnostic and DRAV module

For a radar return at azimuth

`theta = atan2(y, x)`

with measured radial velocity `v_r`, append the Cartesian line-of-sight
components

`v_x^r = v_r cos(theta), v_y^r = v_r sin(theta)`.

The clean PVD screen retains the original `v_r` and appends these two components,
so it cannot lose the raw measurement. It tests whether this physical
inductive bias transfers to Astyx, TruckScenes, V2X-Radar-V, and K-Radar under
an otherwise identical champion configuration.

If PVD passes the four-dataset screen, the paper module is Doppler
Reliability-Adaptive Vectorization (DRAV). It predicts a bounded modulation
from range, RCS, absolute radial speed, pillar return count, and within-pillar
Doppler dispersion:

`[vx', vy'] = (1 + tanh(delta)) [vx_r, vy_r]`.

The last layer producing `delta` is zero-initialized, so DRAV starts exactly
equal to PVD and learns only a reliability correction. The raw `v_r` is always
retained. This explicitly differs from fixed Doppler decomposition in
RadarPillars: reliable returns can receive stronger Cartesian evidence, while
ambiguous/tangential or cluttered returns can be attenuated without losing the
measurement.

Implementation smoke evidence:

- PVD and zero-initialized DRAV output maximum absolute difference: `0.0`;
- output and reliability-gate gradients: finite;
- reliability-gate final-layer gradient norm on a synthetic batch:
  `0.0031656`, proving the gate can leave its identity initialization.

## M4 candidate: reliability-gated geometry-aware pillar context (RGPC)

For pillar feature `f_i`, construct a position/reliability embedding

`e_i = MLP(x_i / W, y_i / H, log(1+n_i)/log(1+n_max))`,

where `n_i` is the number of radar returns in the pillar. Queries and keys use
`f_i + e_i`; values remain `f_i`. This makes contextual similarity aware of
metric position and evidence density.

The contextual result `c_i` is not allowed to replace the baseline feature.
Instead,

`f_i' = f_i + sigmoid(g) * (c_i - f_i)`,

with a learnable channel-wise gate initialized to `0.1`. The identity path
protects stable local features and lets training use context only where it is
beneficial.

This differs from:

- RPFA-Net/global PillarAttention: geometry and density enter attention, and
  the original feature is retained through a controlled residual path;
- PillarDAN: the reliability signal is an explicit physical return count and
  the residual gate prevents wholesale feature replacement;
- generic VoTr/SST: the design targets radar pillar reliability and is tested
  as a lightweight PointPillars insertion rather than a new detector backbone.

## Evidence gate

A module is accepted only after:

1. every one of three paired seeds improves on every dataset;
2. mean incremental gain is at least +1.0 AP on every dataset;
3. paired 95% CI lower bound is greater than zero on every dataset;
4. training, data split, epochs, augmentation, post-processing, and RDAR
   residual expert are identical except for the claimed module.

Seed 2028 is the screen. A failure below +1.0 AP on any dataset triggers early
stopping before formal seeds 2026/2027.

## Literature basis

- Musiat et al., *RadarPillars: Efficient Object Detection from 4D Radar Point
  Clouds*, arXiv:2408.05020.
- Xu et al., *RPFA-Net: a 4D RaDAR Pillar Feature Attention Network for 3D
  Object Detection*, ITSC 2021, DOI: 10.1109/ITSC48978.2021.9564754.
- Li et al., *PillarDAN: Pillar-based Dual Attention Network for 3D Object
  Detection with 4D RaDAR*, ITSC 2023,
  DOI: 10.1109/ITSC57777.2023.10422406.
- Mao et al., *Voxel Transformer for 3D Object Detection*, ICCV 2021.
- Fan et al., *Embracing Single Stride 3D Object Detector with Sparse
  Transformer*, CVPR 2022.
