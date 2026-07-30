# Calibration report

This report summarizes score calibration from frozen prediction PKLs and their matching info PKLs. It is a supporting artifact, not a final matrix closure for `T12`.

| Dataset | Predictions | ECE(hit) | Brier | Score-IoU corr | Top10 IoU | Top10 hit rate | Status |
|---|---:|---:|---:|---:|---:|---:|---|
| stable_astyx | 900 | 0.1102 | 0.1018 | 0.7398 | 0.6943 | 0.8000 | ok |
| stable_truck | 0 | — | — | — | — | — | empty |
| stable_v2x | 0 | — | — | — | — | — | empty |
| stable_kradar | 0 | — | — | — | — | — | empty |

## Interpretation

- Lower ECE and Brier indicate better confidence quality.
- Higher score-IoU correlation indicates a stronger link between score and localization quality.
- This report should be paired with AP and latency evidence before any manuscript-level claim.
