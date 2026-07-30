# Corruption / compensation summary

Date: 2026-07-28

Part 3 is now closed.

## Final benchmark state

- Input family: `m3rob_q15p25_viou0p24_s0p40`
- Evaluation family: `evaluate_range_compensated_support.py`
- Total closed rows: 192
- Datasets: Astyx, TruckScenes, V2X-Radar-V, K-Radar
- Per-dataset row count: 48

## Best observed setting per dataset

| Dataset | Best AP_R40@3D IoU 0.50 | range_power | support_scale | alpha |
|---|---:|---:|---:|---:|
| Astyx | 34.4981 | 0.0 | 8.0 | 0.05 |
| TruckScenes | 18.7540 | 0.0 | 4.0 | 0.30 |
| V2X-Radar-V | 42.6786 | 2.0 | 1.0 | 0.05 |
| K-Radar | 53.7522 | 2.0 | 8.0 | 0.20 |

## Interpretation

- The semi-synthetic compensation benchmark is now fully executable and fully
  tabulated.
- The final matrix is dense enough to support a paper-facing summary.
- Any future rerun should be treated as a new audit row, not as an implicit
  overwrite of this closed matrix.
