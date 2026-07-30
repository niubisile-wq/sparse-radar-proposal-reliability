# Point dropout robustness summary

Protocol: deterministic inference-only radar point dropout before voxelization; no retraining. Drop seed = 3407.
RDAR uses seed2028 checkpoints for all datasets; q55 uses seed2027 for Astyx/TruckScenes/V2X-Radar-V and seed2028 for K-Radar.

## Gate decision

- Absolute AP: q55 wins 11/12 cells vs RDAR; losses 1/12.
- Mean q55 - RDAR AP margin: 6.2902.
- Minimum q55 - RDAR AP margin: -0.0606.
- Mean degradation advantage relative to clean checkpoints: 2.3624. Positive means q55 degrades less or improves more than RDAR.
- Paper decision: keep as average robustness / supplementary evidence, not as a strict all-cell robustness claim.

## Macro by dropout rate

| Drop rate | RDAR AP | q55 AP | q55 - RDAR | RDAR Δclean | q55 Δclean | q55 degradation advantage |
|---:|---:|---:|---:|---:|---:|---:|
| 10% | 33.0908 | 39.8078 | 6.7169 | -2.6651 | 0.1242 | 2.7892 |
| 20% | 31.8445 | 38.4806 | 6.6361 | -3.9114 | -1.2030 | 2.7084 |
| 30% | 32.3692 | 37.8866 | 5.5174 | -3.3868 | -1.7970 | 1.5897 |

## Per-dataset cells

| Dataset | Drop | RDAR AP | q55 AP | q55 - RDAR | RDAR Δclean | q55 Δclean |
|---|---:|---:|---:|---:|---:|---:|
| astyx | 10% | 26.9762 | 37.3582 | 10.3820 | -7.3778 | 0.1749 |
| astyx | 20% | 26.2630 | 36.4556 | 10.1926 | -8.0910 | -0.7277 |
| astyx | 30% | 28.0875 | 35.9020 | 7.8145 | -6.2665 | -1.2813 |
| truckscenes | 10% | 15.0037 | 16.0922 | 1.0885 | -0.3004 | -1.0153 |
| truckscenes | 20% | 12.4396 | 12.9768 | 0.5372 | -2.8645 | -4.1307 |
| truckscenes | 30% | 12.0161 | 11.9555 | -0.0606 | -3.2880 | -5.1520 |
| v2xradarv | 10% | 39.3501 | 44.7776 | 5.4275 | -1.9884 | 0.0299 |
| v2xradarv | 20% | 37.4167 | 43.5292 | 6.1125 | -3.9218 | -1.2185 |
| v2xradarv | 30% | 38.5468 | 45.5191 | 6.9723 | -2.7917 | 0.7714 |
| kradar | 10% | 51.0334 | 61.0032 | 9.9698 | -0.9937 | 1.3072 |
| kradar | 20% | 51.2588 | 60.9608 | 9.7020 | -0.7683 | 1.2648 |
| kradar | 30% | 50.8263 | 58.1698 | 7.3435 | -1.2008 | -1.5262 |
