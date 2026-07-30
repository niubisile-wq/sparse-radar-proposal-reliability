# Range / sparsity / calibration diagnostics

- seed: 2028
- IoU threshold: 0.5

## astyx

| Variant | nGT | Recall | Score-IoU corr | ECE(hit) | Top10 IoU |
|---|---:|---:|---:|---:|---:|
| rdar | 531 | 0.5744 | 0.2734 | 0.5442 | 0.6751 |
| m3rob_q15p25_viou0p24_s0p40 | 531 | 0.5763 | 0.2612 | 0.5692 | 0.6839 |
| q55rpa50_kprior | 531 | 0.5461 | 0.2375 | 0.4693 | 0.6642 |

## truckscenes

| Variant | nGT | Recall | Score-IoU corr | ECE(hit) | Top10 IoU |
|---|---:|---:|---:|---:|---:|
| rdar | 3950 | 0.0559 | 0.2632 | 0.3313 | 0.6031 |
| m3rob_q15p25_viou0p24_s0p40 | 3950 | 0.0577 | 0.2607 | 0.3606 | 0.5983 |
| q55rpa50_kprior | 3950 | 0.0529 | 0.2095 | 0.2906 | 0.5587 |

## v2xradarv

| Variant | nGT | Recall | Score-IoU corr | ECE(hit) | Top10 IoU |
|---|---:|---:|---:|---:|---:|
| rdar | 268 | 0.6194 | 0.1984 | 0.6034 | 0.7030 |
| m3rob_q15p25_viou0p24_s0p40 | 268 | 0.6269 | 0.2386 | 0.6359 | 0.7196 |
| q55rpa50_kprior | 268 | 0.6231 | 0.2772 | 0.5680 | 0.7483 |

## kradar

| Variant | nGT | Recall | Score-IoU corr | ECE(hit) | Top10 IoU |
|---|---:|---:|---:|---:|---:|
| rdar | 198 | 0.6667 | 0.2417 | 0.6533 | 0.7102 |
| m3rob_q15p25_viou0p24_s0p40 | 198 | 0.6465 | 0.2461 | 0.6573 | 0.7239 |
| q55rpa50_kprior | 198 | 0.6616 | 0.2471 | 0.5688 | 0.7069 |

## Practical decision

- The high-performance route `q55rpa50_kprior` is the calibration-positive
  variant in this diagnostic slice.
- The strict route is not the calibration winner here; it should stay in the
  robustness / AP story, not the calibration story.
