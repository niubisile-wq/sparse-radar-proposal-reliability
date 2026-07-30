# Robustness Acceptance Final

Date: 2026-07-27

This note closes the physical-robustness lane for the experiment plan. It
combines the already-frozen point-dropout evidence with the seeded `m3rob`
corruption-grid sweep and the physical evidence ranking screen.

## Evidence sources

- [physical_evidence_rank_screen.md](C:/Users/刘子轩/radar_experiment_configs/results/physical_evidence_rank_screen.md)
- [point_dropout_voting_gate_summary.md](C:/Users/刘子轩/radar_experiment_configs/results/point_dropout_voting_gate_summary.md)
- [voting_sensitivity_summary.md](C:/Users/刘子轩/radar_experiment_configs/results/voting_sensitivity_summary.md)
- [robustness_pgdr_screen_report.md](C:/Users/刘子轩/radar_experiment_configs/results/robustness_pgdr_screen_report.md)
- [robustness_combined_summary_20260727.md](C:/Users/刘子轩/radar_experiment_configs/results/robustness_combined_summary_20260727.md)

## What is now complete

### T8 physical analysis

- The screen is frozen in the physical evidence ranking package.
- It remains a supporting evidence block, not the main acceptance gate.

### T9 point dropout

- Deterministic 10/20/30% dropout evidence is frozen across all four datasets.
- The 11/12 cell advantage over RDAR is already recorded in the dropout summary.
- This is now a supporting robustness package.

### T10 RCS / Doppler corruption grid

- The seeded corruption-grid sweep is complete across Astyx, TruckScenes,
  V2X-Radar-V, and K-Radar.
- `summarize_vote_grid.py` reads the current remote logs and returns a complete
  16-variant grid with paired seeds.
- Two configurations are fully positive across all 12 dataset-seed cells:
  - `m3rob_q15p25_viou0p22_s0p40`
  - `m3rob_q15p25_viou0p24_s0p50`
- The strongest all-positive row is `m3rob_q15p25_viou0p22_s0p40`, with
  `positive=12/12` and macro AP means of:
  - Astyx: `+0.5026`
  - TruckScenes: `+0.5264`
  - V2X-Radar-V: `+0.4119`
  - K-Radar: `+1.6836`

## Acceptance readout

- The robustness lane is no longer a gap item.
- The remaining artifacts are supporting evidence and manuscript wording,
  not missing experiment execution.
- From the plan perspective, the physical-robustness checkbox can be closed.

