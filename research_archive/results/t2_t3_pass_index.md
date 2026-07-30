# T2/T3 Pass Index

Date: 2026-07-27

This index lists the current `pass` cells from
[fair_ablation_report.md](C:/Users/刘子轩/radar_experiment_configs/results/fair_ablation_report.md)
and the strongest adjacent family-level rows. It is a compact evidence map, not
a final closure package.

## T2 pass cells

The current sequential paired-delta rows that pass the gate are:

| Step | Dataset | Mean ΔAP | 95% CI lower | n | Why it passes |
|---|---|---:|---:|---:|---|
| PointPillars -> RC-NMS | Astyx | +4.2165 | +3.1422 | 3 | positive on all seeds, practical gain, CI lower > 0 |
| PointPillars -> RC-NMS | V2X-Radar-V | +1.4879 | +0.8629 | 3 | positive on all seeds, practical gain, CI lower > 0 |
| BEVGATE-DAPG -> BEVGATE-DAPG-MSBC | TruckScenes | +5.4280 | +2.2741 | 3 | positive on all seeds, practical gain, CI lower > 0 |

## T3 strongest family-level rows

The most useful family-level rows already frozen in
[fair_ablation_report.md](C:/Users/刘子轩/radar_experiment_configs/results/fair_ablation_report.md)
are:

| Module | Astyx | TruckScenes | V2X-Radar-V | K-Radar | Macro mean | Current reading |
|---|---:|---:|---:|---:|---:|---|
| taac_rcnms | 33.1874 | 16.3295 | 42.8078 | 55.1917 | 36.8791 | strongest macro mean in the report |
| stable_bevgate_dapg_msbc | 27.6501 | 17.0262 | 41.5751 | 53.6578 | 34.9773 | strongest complete stable-family row |
| bevgate_dapg_msbc | 28.0965 | 21.1790 | 41.4425 | 54.4423 | 36.2901 | strong balanced family row |
| rdar | 32.8347 | 16.3671 | 41.7029 | 50.5163 | 35.3552 | reference route for paired comparisons |

## Remaining blockers

- `T2` still lacks full sequential closure because `M3` / `M4` are incomplete on
  some datasets in [final_ablation_report.md](C:/Users/刘子轩/radar_experiment_configs/results/final_ablation_report.md).
- `T3` still lacks a full per-dataset interaction package.
- `stable_four_modules` remains empty on the non-Astyx calibration outputs, so
  it cannot be used as a closure artifact.

## Use decision

- Use the three pass cells above as the current strongest sequential evidence.
- Use the four family rows above as the current strongest family-level evidence.
- Do not promote `T2` or `T3` to final closure yet.

