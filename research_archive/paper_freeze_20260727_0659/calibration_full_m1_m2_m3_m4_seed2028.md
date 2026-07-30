# Calibration report

This report summarizes score calibration from frozen prediction PKLs and their matching info PKLs. It is a supporting artifact, not a final matrix closure for `T12`.

| Dataset | Predictions | ECE(hit) | Brier | Score-IoU corr | Top10 IoU | Top10 hit rate | Status |
|---|---:|---:|---:|---:|---:|---:|---|
| astyx | 55000 | 0.0127 | 0.0120 | 0.4018 | 0.7138 | 0.9000 | ok |
| truckscenes | 44000 | 0.0205 | 0.0097 | 0.3265 | 0.6100 | 0.8000 | ok |
| v2xradarv | 44000 | 0.0125 | 0.0102 | 0.4137 | 0.7832 | 1.0000 | ok |
| kradar | 44000 | 0.0088 | 0.0065 | 0.4185 | 0.7230 | 1.0000 | ok |

## Interpretation

- Lower ECE and Brier indicate better confidence quality.
- Higher score-IoU correlation indicates a stronger link between score and localization quality.
- This report should be paired with AP and latency evidence before any manuscript-level claim.
