# Fair Ablation Remaining Gap Map

Date: 2026-07-28

This note summarizes the remaining incomplete rows in
`results/fair_ablation_seed_results.csv` after the latest closure pass.

## 1. Current row-level status

- Total rows in the CSV: 322
- Completed rows: 322
- Incomplete rows: 0

The incomplete set is now empty:

- `blocked` rows: 0
- `failed evidence` rows: 0
- `retryable` rows: 0

## 2. Remaining incomplete rows by module

None.

## 3. Remaining incomplete rows by dataset

None.

## 4. Exact failed-evidence rows

None.

## 5. Exact blocked rows

None.

## 6. Interpretation

The fair-ablation CSV is now fully closed.

## 7. Remote artifact evidence

The artifact scan below is kept as historical evidence for the rows that were
previously retryable.

Checkpoint / result presence by module family:

| Module | checkpoint_epoch_160.pth | result.pkl | Reading |
|---|---|---|---|
| stable_bevgate_dapg_msbc | 15 | 20 | recoverable evidence exists |
| dapg2 | 9 | 13 | recoverable evidence exists |
| rccg | 4 | 9 | recoverable evidence exists |
| four_modules | 29 | 32 | recoverable evidence exists |
| sbd10 | 7 | 9 | recoverable evidence exists |
| msbc2 | 7 | 8 | recoverable evidence exists |
| stable_bevgate_dapg | 24 | 35 | recoverable evidence exists |
| taac | 17 | 32 | recoverable evidence exists |
| range3 | 8 | 9 | recoverable evidence exists |
| iouaware | 12 | 47 | recoverable evidence exists |
| bevgate | 73 | 159 | recoverable evidence exists |
| bevgate_dapg_msbc | 25 | 30 | recoverable evidence exists |
| rpa45 | 2 | 4 | recoverable evidence exists |
| dapg3 | 9 | 14 | recoverable evidence exists |
| iouaware_radarreplay | 2 | 4 | recoverable evidence exists |
| range2 | 7 | 8 | recoverable evidence exists |
| sbd20 | 7 | 9 | recoverable evidence exists |
| corner | 5 | 10 | recoverable evidence exists |
| msbc3 | 10 | 12 | recoverable evidence exists |
| bevgate_replay10 | 1 | 3 | recoverable evidence exists |
| rpa50 | 23 | 68 | recoverable evidence exists |

Interpretation:

- The historical scan still contains many recoverable artifacts that can be
  mined for supplementary evidence and reporting.
- This does not mean all historical rows were promotable to main-paper closure;
  it only explains how the now-closed retryable queue was triaged.

Artifact density summary:

- the retryable queue is now empty
- no current residual row is left in the artifact-density triage bucket

Live rerun note:

- `bevgate_replay10 / kradar / 2028` has completed its rerun on the remote
  instance and produced a saved `result.pkl` on GPU0.
- `corner / truckscenes / 2028` has completed its rerun on GPU1.
- `rccg / kradar / 2028` has completed its rerun on GPU2.
- `atss / truckscenes / 2028` has completed its rerun and produced
  `AP_R40@3D IoU 0.50: 0.0000`.
- `iouaware_radarreplay / kradar / 2028` has completed its rerun and produced
  `AP_R40@3D IoU 0.50: 46.6789`.
- `iouaware_radarreplay / v2xradarv / 2028` has completed its rerun and
  produced `AP_R40@3D IoU 0.50: 38.5645`.
- `rpa45 / truckscenes / 2028` has completed its rerun and produced
  `AP_R40@3D IoU 0.50: 12.0227`.
- `rpa55 / truckscenes / 2028` has now completed and produced
  `AP_R40@3D IoU 0.50: 14.2971`.
- There is no remaining waiting row in the TruckScenes queue.

## 8. Practical use

Use this map to separate the remaining work into:

- `blocked`: no checkpoint or no viable continuation path
- `retryable`: the run exists but needs a clean rerun
- `screen-only`: useful for manuscript support but not for final closure

The table does not claim these rows are already closed. It only makes the
residual work explicit enough to route.

## 9. Validated result samples

Three remote `result.pkl` files were inspected directly and confirmed to be
valid non-empty lists of per-frame prediction dictionaries:

| Module family | Dataset | Seed | File length | First-frame boxes |
|---|---|---|---|---|
| stable_bevgate_dapg_msbc | TruckScenes | 2029 | 80 frames | 500 boxes |
| four_modules | Astyx | 2026 | 100 frames | 16 boxes |
| taac | Astyx | 2028 | 100 frames | 500 boxes |

Why this matters:

- these are not dead artifacts;
- they can be reused for screen-only or supplemental evidence;
- they are useful candidates for harvesting into a lighter-weight manuscript
  appendix if a full closure rerun is not worth the cost.
