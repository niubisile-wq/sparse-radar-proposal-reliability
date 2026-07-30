# Unified baseline evidence table — 2026-07-30

## Main three-seed comparison

| Method | Astyx | TruckScenes | V2X-Radar-V | K-Radar | Macro AP |
|---|---:|---:|---:|---:|---:|
| RDAR (M1+M2) | 32.8347 | 16.3671 | 41.7029 | 50.5163 | 35.3552 |
| M3 quality alignment (qflr55) | 35.8438 | 16.9661 | 44.4122 | 57.6910 | 38.7283 |
| High-performance route (q55rpa50_kprior) | 36.9801 | 16.8063 | 44.3786 | 58.3208 | 39.1214 |
| Strict robust voting (selected s=0.40) | 33.6898 | 17.2878 | 42.1245 | 52.2091 | 36.3278 |

## Standard box-voting control sweeps

These are single-seed control sweeps and should not be presented as a replacement for the three-seed main comparison.

| Dataset | Seed | RDAR AP | Best standard box-voting AP | Delta |
|---|---:|---:|---:|---:|
| Astyx | 2026 | 32.7281 | 33.8342 | +1.1061 |
| TruckScenes | 2028 | 15.3041 | 16.9217 | +1.6176 |
| V2X-Radar-V | 2028 | 41.3385 | 42.1186 | +0.7801 |
| K-Radar | 2028 | 52.0271 | 52.0808 | +0.0537 |

### Fixed-parameter three-seed follow-up

| Dataset | IoU | Strength | RDAR mean AP | Box-voting mean AP | Mean delta | All 3 positive |
|---|---:|---:|---:|---:|---:|:---:|
| Astyx | 0.30 | 0.50 | 32.8347 | 33.3070 | +0.4723 | yes |
| TruckScenes | 0.30 | 0.75 | 16.3671 | 16.2840 | -0.0831 | no |
| V2X-Radar-V | 0.40 | 0.25 | 41.7029 | 42.2371 | +0.5342 | yes |
| K-Radar | 0.45 | 0.40 | 50.5163 | 50.5260 | +0.0097 | no |

This negative control shows that standard box voting alone does not reproduce the cross-dataset robustness pattern.

### Gaussian Soft-NMS (global sigma = 0.5)

| Dataset | RDAR mean AP | Soft-NMS mean AP | Mean delta | All 3 positive |
|---|---:|---:|---:|:---:|
| Astyx | 32.8347 | 32.6516 | -0.1831 | no |
| TruckScenes | 16.3671 | 16.4580 | +0.0909 | no |
| V2X-Radar-V | 41.7029 | 41.4931 | -0.2098 | no |
| K-Radar | 50.5163 | 50.5358 | +0.0196 | no |

### WBF (global IoU threshold = 0.5)

| Dataset | RDAR mean AP | WBF mean AP | Mean delta | All 3 positive |
|---|---:|---:|---:|:---:|
| Astyx | 32.8347 | 32.8229 | -0.0118 | no |
| TruckScenes | 16.3671 | 16.2366 | -0.1305 | no |
| V2X-Radar-V | 41.7029 | 41.4555 | -0.2474 | no |
| K-Radar | 50.5163 | 50.3266 | -0.1896 | no |

## Held-out threshold selection

Under training-only selection requiring all nine training dataset-seed deltas to be positive, the four held-out dataset means are:

| Held-out dataset | Mean delta AP | Held-out seed cells positive |
|---|---:|---:|
| Astyx | +0.5026 | 3/3 |
| TruckScenes | +0.5264 | 3/3 |
| V2X-Radar-V | +0.2392 | 2/3 |
| K-Radar | +1.6836 | 3/3 |
| Overall | +0.7380 | 11/12 |

Interpretation: the held-out dataset-level mean remains positive for all four datasets, but the evidence does not justify a held-out 12/12 seed claim.
