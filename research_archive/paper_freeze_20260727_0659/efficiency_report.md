# Efficiency report

Hardware: NVIDIA GeForce RTX 3090

## Parameter count

| Method/config group | Astyx | TruckScenes | V2X-Radar-V | K-Radar |
|---|---:|---:|---:|---:|
| RDAR / PointPillars-TAAC | 4.830 M | 4.830 M | 4.830 M | 4.830 M |
| M3 quality alignment (qflr55) | 4.830 M | 4.830 M | 4.830 M | 4.830 M |
| M4 high-performance (q55rpa50_kprior) | 4.830 M | 4.830 M | 4.830 M | 4.830 M |
| Strict-route expert (stable_bevgate) | 4.868 M | 4.868 M | 4.868 M | 4.868 M |

## Strict robust proposal voting overhead

Measured on the latest available `m3_stable_stage` PKLs per dataset. Timing excludes pickle I/O and KITTI evaluation.

| Dataset | Frames | Primary boxes | Voted boxes | Neighbor links | Mean time (s) | ms/frame |
|---|---:|---:|---:|---:|---:|---:|
| astyx | 100 | 50000 | 47790 | 216560 | 2.2709 +/- 0.0103 | 22.7095 +/- 0.1031 |
| truckscenes | 80 | 40000 | 37277 | 135592 | 1.7607 +/- 0.0146 | 22.0086 +/- 0.1826 |
| v2xradarv | 80 | 40000 | 38009 | 148862 | 1.8031 +/- 0.0038 | 22.5393 +/- 0.0471 |
| kradar | 80 | 40000 | 38457 | 149142 | 1.8279 +/- 0.0139 | 22.8485 +/- 0.1735 |

## Interpretation

- The strict voting module has 0 additional trainable parameters.
- Its overhead is a lightweight post-processing cost and should be reported separately from backbone inference.
- The high-performance q55rpa50_kprior route has its own trainable model parameters and should not be merged with the strict voting route in one parameter claim.

