# External baseline comparison

Derived from `results/formal_seed_summary.md` and aligned to the current paper tables package.

## Completion

| Method | Complete 3 seeds x 4 datasets | Missing |
|---|:---:|---|
| rdar | yes | -- |
| qflr55 | yes | -- |
| q55rpa50_kprior | yes | -- |

## Mean +/- SD AP

| Method | Astyx | TruckScenes | V2X-Radar-V | K-Radar | Macro mean |
|---|---:|---:|---:|---:|---:|
| rdar | 32.8347 +/- 1.4689 | 16.3671 +/- 1.7480 | 41.7029 +/- 1.1490 | 50.5163 +/- 2.0546 | 35.3552 |
| qflr55 | 35.8438 +/- 1.0680 | 16.9661 +/- 1.2785 | 44.4122 +/- 2.5011 | 57.6910 +/- 2.5304 | 38.7283 |
| q55rpa50_kprior | 36.9801 +/- 0.9748 | 16.8063 +/- 1.1764 | 44.3786 +/- 0.5122 | 58.3208 +/- 1.6943 | 39.1214 |

## Seed-level AP

| Method | Dataset | 2026 | 2027 | 2028 |
|---|---|---:|---:|---:|
| rdar | astyx | 32.7281 | 31.4220 | 34.3540 |
| rdar | truckscenes | 15.4127 | 18.3845 | 15.3041 |
| rdar | v2xradarv | 40.7802 | 42.9899 | 41.3385 |
| rdar | kradar | 51.3450 | 48.1767 | 52.0271 |
| qflr55 | astyx | 35.5364 | 34.9632 | 37.0318 |
| qflr55 | truckscenes | 15.5157 | 17.9295 | 17.4530 |
| qflr55 | v2xradarv | 43.3734 | 47.2653 | 42.5979 |
| qflr55 | kradar | 54.7940 | 58.8103 | 59.4687 |
| q55rpa50_kprior | astyx | 35.9197 | 37.1833 | 37.8373 |
| q55rpa50_kprior | truckscenes | 15.5086 | 17.1075 | 17.8028 |
| q55rpa50_kprior | v2xradarv | 44.5943 | 44.7477 | 43.7939 |
| q55rpa50_kprior | kradar | 58.8382 | 56.4281 | 59.6960 |

## Paired deltas

### qflr55 - rdar

| Dataset | Delta2026 | Delta2027 | Delta2028 | Mean Delta | All positive |
|---|---:|---:|---:|---:|:---:|
| astyx | 2.8083 | 3.5412 | 2.6778 | 3.0091 | yes |
| truckscenes | 0.1030 | -0.4550 | 2.1489 | 0.5990 | no |
| v2xradarv | 2.5932 | 4.2754 | 1.2594 | 2.7093 | yes |
| kradar | 3.4490 | 10.6336 | 7.4416 | 7.1747 | yes |

### q55rpa50_kprior - qflr55

| Dataset | Delta2026 | Delta2027 | Delta2028 | Mean Delta | All positive |
|---|---:|---:|---:|---:|:---:|
| astyx | 0.3833 | 2.2201 | 0.8055 | 1.1363 | yes |
| truckscenes | -0.0071 | -0.8220 | 0.3498 | -0.1598 | no |
| v2xradarv | 1.2209 | -2.5176 | 1.1960 | -0.0336 | no |
| kradar | 4.0442 | -2.3822 | 0.2273 | 0.6298 | no |

## Provenance

| Method | Dataset | Seed | Source |
|---|---|---:|---|
| rdar | astyx | 2026 | rdar_astyx_seed2026 |
| rdar | astyx | 2027 | rdar_astyx_seed2027 |
| rdar | astyx | 2028 | rdar_astyx_seed2028 |
| rdar | truckscenes | 2026 | rdar_truckscenes_seed2026 |
| rdar | truckscenes | 2027 | rdar_truckscenes_seed2027 |
| rdar | truckscenes | 2028 | rdar_truckscenes_seed2028 |
| rdar | v2xradarv | 2026 | rdar_v2xradarv_seed2026 |
| rdar | v2xradarv | 2027 | rdar_v2xradarv_seed2027 |
| rdar | v2xradarv | 2028 | rdar_v2xradarv_seed2028 |
| rdar | kradar | 2026 | rdar_kradar_seed2026 |
| rdar | kradar | 2027 | rdar_kradar_seed2027 |
| rdar | kradar | 2028 | rdar_kradar_seed2028 |
| qflr55 | astyx | 2026 | qflr55_astyx_seed2026 |
| qflr55 | astyx | 2027 | qflr55_astyx_seed2027 |
| qflr55 | astyx | 2028 | qflr55_astyx_seed2028 |
| qflr55 | truckscenes | 2026 | qflr55_truckscenes_seed2026 |
| qflr55 | truckscenes | 2027 | qflr55_truckscenes_seed2027 |
| qflr55 | truckscenes | 2028 | qflr55_truckscenes_seed2028 |
| qflr55 | v2xradarv | 2026 | qflr55_v2xradarv_seed2026 |
| qflr55 | v2xradarv | 2027 | qflr55_v2xradarv_seed2027 |
| qflr55 | v2xradarv | 2028 | qflr55_v2xradarv_seed2028 |
| qflr55 | kradar | 2026 | qflr55_kradar_seed2026 |
| qflr55 | kradar | 2027 | qflr55_kradar_seed2027 |
| qflr55 | kradar | 2028 | qflr55_kradar_seed2028 |
| q55rpa50_kprior | astyx | 2026 | q55rpa50_kprior_astyx_seed2026 |
| q55rpa50_kprior | astyx | 2027 | q55rpa50_kprior_astyx_seed2027 |
| q55rpa50_kprior | astyx | 2028 | q55rpa50_kprior_astyx_seed2028 |
| q55rpa50_kprior | truckscenes | 2026 | q55rpa50_kprior_truckscenes_seed2026 |
| q55rpa50_kprior | truckscenes | 2027 | q55rpa50_kprior_truckscenes_seed2027 |
| q55rpa50_kprior | truckscenes | 2028 | q55rpa50_kprior_truckscenes_seed2028 |
| q55rpa50_kprior | v2xradarv | 2026 | q55rpa50_kprior_v2xradarv_seed2026 |
| q55rpa50_kprior | v2xradarv | 2027 | q55rpa50_kprior_v2xradarv_seed2027 |
| q55rpa50_kprior | v2xradarv | 2028 | q55rpa50_kprior_v2xradarv_seed2028 |
| q55rpa50_kprior | kradar | 2026 | q55rpa50_kprior_kradar_seed2026 |
| q55rpa50_kprior | kradar | 2027 | q55rpa50_kprior_kradar_seed2027 |
| q55rpa50_kprior | kradar | 2028 | q55rpa50_kprior_kradar_seed2028 |
