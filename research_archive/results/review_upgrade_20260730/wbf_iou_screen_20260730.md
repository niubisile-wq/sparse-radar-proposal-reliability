# WBF IoU-threshold screen (seed 2028)

Input: RDAR prediction sets. WBF fuses all candidates in IoU clusters and retains representative metadata.

| Dataset | Best IoU threshold | RDAR AP | Best WBF AP | Delta AP |
|---|---:|---:|---:|---:|
| astyx | 0.5 | 34.3540 | 34.4898 | +0.1358 |
| truckscenes | 0.5 | 15.3041 | 15.1802 | -0.1239 |
| v2xradarv | 0.5 | 41.3385 | 40.6730 | -0.6655 |
| kradar | 0.5 | 52.0271 | 51.9306 | -0.0965 |

## All thresholds

| Dataset | IoU | AP | Delta AP |
|---|---:|---:|---:|
| astyx | 0.3 | 32.4529 | -1.9011 |
| astyx | 0.5 | 34.4898 | +0.1358 |
| astyx | 0.7 | 34.4186 | +0.0646 |
| truckscenes | 0.3 | 15.1777 | -0.1264 |
| truckscenes | 0.5 | 15.1802 | -0.1239 |
| truckscenes | 0.7 | 15.1562 | -0.1479 |
| v2xradarv | 0.3 | 38.5564 | -2.7821 |
| v2xradarv | 0.5 | 40.6730 | -0.6655 |
| v2xradarv | 0.7 | 40.6596 | -0.6789 |
| kradar | 0.3 | 50.7802 | -1.2469 |
| kradar | 0.5 | 51.9306 | -0.0965 |
| kradar | 0.7 | 51.8923 | -0.1348 |
