# Fair Ablation Live Rerun Snapshot

Date: 2026-07-28 12:01 CST

This snapshot records the current state of the active reruns that are trying to
close the remaining no-artifact / retryable gaps.

## Active jobs

The previous retry queue is empty, but the host is currently occupied by live
training reruns.

## Current training jobs

These are the live reruns currently occupying the host GPUs:

| Row | GPU | Status |
|---|---:|---|
| none | - | none |

## Completed reruns

| Row | GPU | Status |
|---|---:|---|
| `atss15 / Astyx / 2028` | 1 | completed with `AP_R40@3D IoU 0.50: 0.0000` |
| `bevgate / K-Radar / 3407` | 2 | completed with saved `result.pkl` and AP `39.3228` |
| `bevgate_dapg_msbc / K-Radar / 2028` | 1 | completed with saved `result.pkl` and AP `48.7151` |
| `stable_bevgate_dapg_msbc / K-Radar / 2029` | 2 | completed with saved `result.pkl` and AP `52.5104` |
| `stable_four_modules / K-Radar / 2036` | 0 | completed with saved `result.pkl` and AP `58.4910` |
| `atss5 / Astyx / 2028` | 1 | completed with `AP_R40@3D IoU 0.50: 0.0000` |
| `stable_bevgate_dapg_msbc / K-Radar / 5623` | 0 | completed with saved `result.pkl` and AP `54.1047` |
| `atss / K-Radar / 2028` | 2 | completed with `AP_R40@3D IoU 0.50: 0.0000` |
| `four_modules / K-Radar / 2026` | 1 | completed with saved `result.pkl` and AP `51.1773` |
| `four_modules / K-Radar / 2027` | 2 | completed with saved `result.pkl` and AP `53.2546` |
| `msbc3 / K-Radar / 2028` | 0 | completed with saved `result.pkl` and AP `46.0134` |
| `bevgate_replay10 / kradar / 2028` | 0 | completed with saved `result.pkl` |
| `corner / truckscenes / 2028` | 1 | completed with saved `result.pkl` |
| `rccg / kradar / 2028` | 2 | completed with saved `result.pkl` |
| `atss / truckscenes / 2028` | 0 | completed with saved `result.pkl` |
| `iouaware_radarreplay / kradar / 2028` | 1 | completed with saved `result.pkl` |
| `iouaware_radarreplay / v2xradarv / 2028` | 2 | completed with saved `result.pkl` |
| `rpa45 / truckscenes / 2028` | 0 | completed with saved `result.pkl` |
| `rpa55 / truckscenes / 2028` | 1 | completed with saved `result.pkl` and AP `14.2971` |

## Waiting queue

No waiting rows remain.

## Still pending

none

## Interpretation

- The last live rerun has completed and the corresponding result has been written back.
- The Astyx split blocker has been rerun to completion and now yields usable
  zero-AP boundary evidence rather than a missing-sample failure.
- `bevgate / K-Radar / 3407`, `bevgate_dapg_msbc / K-Radar / 2028`,
  `stable_bevgate_dapg_msbc / K-Radar / 2029`, `stable_bevgate_dapg_msbc /
  K-Radar / 5623`, `stable_four_modules / K-Radar / 2036`, `atss5 / Astyx /
  2028`, `atss / K-Radar / 2028`, `four_modules / K-Radar / 2026`,
  `four_modules / K-Radar / 2027`, and `msbc3 / K-Radar / 2028` have all been
  rerun to completion and written back with exact AP results.
