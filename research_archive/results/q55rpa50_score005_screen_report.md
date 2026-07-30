# q55rpa50 score005 screen report

This report freezes the current `score005` screen evidence as a supporting
artifact for `T12`, not a final calibration acceptance package.

## Evidence sources

- `logs/fair_ablation/screen_q55rpa50_score005_astyx_seed2028_gpu2.log`
- `logs/fair_ablation/screen_q55rpa50_score005_truckscenes_seed2028_gpu2.log`
- `logs/fair_ablation/screen_q55rpa50_score005_v2xradarv_seed2028_gpu2.log`
- `results/q55rpa50_score005_vs_rdar_screen_gate.md`
- `results/q55rpa50_score005_vs_qflr55_screen_gate.md`

## Observed AP snapshot

### Against RDAR

| Dataset | AP_R40@3D IoU 0.50 | Delta |
|---|---:|---:|
| Astyx | 37.8373 | +3.4833 |
| TruckScenes | 17.8028 | +2.4987 |
| V2X-Radar-V | pending | pending |
| K-Radar | pending | pending |

### Against qflr55

| Dataset | AP_R40@3D IoU 0.50 | Delta |
|---|---:|---:|
| Astyx | 37.8373 | +0.8055 |
| TruckScenes | 17.8028 | +0.3498 |
| V2X-Radar-V | pending | pending |
| K-Radar | pending | pending |

## Interpretation

- The score005 route improves the Astyx and TruckScenes 2028 screen results
  against both RDAR and qflr55.
- The screen is incomplete because V2X-Radar-V and K-Radar are still pending.
- This is a threshold-screening result only. It does not replace the ECE,
  Brier, or score-IoU calibration package required for `T12`.

## Status

`score005` is a useful calibration-adjacent screen, but `T12` remains
`screening`, not complete.

