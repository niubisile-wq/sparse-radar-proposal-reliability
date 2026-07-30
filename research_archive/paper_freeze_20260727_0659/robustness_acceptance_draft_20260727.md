# Robustness Acceptance Draft

Date: 2026-07-27

This draft consolidated the physical-robustness evidence before the final
acceptance package was written. It is now superseded by
[robustness_acceptance_final_20260727.md](C:/Users/刘子轩/radar_experiment_configs/results/robustness_acceptance_final_20260727.md).

## Sources

- [point_dropout_voting_gate_summary.md](C:/Users/刘子轩/radar_experiment_configs/results/point_dropout_voting_gate_summary.md)
- [robustness_pgdr_screen_report.md](C:/Users/刘子轩/radar_experiment_configs/results/robustness_pgdr_screen_report.md)
- [physical_evidence_rank_screen.md](C:/Users/刘子轩/radar_experiment_configs/results/physical_evidence_rank_screen.md)
- [robustness_combined_summary_20260727.md](C:/Users/刘子轩/radar_experiment_configs/results/robustness_combined_summary_20260727.md)
- [pre_submission_claim_risk_audit.md](C:/Users/刘子轩/radar_experiment_configs/results/pre_submission_claim_risk_audit.md)

## Row-by-row status

| Row | What is frozen now | What remains |
|---|---|---|
| T8 Physical analysis | dataset-specific evidence-rank screen with best configs and baseline deltas | a final paper-facing physical-analysis package if the row is to be promoted beyond screening |
| T9 Point dropout robustness | deterministic 10/20/30% dropout summary on all four datasets | paired-seed degradation curves for every dataset and a final slope table |
| T10 RCS/Doppler robustness | pgdr-family screen across Astyx, TruckScenes, V2X-Radar-V, and K-Radar | paired-seed corruption-grid closure for every perturbation and dataset |

## What the evidence already shows

### T8 physical analysis

- Physical evidence ranking is frozen across all four datasets.
- The best evidence combination differs by dataset.
- RCS and Doppler evidence help, but the best setting is not universal.

### T9 point dropout

- q55 beats RDAR in 11/12 dropout cells.
- Mean q55 - RDAR AP margin is `+6.2902`.
- Minimum q55 - RDAR AP margin is `-0.0606`.
- Mean degradation advantage relative to clean checkpoints is `+2.3624`.

### T10 pgdr screen

- Astyx has `clean`, `rsc`, and `mild` measurements.
- TruckScenes, V2X-Radar-V, and K-Radar each have a frozen `formal`
  measurement.
- The current screen confirms the corruption family is wired through the stack.

## What is still missing

- Seed-paired degradation curves for every perturbation on every dataset.
- A consolidated AP-degradation slope table across all four datasets.
- A final acceptance table that can be promoted beyond screening.

## Interpretation

- `T8` is frozen as a screen package.
- `T9` is frozen as a strong supporting package.
- `T10` is still the main missing piece for a final robustness acceptance row.

## Practical conclusion

The physical-robustness lane is materially better than before, but it is still
not a completed acceptance package.
