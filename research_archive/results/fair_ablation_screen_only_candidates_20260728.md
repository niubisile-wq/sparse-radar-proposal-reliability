# Fair Ablation Screen-Only Candidates

Date: 2026-07-28

This note extracts the most useful screen-only candidates from the retryable
artifact inventory.

Source files:

- [fair_ablation_retry_artifact_inventory_20260728.csv](C:/Users/刘子轩/radar_experiment_configs/results/fair_ablation_retry_artifact_inventory_20260728.csv)
- [fair_ablation_screen_only_top15_20260728.csv](C:/Users/刘子轩/radar_experiment_configs/results/fair_ablation_screen_only_top15_20260728.csv)
- [fair_ablation_screen_only_no_artifact_20260728.csv](C:/Users/刘子轩/radar_experiment_configs/results/fair_ablation_screen_only_no_artifact_20260728.csv)

## 1. Top artifact-dense candidates

These are the 15 retryable rows with the strongest visible artifact density.
They are the best candidates for immediate screen-only packaging or fast
rerun triage.

| Module | Dataset | Seed | result_count | ckpt_count |
|---|---|---|---|---|
| stable_bevgate_dapg | Astyx | 5623 | 14 | 7 |
| rpa50 | TruckScenes | 2028 | 12 | 4 |
| rccg | Astyx | 2026 | 9 | 4 |
| dapg2 | Astyx | 2035 | 8 | 4 |
| stable_four_modules | Astyx | 5623 | 7 | 4 |
| stable_bevgate_dapg_msbc | Astyx | 5623 | 6 | 3 |
| iouaware | Astyx | 5623 | 5 | 4 |
| msbc2 | Astyx | 2035 | 5 | 4 |
| four_modules | K-Radar | 3407 | 5 | 3 |
| stable_bevgate_dapg_msbc | Astyx | 2029 | 5 | 3 |
| four_modules | K-Radar | 2036 | 5 | 3 |
| stable_bevgate_dapg | V2X-Radar-V | 5623 | 5 | 2 |
| bevgate_dapg_msbc | K-Radar | 2027 | 3 | 3 |
| bevgate | K-Radar | 2027 | 3 | 2 |
| stable_bevgate_dapg | TruckScenes | 5623 | 3 | 2 |

Directly validated samples from this group:

| Module | Dataset | Seed | Frames | First-frame boxes | Avg scores/frame | Max scores/frame |
|---|---|---|---|---|---|---|
| stable_bevgate_dapg | Astyx | 5623 | 100 | 18 | 9.14 | 22 |
| four_modules | Astyx | 2026 | 100 | 16 | 9.05 | 23 |
| taac | Astyx | 2028 | 100 | 500 | 500.0 | 500 |
| rpa50 | TruckScenes | 2028 | 80 | 500 | 500.0 | 500 |

## 2. No-artifact retryable rows

These rows have no checkpoint or `result.pkl` found in the scanned tree.
They are lower-priority rerun candidates.

- `atss / truckscenes / 2028`
- `iouaware_radarreplay / kradar / 2028`
- `iouaware_radarreplay / v2xradarv / 2028`
- `rpa45 / truckscenes / 2028`
- `rpa55 / truckscenes / 2028`

## 3. Recommended immediate use

1. Package the 15 artifact-dense rows as screen-only evidence first.
2. Keep the 5 no-artifact rows separate as low-priority rerun candidates.
3. Do not mix either group with the 2 truly blocked Astyx split failures.

## 4. Current reading

This is the last stage before any more brute-force reruns:

- the strong rows are now identifiable by artifact density;
- the weak rows are isolated;
- the true blockers remain isolated.

The four directly validated samples above are the ones I would package first if
the immediate goal is to create screen-only evidence with minimal additional
compute.

Current live rerun:

- `bevgate_replay10 / kradar / 2028`, `corner / truckscenes / 2028`, and
  `rccg / kradar / 2028` have all completed rerunning on the remote instance.
- `atss / truckscenes / 2028`, `iouaware_radarreplay / kradar / 2028`, and
  `iouaware_radarreplay / v2xradarv / 2028` are now the live reruns in flight.
