# Main Comparison Evidence Report

This report formalizes the T1 main comparison package for the four core datasets.

## Coverage

- Metric: `AP_R40`
- Datasets:
  - Astyx
  - MAN TruckScenes-mini
  - V2X-Radar-V-400
  - K-Radar-400
- Evidence package:
  - `results/13x4_ap_evidence.json`
  - `results/13x4_ap_results.csv`

The evidence package already includes a method-to-log mapping for all 13 rows,
so this is not a synthetic summary. It is a frozen audit view of the current
main comparison table.

## Snapshot

| Baseline | Astyx | TruckScenes-mini | V2X-Radar-V-400 | K-Radar-400 | MacroMean |
|---|---:|---:|---:|---:|---:|
| RadarPillar | 18.8006 | 5.5600 | 30.0646 | 32.9914 | 21.8541 |
| PointPillars | 17.1414 | 11.9058 | 32.9590 | 31.9160 | 23.4806 |
| MAFF-Net | 14.8022 | 11.3625 | 23.2357 | 2.0081 | 12.8521 |
| PV-RCNN | 14.3216 | 6.0524 | 13.3476 | 2.9420 | 9.1659 |
| Voxel R-CNN | 13.7367 | 2.1706 | 9.1176 | 21.4797 | 11.6262 |
| VoxelNeXt | 12.4657 | 2.7029 | 15.1061 | 20.5481 | 12.7057 |
| SECOND | 10.2040 | 2.6218 | 9.9993 | 15.2708 | 9.5240 |
| CenterPoint | 9.4416 | 2.6889 | 14.5770 | 11.9113 | 9.6547 |
| PillarNet | 7.3324 | 2.8710 | 9.7977 | 9.0488 | 7.2625 |
| PV-RCNN++ | 6.0159 | 3.6516 | 11.2030 | 15.3282 | 9.0497 |
| Part-A^2 | 3.5379 | 2.2953 | 10.8219 | 11.8770 | 7.1330 |
| PointRCNN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| TransFusion | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Audit Notes

- The `results/13x4_ap_evidence.json` file maps each method and dataset cell to a
  source log name.
- The CSV is the publication-facing table.
- The package is already aligned with the four-dataset reporting requirement in
  the plan matrix.

## Status

T1 is now supported by a frozen evidence package and should be treated as
`screening`, not `pending`.
