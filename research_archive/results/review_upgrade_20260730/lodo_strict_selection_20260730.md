# Leave-one-dataset-out strict-selection audit (2026-07-30)

Selection rule: among the frozen grid configurations whose nine training dataset-seed deltas are all positive, select the one with the largest training mean delta. The held-out dataset is never used for selection. Baseline is RDAR.

| Held-out | Selected vote IoU | Strength | Training mean delta | Training minimum delta | Held-out mean delta | Held-out minimum delta | Held-out all 3 positive |
|---|---:|---:|---:|---:|---:|---:|:---:|
| astyx | 0.22 | 0.40 | +0.8740 | +0.0252 | +0.5026 | +0.1931 | yes |
| truckscenes | 0.22 | 0.40 | +0.8660 | +0.1623 | +0.5264 | +0.0252 | yes |
| v2xradarv | 0.24 | 0.35 | +1.1826 | +0.5248 | +0.2392 | -0.2945 | no |
| kradar | 0.22 | 0.40 | +0.4803 | +0.0252 | +1.6836 | +1.0708 | yes |

## Seed-level results

| Held-out | Seed | Selected tag | RDAR AP | Held-out AP | Delta AP |
|---|---:|---|---:|---:|---:|
| astyx | 2026 | m3rob_q15p25_viou0p22_s0p40 | 32.7281 | 33.2512 | +0.5231 |
| astyx | 2027 | m3rob_q15p25_viou0p22_s0p40 | 31.4220 | 32.2137 | +0.7917 |
| astyx | 2028 | m3rob_q15p25_viou0p22_s0p40 | 34.3540 | 34.5471 | +0.1931 |
| truckscenes | 2026 | m3rob_q15p25_viou0p22_s0p40 | 15.4127 | 15.4379 | +0.0252 |
| truckscenes | 2027 | m3rob_q15p25_viou0p22_s0p40 | 18.3845 | 18.9652 | +0.5807 |
| truckscenes | 2028 | m3rob_q15p25_viou0p22_s0p40 | 15.3041 | 16.2774 | +0.9733 |
| v2xradarv | 2026 | m3rob_q15p25_viou0p24_s0p35 | 40.7802 | 40.9479 | +0.1677 |
| v2xradarv | 2027 | m3rob_q15p25_viou0p24_s0p35 | 42.9899 | 42.6954 | -0.2945 |
| v2xradarv | 2028 | m3rob_q15p25_viou0p24_s0p35 | 41.3385 | 42.1828 | +0.8443 |
| kradar | 2026 | m3rob_q15p25_viou0p22_s0p40 | 51.3450 | 53.9389 | +2.5939 |
| kradar | 2027 | m3rob_q15p25_viou0p22_s0p40 | 48.1767 | 49.2475 | +1.0708 |
| kradar | 2028 | m3rob_q15p25_viou0p22_s0p40 | 52.0271 | 53.4131 | +1.3860 |
