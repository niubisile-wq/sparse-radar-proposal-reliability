# Robustness Combined Summary

Date: 2026-07-27

This note consolidates the current robustness evidence into one place. It is a
supporting summary, not a final acceptance package for `T8`/`T10`.

## Evidence sources

- [robustness_pgdr_screen_report.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/robustness_pgdr_screen_report.md)
- [point_dropout_voting_gate_summary.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/point_dropout_voting_gate_summary.md)
- [physical_evidence_rank_screen.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/physical_evidence_rank_screen.md)
- [pre_submission_claim_risk_audit.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/pre_submission_claim_risk_audit.md)

## What is already supported

- Point-dropout robustness is quantified across all four datasets and three
  dropout rates.
- The `pgdr` screen covers Astyx, TruckScenes, V2X-Radar-V, and K-Radar.
- Physical evidence ranking shows that `count`, `rcs`, and `doppler` signals
  can improve AP, but the best evidence combination differs by dataset.
- The claim-risk audit already separates safe wording from unsafe wording for
  robustness claims.

## Quantitative anchors

### Point dropout

- q55 beats RDAR in 11/12 dropout cells.
- Mean q55 - RDAR AP margin: `+6.2902`.
- Minimum q55 - RDAR AP margin: `-0.0606`.
- Mean degradation advantage relative to clean checkpoints: `+2.3624`.

### pgdr screen

- Astyx: `clean 17.9559`, `rsc 17.9559`, `mild 17.8352`.
- TruckScenes: `formal 5.5996`.
- V2X-Radar-V: `formal 28.7995`.
- K-Radar: `formal 26.2880`.

### physical evidence rank screen

- Astyx best config: `rer_all_p0p0_logit_a0p200`, AP `35.7324`.
- TruckScenes best config: `rer_count_p0p0_logit_a1p600`, AP `18.3579`.
- V2X-Radar-V best config: `rer_count_doppler_p0p0_mul_a0p400`, AP `43.4016`.
- K-Radar best config: `rer_count_rcs_p0p0_logit_a1p600`, AP `54.2241`.

## Remaining gaps

- paired-seed degradation curves for every perturbation and every dataset;
- a consolidated AP-degradation slope table across all four datasets;
- a final robustness acceptance table rather than screen-level evidence;
- one common perturbation protocol that closes both strict and high-performance
  routes in the same table.

## Practical reading

- Robustness is no longer a blank spot; it is a real, multi-artifact evidence
  family.
- The current state is still best described as screening-plus-supporting
  evidence, not final acceptance.
