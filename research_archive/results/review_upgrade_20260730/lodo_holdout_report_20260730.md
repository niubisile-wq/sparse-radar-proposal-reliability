# Leave-one-dataset-out threshold audit (2026-07-30)

Protocol: selected from the other three datasets using the frozen quality-alignment voting grid; evaluation uses the corresponding frozen per-seed outputs. The baseline is RDAR (M1+M2), not the stronger q55 route.

| Held-out dataset | Selected vote IoU | Strength | Mean delta AP | Min delta AP | All seed deltas > 0 | n |
|---|---:|---:|---:|---:|:---:|---:|
| astyx | 0.24 | 0.35 | +0.9871 | +0.7986 | yes | 3 |
| truckscenes | 0.25 | 0.35 | +0.9157 | +0.7818 | yes | 3 |
| v2xradarv | 0.24 | 0.35 | +0.2392 | -0.2945 | no | 3 |
| kradar | 0.24 | 0.35 | +1.5059 | +0.5248 | yes | 3 |

## Seed-level results

| Dataset | Seed | RDAR AP | Held-out AP | Delta AP | Log |
|---|---:|---:|---:|---:|---|
| astyx | 2026 | 32.7281 | 33.9447 | +1.2166 | m3rob_q15p25_viou0p24_s0p35_astyx_seed2026_gpu0.log |
| astyx | 2027 | 31.4220 | 32.3681 | +0.9461 | m3rob_q15p25_viou0p24_s0p35_astyx_seed2027_gpu0.log |
| astyx | 2028 | 34.3540 | 35.1526 | +0.7986 | m3rob_q15p25_viou0p24_s0p35_astyx_seed2028_gpu0.log |
| truckscenes | 2026 | 15.4127 | 16.4645 | +1.0518 | m3rob_q15p25_viou0p25_s0p35_truckscenes_seed2026_gpu1.log |
| truckscenes | 2027 | 18.3845 | 19.1663 | +0.7818 | m3rob_q15p25_viou0p25_s0p35_truckscenes_seed2027_gpu1.log |
| truckscenes | 2028 | 15.3041 | 16.2177 | +0.9136 | m3rob_q15p25_viou0p25_s0p35_truckscenes_seed2028_gpu1.log |
| v2xradarv | 2026 | 40.7802 | 40.9479 | +0.1677 | m3rob_q15p25_viou0p24_s0p35_v2xradarv_seed2026_gpu2.log |
| v2xradarv | 2027 | 42.9899 | 42.6954 | -0.2945 | m3rob_q15p25_viou0p24_s0p35_v2xradarv_seed2027_gpu2.log |
| v2xradarv | 2028 | 41.3385 | 42.1828 | +0.8443 | m3rob_q15p25_viou0p24_s0p35_v2xradarv_seed2028_gpu2.log |
| kradar | 2026 | 51.3450 | 53.9517 | +2.6067 | m3rob_q15p25_viou0p24_s0p35_kradar_seed2026_gpu3.log |
| kradar | 2027 | 48.1767 | 48.7015 | +0.5248 | m3rob_q15p25_viou0p24_s0p35_kradar_seed2027_gpu3.log |
| kradar | 2028 | 52.0271 | 53.4132 | +1.3861 | m3rob_q15p25_viou0p24_s0p35_kradar_seed2028_gpu3.log |
