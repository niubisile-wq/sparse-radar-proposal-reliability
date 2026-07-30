# WBF three-seed baseline (IoU threshold = 0.5)

IoU threshold 0.5 was fixed globally after the seed-2028 screen; the three-seed table uses the same threshold for all datasets.

| Dataset | RDAR mean AP | WBF mean AP | Mean delta | SD delta | All 3 positive |
|---|---:|---:|---:|---:|:---:|
| astyx | 32.8347 | 32.8229 | -0.0118 | 0.1668 | no |
| truckscenes | 16.3671 | 16.2366 | -0.1305 | 0.0677 | no |
| v2xradarv | 41.7029 | 41.4555 | -0.2474 | 0.3644 | no |
| kradar | 50.5163 | 50.3266 | -0.1896 | 0.0866 | no |

## Seed-level results

| Dataset | Seed | RDAR AP | WBF AP | Delta AP |
|---|---:|---:|---:|---:|
| astyx | 2026 | 32.7281 | 32.5354 | -0.1927 |
| astyx | 2027 | 31.4220 | 31.4434 | +0.0214 |
| astyx | 2028 | 34.3540 | 34.4898 | +0.1358 |
| truckscenes | 2026 | 15.4127 | 15.3464 | -0.0663 |
| truckscenes | 2027 | 18.3845 | 18.1833 | -0.2012 |
| truckscenes | 2028 | 15.3041 | 15.1802 | -0.1239 |
| v2xradarv | 2026 | 40.7802 | 40.7008 | -0.0794 |
| v2xradarv | 2027 | 42.9899 | 42.9927 | +0.0028 |
| v2xradarv | 2028 | 41.3385 | 40.6730 | -0.6655 |
| kradar | 2026 | 51.3450 | 51.1404 | -0.2046 |
| kradar | 2027 | 48.1767 | 47.9089 | -0.2678 |
| kradar | 2028 | 52.0271 | 51.9306 | -0.0965 |
