# Standard box-voting three-seed baseline (2026-07-30)

Fixed parameters were selected from the earlier 20-point control sweeps and then evaluated for all three seeds. No parameter was selected separately on the seed being reported.

| Dataset | IoU | Strength | RDAR mean AP | Box-voting mean AP | Mean delta | SD delta | All 3 positive |
|---|---:|---:|---:|---:|---:|---:|:---:|
| astyx | 0.30 | 0.50 | 32.8347 | 33.3070 | +0.4723 | 0.1651 | yes |
| truckscenes | 0.30 | 0.75 | 16.3671 | 16.2840 | -0.0831 | 0.4090 | no |
| v2xradarv | 0.40 | 0.25 | 41.7029 | 42.2371 | +0.5342 | 0.3317 | yes |
| kradar | 0.45 | 0.40 | 50.5163 | 50.5260 | +0.0097 | 0.0459 | no |

## Seed-level results

| Dataset | Seed | RDAR AP | Box-voting AP | Delta AP |
|---|---:|---:|---:|---:|
| astyx | 2026 | 32.7281 | 33.1603 | +0.4322 |
| astyx | 2027 | 31.4220 | 31.7529 | +0.3309 |
| astyx | 2028 | 34.3540 | 35.0077 | +0.6537 |
| truckscenes | 2026 | 15.4127 | 15.2455 | -0.1672 |
| truckscenes | 2027 | 18.3845 | 17.9410 | -0.4435 |
| truckscenes | 2028 | 15.3041 | 15.6656 | +0.3615 |
| v2xradarv | 2026 | 40.7802 | 41.4459 | +0.6657 |
| v2xradarv | 2027 | 42.9899 | 43.1468 | +0.1569 |
| v2xradarv | 2028 | 41.3385 | 42.1186 | +0.7801 |
| kradar | 2026 | 51.3450 | 51.3582 | +0.0132 |
| kradar | 2027 | 48.1767 | 48.1389 | -0.0378 |
| kradar | 2028 | 52.0271 | 52.0808 | +0.0537 |
