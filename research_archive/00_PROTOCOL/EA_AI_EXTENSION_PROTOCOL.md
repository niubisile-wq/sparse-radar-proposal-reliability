# EAAI 投稿补强实验协议

Date: 2026-07-28

This protocol is the working contract for the current paper-ready extension
round. It is intentionally read-only with respect to the historical freeze.

## 1. Frozen baseline

- BASE_FREEZE_ID: `20260728_230418`
- Frozen reference workspace: `BASE_FREEZE_ID` only
- Historical results are read-only unless an explicit rerun is logged in
  `runs/RUN_LEDGER.csv`

## 2. Fixed evaluation scope

- Task: single-class sparse radar 3D object detection
- Core datasets: Astyx, TruckScenes, V2X-Radar-V, K-Radar
- Main metric: `AP_R40 @ 3D IoU 0.50`
- Seed protocol: `2026`, `2027`, `2028`
- Training / validation / test splits must remain identical across methods
- No dataset-specific hidden priors, no manual result replacement, no silent
  post-hoc filtering

## 3. Fair-comparison rules

1. Every formal comparison must use the same evaluator and the same class /
   coordinate mapping.
2. A method may only be compared after its checkpoint, prediction file, and
   evaluation log are all present.
3. Any method that uses extra priors or a modified input modality must be
   labeled accordingly in the manuscript.
4. The paper-facing baseline registry is the source of truth for which methods
   are in scope.

## 4. Deliverables for this round

- Part 1: protocol freeze and ledger
- Part 2: formal external PK
- Part 3: semi-synthetic radar corruption / compensation benchmark
- Part 5: manuscript merge, audit, and new freeze

## 5. Operational note

This round is allowed to add new evidence, but not to alter the historical
freeze. New evidence must be written to separate result files and recorded in
the run ledger.
