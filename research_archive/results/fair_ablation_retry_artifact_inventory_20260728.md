# Fair Ablation Retry Artifact Inventory

Date: 2026-07-28

This note summarizes the row-level artifact scan for the current retryable rows.

Source files:

- [fair_ablation_retry_queue_20260728.csv](C:/Users/刘子轩/radar_experiment_configs/results/fair_ablation_retry_queue_20260728.csv)
- [fair_ablation_retry_artifact_inventory_20260728.csv](C:/Users/刘子轩/radar_experiment_configs/results/fair_ablation_retry_artifact_inventory_20260728.csv)

## 1. Summary

- Retryable rows scanned: 52
- Rows with at least one recoverable artifact: 47
- Rows with no artifact found: 5

## 2. Validated non-empty samples

These `result.pkl` files were directly opened and confirmed to be valid lists of
per-frame prediction dictionaries:

| Module family | Dataset | Seed | File length | First-frame boxes |
|---|---|---|---|---|
| stable_bevgate_dapg_msbc | TruckScenes | 2029 | 80 frames | 500 boxes |
| four_modules | Astyx | 2026 | 100 frames | 16 boxes |
| taac | Astyx | 2028 | 100 frames | 500 boxes |

## 3. Highest artifact density rows

These rows have the strongest recoverable artifact density and are the best
screen-only or rerun candidates:

| Module | Dataset | Seed | result_count | ckpt_count |
|---|---|---|---|---|
| stable_bevgate_dapg | Astyx | 5623 | 14 | 7 |
| rpa50 | TruckScenes | 2028 | 12 | 4 |
| rccg | Astyx | 2026 | 9 | 4 |
| dapg2 | Astyx | 2035 | 8 | 4 |
| stable_four_modules | Astyx | 5623 | 7 | 4 |
| stable_bevgate_dapg_msbc | Astyx | 5623 | 6 | 3 |
| msbc2 | Astyx | 2035 | 5 | 4 |
| iouaware | Astyx | 5623 | 5 | 4 |

## 4. No-artifact retryable rows

These rows have no checkpoint or `result.pkl` found in the scanned tree:

- `atss / truckscenes / 2028`
- `iouaware_radarreplay / kradar / 2028`
- `iouaware_radarreplay / v2xradarv / 2028`
- `rpa45 / truckscenes / 2028`
- `rpa55 / truckscenes / 2028`

## 5. Practical reading

- Use the highest-density rows for immediate screen-only packaging.
- Use the no-artifact rows as lower-priority rerun candidates.
- Keep the full CSV as the authoritative artifact inventory if you need to
  inspect row-level details.
