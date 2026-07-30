# Calibration report

This report summarizes score calibration from frozen prediction PKLs and their matching info PKLs. It is a supporting artifact, not a final matrix closure for `T12`.

| Dataset | Predictions | ECE(hit) | Brier | Score-IoU corr | Top10 IoU | Top10 hit rate |
|---|---:|---:|---:|---:|---:|---:|
| astyx_baseline | 929 | 0.1006 | 0.1025 | 0.7380 | 0.7175 | 1.0000 |
| astyx_rcnms | 50000 | 0.0390 | 0.0068 | 0.4984 | 0.7000 | 1.0000 |
| astyx_rdar | 55000 | 0.0302 | 0.0117 | 0.3430 | 0.7000 | 1.0000 |
| astyx_drav | 55000 | 0.0315 | 0.0114 | 0.3416 | 0.7132 | 0.9000 |
| astyx_drav_rgpc | 55000 | 0.0334 | 0.0116 | 0.3715 | 0.7203 | 1.0000 |

## Interpretation

- Lower ECE and Brier indicate better confidence quality.
- Higher score-IoU correlation indicates a stronger link between score and localization quality.
- This report should be paired with AP and latency evidence before any manuscript-level claim.
