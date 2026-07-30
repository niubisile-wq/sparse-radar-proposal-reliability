# Standard box-voting comparison (seed 2028)

Input: RDAR prediction sets. This is a post-processing baseline sweep over vote IoU and strength, separate from the quality-aligned strict route.

| Dataset | Best IoU | Best strength | RDAR AP | Best AP | Delta AP |
|---|---:|---:|---:|---:|---:|
| truckscenes | 0.30 | 0.75 | 15.3041 | 16.9217 | +1.6176 |
| v2xradarv | 0.40 | 0.25 | 41.3385 | 42.1186 | +0.7801 |

## All sweep points

| Dataset | IoU | Strength | AP | Delta AP |
|---|---:|---:|---:|---:|
| truckscenes | 0.30 | 0.25 | 15.3000 | -0.0041 |
| truckscenes | 0.30 | 0.40 | 16.3179 | +1.0138 |
| truckscenes | 0.30 | 0.50 | 16.8046 | +1.5005 |
| truckscenes | 0.30 | 0.60 | 16.8033 | +1.4992 |
| truckscenes | 0.30 | 0.75 | 16.9217 | +1.6176 |
| truckscenes | 0.35 | 0.25 | 15.1706 | -0.1335 |
| truckscenes | 0.35 | 0.40 | 15.2991 | -0.0050 |
| truckscenes | 0.35 | 0.50 | 15.2992 | -0.0049 |
| truckscenes | 0.35 | 0.60 | 14.8913 | -0.4128 |
| truckscenes | 0.35 | 0.75 | 14.6739 | -0.6302 |
| truckscenes | 0.40 | 0.25 | 15.4089 | +0.1048 |
| truckscenes | 0.40 | 0.40 | 15.3310 | +0.0269 |
| truckscenes | 0.40 | 0.50 | 15.3506 | +0.0465 |
| truckscenes | 0.40 | 0.60 | 15.1848 | -0.1193 |
| truckscenes | 0.40 | 0.75 | 15.1273 | -0.1768 |
| truckscenes | 0.45 | 0.25 | 15.4040 | +0.0999 |
| truckscenes | 0.45 | 0.40 | 15.3681 | +0.0640 |
| truckscenes | 0.45 | 0.50 | 15.3703 | +0.0662 |
| truckscenes | 0.45 | 0.60 | 15.3372 | +0.0331 |
| truckscenes | 0.45 | 0.75 | 15.3221 | +0.0180 |
| v2xradarv | 0.30 | 0.25 | 41.2757 | -0.0628 |
| v2xradarv | 0.30 | 0.40 | 40.9704 | -0.3681 |
| v2xradarv | 0.30 | 0.50 | 41.0950 | -0.2435 |
| v2xradarv | 0.30 | 0.60 | 40.7260 | -0.6125 |
| v2xradarv | 0.30 | 0.75 | 40.3007 | -1.0378 |
| v2xradarv | 0.35 | 0.25 | 40.9729 | -0.3656 |
| v2xradarv | 0.35 | 0.40 | 40.5954 | -0.7431 |
| v2xradarv | 0.35 | 0.50 | 40.6561 | -0.6824 |
| v2xradarv | 0.35 | 0.60 | 40.6711 | -0.6674 |
| v2xradarv | 0.35 | 0.75 | 40.2784 | -1.0601 |
| v2xradarv | 0.40 | 0.25 | 42.1186 | +0.7801 |
| v2xradarv | 0.40 | 0.40 | 41.4358 | +0.0973 |
| v2xradarv | 0.40 | 0.50 | 41.2936 | -0.0449 |
| v2xradarv | 0.40 | 0.60 | 41.2936 | -0.0449 |
| v2xradarv | 0.40 | 0.75 | 41.1827 | -0.1558 |
| v2xradarv | 0.45 | 0.25 | 40.6813 | -0.6572 |
| v2xradarv | 0.45 | 0.40 | 40.2633 | -1.0752 |
| v2xradarv | 0.45 | 0.50 | 40.2643 | -1.0742 |
| v2xradarv | 0.45 | 0.60 | 39.7304 | -1.6081 |
| v2xradarv | 0.45 | 0.75 | 39.1804 | -2.1581 |
