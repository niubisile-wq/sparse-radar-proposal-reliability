# Gaussian Soft-NMS sigma screen (seed 2028)

Input: RDAR prediction sets. Same dataset evaluation protocol as the box-voting controls.

| Dataset | Best sigma | RDAR AP | Best Soft-NMS AP | Delta AP |
|---|---:|---:|---:|---:|
| astyx | 1.0 | 34.3540 | 34.3344 | -0.0196 |
| truckscenes | 0.5 | 15.3041 | 15.6160 | +0.3119 |
| v2xradarv | 1.0 | 41.3385 | 41.2813 | -0.0572 |
| kradar | 0.5 | 52.0271 | 51.9144 | -0.1127 |

## All sigma values

| Dataset | Sigma | AP | Delta AP |
|---|---:|---:|---:|
| astyx | 0.1 | 32.7744 | -1.5796 |
| astyx | 0.5 | 34.2510 | -0.1030 |
| astyx | 1.0 | 34.3344 | -0.0196 |
| truckscenes | 0.1 | 15.3577 | +0.0536 |
| truckscenes | 0.5 | 15.6160 | +0.3119 |
| truckscenes | 1.0 | 15.5671 | +0.2630 |
| v2xradarv | 0.1 | 40.5774 | -0.7611 |
| v2xradarv | 0.5 | 41.1269 | -0.2116 |
| v2xradarv | 1.0 | 41.2813 | -0.0572 |
| kradar | 0.1 | 51.2467 | -0.7804 |
| kradar | 0.5 | 51.9144 | -0.1127 |
| kradar | 1.0 | 51.8982 | -0.1289 |
