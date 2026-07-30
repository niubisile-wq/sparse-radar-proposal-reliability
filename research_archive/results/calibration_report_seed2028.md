# Calibration report

This report summarizes score calibration from frozen prediction PKLs and their matching info PKLs. It is a supporting artifact, not a final matrix closure for `T12`.

| Dataset | Predictions | ECE(hit) | Brier | Score-IoU corr | Top10 IoU | Top10 hit rate |
|---|---:|---:|---:|---:|---:|---:|
| astyx | 55000 | 0.0361 | 0.0122 | 0.3974 | 0.7170 | 0.9000 |
| truckscenes | 44000 | 0.0495 | 0.0118 | 0.2979 | 0.5863 | 0.8000 |
| v2xradarv | 44000 | 0.0374 | 0.0094 | 0.3472 | 0.7367 | 0.9000 |
| kradar | 44000 | 0.0246 | 0.0063 | 0.3752 | 0.6905 | 1.0000 |

## Interpretation

- Lower ECE and Brier indicate better confidence quality.
- Higher score-IoU correlation indicates a stronger link between score and localization quality.
- This report should be paired with AP and latency evidence before any manuscript-level claim.
