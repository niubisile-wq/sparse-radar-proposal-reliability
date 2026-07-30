# Detector latency from existing logs

Parsed from completed OpenPCDet eval logs. Unit: ms/frame.

| Method/log group | Astyx | TruckScenes | V2X-Radar-V | K-Radar |
|---|---:|---:|---:|---:|
| RDAR / TAAC + RC-NMS eval | 87.73 +/- 7.26 (3 seeds) | 18.17 +/- 1.50 (3 seeds) | 22.97 +/- 2.59 (3 seeds) | 23.90 +/- 3.05 (3 seeds) |
| M3 qflr55 + RC-NMS eval | 96.23 +/- 12.33 (3 seeds) | 24.07 +/- 3.43 (3 seeds) | 26.80 +/- 6.37 (3 seeds) | 24.30 +/- 0.89 (3 seeds) |
| M4 high-perf q55rpa50_kprior + RC-NMS eval | 73.50 +/- 11.60 (2 seeds) | 17.95 +/- 0.49 (2 seeds) | 21.65 +/- 1.48 (2 seeds) | 23.47 +/- 0.55 (3 seeds) |
| Strict-route expert stable_bevgate + RC-NMS eval | 77.27 +/- 9.22 (3 seeds) | 17.77 +/- 2.86 (3 seeds) | 20.10 +/- 2.52 (3 seeds) | 21.33 +/- 1.37 (3 seeds) |

## Use decision

- Keep this as detector-latency evidence if the manuscript states the exact eval setting.
- Do not merge detector latency and voting latency unless reporting an end-to-end pipeline variant.
- If a strict real-time claim is needed, rerun a dedicated profiler with fixed batch size, warmup, and no AP evaluation.

