# Range / sparsity / calibration diagnostics

This report freezes the current seed-2028 diagnostic evidence for the
calibration-adjacent analysis used by `T6`, `T7`, and `T12` support.
It is not a final calibration acceptance package.

## Scope

- Seed: 2028
- IoU threshold: 0.5
- Variants compared against RDAR:
  - `qflr55`
  - `q55rpa50_kprior`

## Evidence sources

- `results/range_sparsity_diagnostic_seed2028.md`
- `results/diagnostic_gate_summary.json`
- `results/diagnostic_gate_summary.md`

## Summary

The diagnostics show that calibration is the cleaner signal for
`q55rpa50_kprior`, while range-wise and sparsity-wise recall remain mixed.
This is useful as a frozen diagnostic artifact, but it does not satisfy the
full `T12` requirement because the matrix still asks for baseline/M1-M4 paired
predictions and a Brier-score report.

## Astyx

| Variant | nGT | Recall | Score-IoU corr | ECE(hit) | Top10 IoU |
|---|---:|---:|---:|---:|---:|
| rdar | 531 | 0.5744 | 0.2734 | 0.5442 | 0.6751 |
| qflr55 | 531 | 0.5612 | 0.2317 | 0.5041 | 0.6618 |
| q55rpa50_kprior | 531 | 0.5461 | 0.2375 | 0.4693 | 0.6642 |

## TruckScenes-mini

| Variant | nGT | Recall | Score-IoU corr | ECE(hit) | Top10 IoU |
|---|---:|---:|---:|---:|---:|
| rdar | 3950 | 0.0559 | 0.2632 | 0.3313 | 0.6031 |
| qflr55 | 3950 | 0.0534 | 0.2269 | 0.3028 | 0.5724 |
| q55rpa50_kprior | 3950 | 0.0529 | 0.2095 | 0.2906 | 0.5587 |

## V2X-Radar-V-400

| Variant | nGT | Recall | Score-IoU corr | ECE(hit) | Top10 IoU |
|---|---:|---:|---:|---:|---:|
| rdar | 268 | 0.6194 | 0.1984 | 0.6034 | 0.7030 |
| qflr55 | 268 | 0.6306 | 0.2910 | 0.5497 | 0.7344 |
| q55rpa50_kprior | 268 | 0.6231 | 0.2772 | 0.5680 | 0.7483 |

## K-Radar-400

| Variant | nGT | Recall | Score-IoU corr | ECE(hit) | Top10 IoU |
|---|---:|---:|---:|---:|---:|
| rdar | 198 | 0.6667 | 0.2417 | 0.6533 | 0.7102 |
| qflr55 | 198 | 0.6616 | 0.2144 | 0.6309 | 0.6899 |
| q55rpa50_kprior | 198 | 0.6616 | 0.2471 | 0.5688 | 0.7069 |

## Practical decision

- Range-wise and sparsity-wise recall are mixed, so they remain internal
  supporting diagnostics.
- Calibration is the cleaner signal for `q55rpa50_kprior`.
- This report strengthens the evidence chain for `T12`, but it does not close
  the matrix requirement yet.

## Status

`T6`, `T7`, and the calibration-adjacent part of `T12` remain `screening`.
