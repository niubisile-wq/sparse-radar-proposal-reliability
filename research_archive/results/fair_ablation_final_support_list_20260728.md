# Fair Ablation Final Support List

Date: 2026-07-28

This note compresses the current support surface into a manuscript-facing list.
The exact CSV closure queue is now empty; this note is only about manuscript
supporting evidence.

## 1. Current status

- `fair_ablation_seed_results.csv`: `322/322` complete, `0` incomplete
- Residual queue: `0` blocked rows, `0` failed-evidence rows
- Support surface: `17` sibling / screen-only entries now collected

## 2. Best manuscript-facing support

These are the entries most likely to help in the main text, appendix, or a
boundary/contrast paragraph.

| Variant | Dataset | Seed | AP | Use |
|---|---|---:|---:|---|
| `q55kprior` | K-Radar | 2028 | 58.7077 | strongest direct GPU-backed sibling eval |
| `q55rpa50_kprior` | K-Radar | 2028 | 59.6806 | high-performance sibling support |
| `q55rpa50_kprior` | K-Radar | 2027 | 56.4168 | second seed for sibling support |
| `q55rccg` | Astyx | 2028 | 26.7364 | low-cost sibling contrast |
| `q55kaap` | K-Radar | 2028 | 58.7217 | high-performing sibling contrast |
| `q55msbc3` | Astyx | 2028 | 32.7835 | sibling contrast for msbc-family boundary |
| `stable_bevgate_dapg` | Astyx | 5623 | 30.9132 | already closed in the seed CSV |
| `stable_bevgate_dapg` | TruckScenes | 5623 | 13.1191 | sibling evidence, TruckScenes side |
| `stable_bevgate_dapg` | V2X-Radar-V | 5623 | 38.1079 | sibling evidence, V2X side |
| `stable_four_modules` | Astyx | 5623 | 29.1196 | already closed in the seed CSV |
| `stable_four_modules` | TruckScenes | 5623 | 0.0000 | useful negative boundary |
| `stable_four_modules` | V2X-Radar-V | 5623 | 0.0000 | useful negative boundary |
| `stable_bevgate_dapg_msbc` | Astyx | 2029 | 18.0565 | already closed in the seed CSV |
| `stable_bevgate_dapg_msbc` | V2X-Radar-V | 5623 | 41.4603 | sibling evidence, V2X side |
| `iouaware` | Astyx | 5623 | 31.1360 | already closed in the seed CSV |

## 3. Negative / boundary evidence

These rows are still useful, but only as failure-boundary or contrast evidence.

- `qflr55atss / Astyx / 2028` -> `0.0000`
- `qflr55_kradar / K-Radar / 2026` -> `53.1160`
- `atss / K-Radar / 2028` -> now closed with exact AP `0.0000`
- `atss5 / Astyx / 2028` -> now closed with exact AP `0.0000`
- `atss15 / Astyx / 2028` -> now closed with exact AP `0.0000`

## 4. Recommended paper use

Use the support surface in this order:

1. Main appendix / sibling comparison paragraph: `q55kprior`, `q55rpa50_kprior`, `q55rccg`, `q55kaap`, `q55msbc3`
2. Failure-boundary paragraph: `qflr55atss`, `stable_four_modules / TruckScenes`, `stable_four_modules / V2X-Radar-V`
3. Supporting contrast note: the `stable_bevgate_dapg` and `stable_bevgate_dapg_msbc` siblings

## 5. Writing constraint

The exact residual queue is closed; this material should be treated as
supporting evidence for the manuscript only.
