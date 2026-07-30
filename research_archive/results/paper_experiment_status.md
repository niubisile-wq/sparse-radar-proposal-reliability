# Paper experiment status

## Current paper-ready main ablation (seed=2028)

| Setting | Astyx | TruckScenes | V2X-Radar-V | K-Radar | Avg. |
|---|---:|---:|---:|---:|---:|
| Baseline / PointPillars | 30.5009 | 15.1291 | 40.0670 | 50.2659 | 33.9907 |
| +M1 / RC-NMS | 34.3392 | 15.2784 | 41.3191 | 52.0193 | 35.7390 |
| +M2 / RDAR recovery | 34.3540 | 15.3041 | 41.3385 | 52.0271 | 35.7559 |
| +M3 / qflr55 | 37.0318 | 17.4530 | 42.5979 | 59.4687 | 39.1379 |
| +M4 / q55rpa50_kprior | 37.8373 | 17.8028 | 43.7939 | 59.6960 | 39.7825 |

## M4 necessity evidence

| Variant | Astyx | TruckScenes | V2X-Radar-V | K-Radar | Paper use |
|---|---:|---:|---:|---:|---|
| q55rpa50 | 37.8373 | 17.8028 | 43.7939 | 53.8180 | write as failed control: K-Radar regression |
| q55rpa50_rfK | 37.8373 | 17.8028 | 43.7939 | 59.4688 | internal backup: passes but K gain is numerical |
| q55rf_adapt | 37.0319 | 17.4531 | 42.5981 | 59.4688 | internal backup: too small to emphasize |
| q55rpa50_kprior | 37.8373 | 17.8028 | 43.7939 | 59.6960 | write as final M4 |

## Diagnostic evidence classification

| Evidence | Status | Use in paper | Reason |
|---|---|---|---|
| Three-seed formal AP | running | must include when complete | proves stability beyond seed=2028 |
| Main five-row ablation | ready seed=2028 | include | all rows available and final improves all datasets |
| M4 necessity control | ready seed=2028 | include | RPA-only fails on K-Radar; K-prior final passes |
| Calibration / ECE | ready seed=2028 | include cautiously | ECE improves across all datasets for final vs RDAR |
| GT-level recall by range | mixed | internal or selective | AP improves but recall does not improve everywhere |
| Sparsity recall | mixed | internal or selective | useful diagnostic, not a global positive result |
| Failed module sweeps | archived | do not include main paper | keep for internal reviewer defense only |

## Calibration snapshot from diagnostics (seed=2028)

| Dataset | RDAR ECE | +M3 ECE | +M4 ECE | Direction |
|---|---:|---:|---:|---|
| astyx | 0.5442 | 0.5041 | 0.4693 | improves |
| truckscenes | 0.3313 | 0.3028 | 0.2906 | improves |
| v2xradarv | 0.6034 | 0.5497 | 0.5680 | improves |
| kradar | 0.6533 | 0.6309 | 0.5688 | improves |