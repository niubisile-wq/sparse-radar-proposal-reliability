# Final four-module ablation

This report freezes the current `T2` evidence as a screening artifact, not a
final acceptance package.

Evidence source:

- `build_final_ablation_report.py`
- remote `logs/fair_ablation/fair_*_seed*_gpu*.log`
- remote `logs/fair_ablation/eval_rdar_*_seed*_gpu*.log`

## Acceptance gate

All paired seeds positive, mean incremental gain >= +1.0 AP, paired 95% CI
lower bound > 0.

## Sequential AP

| System | Astyx | TruckScenes | V2X-Radar-V | K-Radar | Macro |
|---|---:|---:|---:|---:|---:|
| PointPillars | 28.5987 +/- 1.6869 (n=3) | 15.7163 +/- 1.7772 (n=3) | 40.1987 +/- 0.9695 (n=3) | 48.9068 +/- 1.6606 (n=3) | 33.3551 |
| + M1 RC-NMS | 32.8152 +/- 1.4692 (n=3) | 16.3498 +/- 1.7514 (n=3) | 41.6866 +/- 1.1545 (n=3) | 50.5059 +/- 2.0589 (n=3) | 35.3394 |
| + M2 RDAR | 32.8347 +/- 1.4689 (n=3) | 16.3671 +/- 1.7480 (n=3) | 41.7029 +/- 1.1490 (n=3) | 50.5163 +/- 2.0546 (n=3) | 35.3552 |
| + M3 DRAV | 33.8614 +/- 0.0000 (n=1) | — | 40.2537 +/- 0.0000 (n=1) | — | — |
| + M4 RGPC | — | — | — | — | — |

## Sequential paired increments

| Step | Dataset | Mean Delta AP | CI95 lower | n | Pass |
|---|---|---:|---:|---:|:---:|
| PointPillars -> + M1 RC-NMS | astyx | +4.2165 | +3.1422 | 3 | yes |
| PointPillars -> + M1 RC-NMS | truckscenes | +0.6335 | -0.5399 | 3 | no/pending |
| PointPillars -> + M1 RC-NMS | v2xradarv | +1.4879 | +0.8629 | 3 | yes |
| PointPillars -> + M1 RC-NMS | kradar | +1.5991 | -4.4846 | 3 | no/pending |
| + M1 RC-NMS -> + M2 RDAR | astyx | +0.0195 | -0.0019 | 3 | no/pending |
| + M1 RC-NMS -> + M2 RDAR | truckscenes | +0.0173 | -0.0007 | 3 | no/pending |
| + M1 RC-NMS -> + M2 RDAR | v2xradarv | +0.0163 | +0.0024 | 3 | no/pending |
| + M1 RC-NMS -> + M2 RDAR | kradar | +0.0103 | -0.0004 | 3 | no/pending |
| + M2 RDAR -> + M3 DRAV | astyx | -0.4926 | — | 1 | no/pending |
| + M2 RDAR -> + M3 DRAV | truckscenes | — | — | 0 | no/pending |
| + M2 RDAR -> + M3 DRAV | v2xradarv | -1.0848 | — | 1 | no/pending |
| + M2 RDAR -> + M3 DRAV | kradar | — | — | 0 | no/pending |
| + M3 DRAV -> + M4 RGPC | astyx | — | — | 0 | no/pending |
| + M3 DRAV -> + M4 RGPC | truckscenes | — | — | 0 | no/pending |
| + M3 DRAV -> + M4 RGPC | v2xradarv | — | — | 0 | no/pending |
| + M3 DRAV -> + M4 RGPC | kradar | — | — | 0 | no/pending |

## Training-module factorial controls

| Variant | Astyx | TruckScenes | V2X-Radar-V | K-Radar |
|---|---:|---:|---:|---:|
| pvd | 31.9413 +/- 0.0000 | 16.1795 +/- 0.0000 | 41.7123 +/- 0.0000 | 53.9699 +/- 0.0000 |
| drav | 33.8614 +/- 0.0000 | — | 40.2537 +/- 0.0000 | — |
| rgpc | 33.1426 +/- 0.0000 | — | — | — |
| pvd_rgpc | 34.4606 +/- 0.0000 | 12.6728 +/- 0.0000 | 46.3428 +/- 0.0000 | — |
| drav_rgpc | — | — | — | — |

## Status

`T2` is screening-only at present. It is not complete because `M3/M4` are
incomplete and the sequential gate does not pass on all datasets.
