# Stable BEV-gated expert specification

The strict-route expert uses the same radar input representation, class list,
box coder, and seven-parameter output head as the primary PointPillars-style
detector. The dataset-specific configuration files are:

- `pointpillars_stable_bevgate_astyx_car.yaml`
- `pointpillars_stable_bevgate_dapg_msbc_truckscenes_car.yaml`
- `pointpillars_stable_bevgate_dapg_msbc_v2xradarv_car.yaml`
- `pointpillars_stable_bevgate_dapg_msbc_kradar_car.yaml`

Core settings are 64-channel PillarVFE, 32-channel DensityAwarePillarGate,
64-channel BEV scatter, three BEV blocks with depths `[3,5,5]`, strides
`[2,2,2]`, filters `[64,128,256]`, and three 128-channel upsampling paths.
The stable channel gate uses reduction 8 and initial residual scale 0.1. The
multi-scale BEV context uses hidden width 32, dilations `[1,2,4]`, and initial
residual scale 0.1. Training uses the same 160-epoch Adam one-cycle schedule,
frozen split, augmentation policy, and evaluation checkpoint epoch as the
paired primary stream.

The gate is applied after BEV feature aggregation. For feature tensor `x`, it
computes `x * (1 + r * (2 sigmoid(g(GAP(x))) - 1))`, where `r` is a learnable
bounded residual scale initialized to 0.1. No extra sensor channel or label is
used. The exact YAML files and checkpoint provenance are archived with the
revision package.
