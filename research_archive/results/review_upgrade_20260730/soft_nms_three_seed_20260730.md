# Gaussian Soft-NMS three-seed baseline (sigma=0.5)

Sigma 0.5 was fixed globally before the three-seed run; no dataset-specific seed-2028 tuning is used in this table.

| Dataset | RDAR mean AP | Soft-NMS mean AP | Mean delta | SD delta | All 3 positive |
|---|---:|---:|---:|---:|:---:|
| astyx | 32.8347 | 32.6516 | -0.1831 | 0.0727 | no |
| truckscenes | 16.3671 | 16.4580 | +0.0909 | 0.2467 | no |
| v2xradarv | 41.7029 | 41.4931 | -0.2098 | 0.0603 | no |
| kradar | 50.5163 | 50.5358 | +0.0196 | 0.1148 | no |

## Seed-level results

| Dataset | Seed | RDAR AP | Soft-NMS AP | Delta AP |
|---|---:|---:|---:|---:|
| astyx | 2026 | 32.7281 | 32.5265 | -0.2016 |
| astyx | 2027 | 31.4220 | 31.1772 | -0.2448 |
| astyx | 2028 | 34.3540 | 34.2510 | -0.1030 |
| truckscenes | 2026 | 15.4127 | 15.2374 | -0.1753 |
| truckscenes | 2027 | 18.3845 | 18.5205 | +0.1360 |
| truckscenes | 2028 | 15.3041 | 15.6160 | +0.3119 |
| v2xradarv | 2026 | 40.7802 | 40.6316 | -0.1486 |
| v2xradarv | 2027 | 42.9899 | 42.7208 | -0.2691 |
| v2xradarv | 2028 | 41.3385 | 41.1269 | -0.2116 |
| kradar | 2026 | 51.3450 | 51.4234 | +0.0784 |
| kradar | 2027 | 48.1767 | 48.2697 | +0.0930 |
| kradar | 2028 | 52.0271 | 51.9144 | -0.1127 |
