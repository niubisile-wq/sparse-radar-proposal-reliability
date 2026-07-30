# T2/T3 Support Digest

Date: 2026-07-27

This digest is not a final closure package. It isolates the strongest current
evidence that can support the T2 sequential-ablation and T3 family-level
storylines.

## T2: Sequential ablation signals

Most defensible positive steps from the current fair-ablation ledger:

- `pointpillars -> rcnms` passes on Astyx and V2X-Radar-V.
- `bevgate_dapg -> bevgate_dapg_msbc` passes on TruckScenes.
- `stable_bevgate_dapg -> stable_bevgate_dapg_msbc` is positive on Astyx and K-Radar, but remains incomplete overall.

Current blockers that prevent closure:

- `M3` and `M4` are still incomplete on some datasets in
  [final_ablation_report.md](C:/Users/刘子轩/radar_experiment_configs/results/final_ablation_report.md).
- The `stable_four_modules` branch is structurally valid but functionally empty
  on the non-Astyx datasets in the calibration inventory.

## T3: Family-level / factor-level signals

The strongest family-level evidence currently in hand:

- `taac_rcnms` has the highest macro mean among the frozen fair-ablation rows
  in [fair_ablation_report.md](C:/Users/刘子轩/radar_experiment_configs/results/fair_ablation_report.md).
- `stable_bevgate_dapg_msbc` is the strongest complete stable-family row in the
  same report.
- `stable_four_modules` remains incomplete because its non-Astyx calibration
  outputs are empty.

## What this means

- The fair-ablation evidence already supports a narrower “best-supported
  improvements” narrative.
- It does not yet support promoting `T2` or `T3` to final matrix closure.
- The remaining work is still dominated by incomplete dataset coverage rather
  than lack of a representative story arc.

