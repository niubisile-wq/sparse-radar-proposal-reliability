# Strict route paired statistical summary

Variant: `m3rob_q15p25_viou0p24_s0p40`; baseline: RDAR. Unit: AP_R40@3D IoU 0.50 delta.

## Gate decision

- Positive paired comparisons: 12/12.
- Mean ΔAP: 0.9726; median ΔAP: 0.8493.
- Min/Max ΔAP: 0.1718 / 2.6060.
- Bootstrap 95% CI for mean ΔAP: [0.6468, 1.3536].
- Exact sign test: one-sided p = 0.000244; two-sided p = 0.000488.
- Paper decision: keep as strict cross-seed robustness evidence; treat p-values as auxiliary because n=12.

## Paired deltas

| Dataset | Seed | Strict - RDAR ΔAP |
|---|---:|---:|
| astyx | 2026 | 0.8222 |
| astyx | 2027 | 0.6202 |
| astyx | 2028 | 1.1228 |
| truckscenes | 2026 | 0.4765 |
| truckscenes | 2027 | 0.8135 |
| truckscenes | 2028 | 1.4721 |
| v2xradarv | 2026 | 0.2167 |
| v2xradarv | 2027 | 0.1718 |
| v2xradarv | 2028 | 0.8763 |
| kradar | 2026 | 2.6060 |
| kradar | 2027 | 1.0864 |
| kradar | 2028 | 1.3861 |
