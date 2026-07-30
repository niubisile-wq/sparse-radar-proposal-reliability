# M4 candidate: Sensor-Calibrated Physical Evidence Encoding (SCPE)

## Status

Candidate only. It must not be called an accepted innovation module until it
passes the four-dataset screen and the three-seed paired significance gate.

## Empirical problem

All four benchmark inputs use the same nominal point format:

`[x, y, z, RCS/magnitude, radial velocity]`

However, inspection of one raw training frame per dataset shows incompatible
physical-attribute scales:

| Dataset | RCS/magnitude range | radial-velocity range |
|---|---:|---:|
| Astyx | 45.0 to 84.5 | -5.12 to 5.20 |
| MAN TruckScenes | -20.0 to 35.0 | -3.65 to 2.17 |
| V2X-Radar-V | 112.1 to 162.3 | -4.32 to 2.69 |
| K-Radar | 0.03 to 34.23 | -1.68 to 1.77 |

The current PillarVFE concatenates position, RCS and velocity and feeds them
through one PFN. This asks a shared architectural pattern to learn geometry and
sensor-dependent physical scales in the same projection.

## Literature basis

1. RadarPillars argues that LiDAR-oriented encoders underuse radar-specific
   velocity and introduces velocity decomposition and pillar attention.
   https://arxiv.org/abs/2408.05020
2. RCBEVDet uses a dual-stream radar backbone and an RCS-aware BEV encoder,
   treating RCS as a radar-specific physical prior rather than an ordinary
   coordinate channel.
   https://openaccess.thecvf.com/content/CVPR2024/papers/Lin_RCBEVDet_Radar-camera_Fusion_in_Birds_Eye_View_for_3D_Object_CVPR_2024_paper.pdf
3. DLRFusion reports that radar power and Doppler have different
   characteristics and encodes them through separate sparse paths before
   interaction.
   https://openaccess.thecvf.com/content/ICCV2025/html/Chae_Doppler-Aware_LiDAR-RADAR_Fusion_for_Weather-Robust_3D_Detection_ICCV_2025_paper.html
4. DoppDrive demonstrates that Doppler is not merely an auxiliary scalar: it
   provides physically meaningful motion evidence for radar densification.
   Temporal aggregation cannot be used here because the unified benchmark
   infos contain no sequence/pose/time metadata.
   https://openaccess.thecvf.com/content/ICCV2025/html/Haitman_DoppDrive_Doppler-Driven_Temporal_Aggregation_for_Improved_Radar_Object_Detection_ICCV_2025_paper.html

## Proposed mechanism

SCPE keeps the original geometry PFN unchanged and adds a physical residual
path:

1. For each frame, normalize RCS and radial velocity using valid radar points.
   The first screen uses mean/std for GPU-efficient differentiable batching;
   median/MAD is a later robustness ablation.
2. Construct a physical descriptor per point:
   `[z_rcs, z_vr, |z_vr|, z_rcs * |z_vr|]`.
3. Encode the descriptor with a small MLP and aggregate it inside each pillar
   using both max and mean pooling.
4. Fuse it into the ordinary pillar feature through a bounded residual gate:

   `F_out = F_geo + alpha * sigmoid(G(F_geo, F_phys)) * tanh(F_phys)`

5. Initialize the residual scale conservatively so the module begins near the
   proven baseline and learns only useful physical corrections.

## Why it is distinct from failed trials

- It does not repeat velocity decomposition alone.
- It does not repeat standalone pillar/channel attention.
- It does not replace the geometry representation.
- It explicitly addresses cross-sensor physical-scale mismatch and preserves
  raw baseline features through a residual path.

## Paper story

M1 preserves candidates that conventional radar post-processing suppresses.
M2 recovers geometrically supported residual detections.
M3 aligns classification confidence with localization quality during training.
M4 improves the evidence entering the detector by disentangling calibrated
radar physics from geometry.

The full story is therefore:

`physical evidence encoding -> quality-aligned learning -> candidate
preservation -> evidence-supported recovery`.

## Acceptance protocol

Screen on seed 2028 after the already accepted sequential stack.

- Reject immediately if any dataset is non-positive.
- Promote to formal validation only if every dataset gains at least 1.0 AP.
- Formal validation uses seeds 2026, 2027 and 2028.
- Final acceptance requires all 12 paired deltas positive and, for each
  dataset, paired 95% CI lower bound above zero.
- Also record parameters, FLOPs/latency, recall by range and performance by
  RCS/velocity bins to prove the intended mechanism.
