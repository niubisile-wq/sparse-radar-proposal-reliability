# Calibration report

This report summarizes score calibration from frozen prediction PKLs and their matching info PKLs. It is a supporting artifact, not a final matrix closure for `T12`.

| Dataset | Predictions | ECE(hit) | Brier | Score-IoU corr | Top10 IoU | Top10 hit rate |
|---|---:|---:|---:|---:|---:|---:|
| astyx_rdar | 55000 | 0.0302 | 0.0117 | 0.3430 | 0.7000 | 1.0000 |
| astyx_m3 | 55000 | 0.0208 | 0.0135 | 0.3521 | 0.7128 | 1.0000 |
| astyx_q55 | 55000 | 0.0361 | 0.0122 | 0.3974 | 0.7170 | 0.9000 |
| truck_rdar | 44000 | 0.0388 | 0.0108 | 0.2815 | 0.4410 | 0.4000 |
| truck_m3 | 44000 | 0.0260 | 0.0120 | 0.3097 | 0.5042 | 0.4000 |
| truck_q55 | 44000 | 0.0495 | 0.0118 | 0.2979 | 0.5863 | 0.8000 |
| v2x_rdar | 44000 | 0.0313 | 0.0088 | 0.3276 | 0.7497 | 1.0000 |
| v2x_m3 | 44000 | 0.0199 | 0.0111 | 0.3428 | 0.7616 | 1.0000 |
| v2x_q55 | 44000 | 0.0374 | 0.0094 | 0.3472 | 0.7367 | 0.9000 |
| kradar_rdar | 44000 | 0.0219 | 0.0061 | 0.3264 | 0.6859 | 1.0000 |
| kradar_m3 | 44000 | 0.0158 | 0.0072 | 0.3312 | 0.7031 | 1.0000 |
| kradar_q55 | 44000 | 0.0246 | 0.0063 | 0.3752 | 0.6905 | 1.0000 |

## Interpretation

- Lower ECE and Brier indicate better confidence quality.
- Higher score-IoU correlation indicates a stronger link between score and localization quality.
- This report should be paired with AP and latency evidence before any manuscript-level claim.
