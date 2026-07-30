# Matrix Closure Map

Date: 2026-07-27

This document classifies `T1` to `T15` by current evidence strength. It is a
closure map, not a claim that the matrix is already finished.

## Summary

| ID | Current state | Evidence strength | Remaining gap |
|---|---|---|---|
| T1 | supported | strong | final paper-facing promotion language, if needed |
| T2 | partial | strong but incomplete | M3/M4 are incomplete on some datasets |
| T3 | supported | strong | paper-facing promotion language, if needed |
| T4 | partial | moderate | paired one-variable-at-a-time closure |
| T5 | partial | moderate | full identity-safe RGPC variant coverage |
| T6 | partial | moderate | final accepted range table with all bins closed |
| T7 | partial | moderate | full sparsity closure with bootstrap CI |
| T8 | partial | moderate | final physical-analysis package, not just screening |
| T9 | partial | moderate | point-dropout slope finalized across seeds |
| T10 | partial | moderate | RCS/Doppler corruption grid fully closed |
| T11 | supported | strong | paper-facing promotion language, if needed |
| T12 | supported | strong | paper-facing promotion language, if needed |
| T13 | partial | moderate | final convergence package / time-to-target framing |
| T14 | partial | weak-to-moderate | fixed-frame qualitative set still needs final selection |
| T15 | partial | moderate | shared-global sensitivity package still incomplete |

## Row Notes

### T1 Main comparison

Current evidence:

- [results/main_comparison_13x4_ap_report.md](C:/Users/刘子轩/radar_experiment_configs/results/main_comparison_13x4_ap_report.md)
- [results/13x4_ap_evidence.json](C:/Users/刘子轩/radar_experiment_configs/results/13x4_ap_evidence.json)
- [results/13x4_ap_results.csv](C:/Users/刘子轩/radar_experiment_configs/results/13x4_ap_results.csv)
- [results/t1_t11_closure_memo.md](C:/Users/刘子轩/radar_experiment_configs/results/t1_t11_closure_memo.md)

Assessment:

- The four-dataset main comparison package is frozen and auditable.
- This is materially better than a vague screening note.
- It still remains a frozen evidence package, not the final manuscript claim.

### T2 Sequential ablation

Current evidence:

- [results/final_ablation_report.md](C:/Users/刘子轩/radar_experiment_configs/results/final_ablation_report.md)
- [results/fair_ablation_report.md](C:/Users/刘子轩/radar_experiment_configs/results/fair_ablation_report.md)
- [results/fair_ablation_seed_results.csv](C:/Users/刘子轩/radar_experiment_configs/results/fair_ablation_seed_results.csv)
- [results/t2_t3_support_digest.md](C:/Users/刘子轩/radar_experiment_configs/results/t2_t3_support_digest.md)
- [results/t2_t3_pass_index.md](C:/Users/刘子轩/radar_experiment_configs/results/t2_t3_pass_index.md)

Assessment:

- The sequential curve is partially reconstructed.
- M1 and M2 are supported on all four datasets.
- M3 and M4 are incomplete, so the gate is not closed.

### T3 Standalone factorial

Current evidence:

- [results/final_ablation_report.md](C:/Users/刘子轩/radar_experiment_configs/results/final_ablation_report.md)
- [results/fair_ablation_report.md](C:/Users/刘子轩/radar_experiment_configs/results/fair_ablation_report.md)
- [results/component_ablation_screen_report.md](C:/Users/刘子轩/radar_experiment_configs/results/component_ablation_screen_report.md)
- [results/t2_t3_support_digest.md](C:/Users/刘子轩/radar_experiment_configs/results/t2_t3_support_digest.md)
- [results/t2_t3_pass_index.md](C:/Users/刘子轩/radar_experiment_configs/results/t2_t3_pass_index.md)

Assessment:

- The full per-dataset interaction closure now exists across Astyx,
  TruckScenes, V2X-Radar-V, and K-Radar via the verified
  `M1+M2+M3+M4` outputs.
- The remaining work is only manuscript-facing phrasing, if any.

### T4 and T5

Current evidence:

- [results/component_ablation_screen_report.md](C:/Users/刘子轩/radar_experiment_configs/results/component_ablation_screen_report.md)
- [results/rgpc_family_screen_gate_report.md](C:/Users/刘子轩/radar_experiment_configs/results/rgpc_family_screen_gate_report.md)

Assessment:

- These are in screening form with some partial and failing cells.
- They are not yet publication-final ablation packages.

### T6 and T7

Current evidence:

- [results/range_sparsity_diagnostic_seed2028.md](C:/Users/刘子轩/radar_experiment_configs/results/range_sparsity_diagnostic_seed2028.md)
- [results/diagnostic_all_seed2028.md](C:/Users/刘子轩/radar_experiment_configs/results/diagnostic_all_seed2028.md)

Assessment:

- Range and sparsity diagnostics exist.
- They remain diagnostic/supporting artifacts rather than final acceptance tables.

### T8 Physical analysis

Current evidence:

- [results/physical_evidence_rank_screen.md](C:/Users/刘子轩/radar_experiment_configs/results/physical_evidence_rank_screen.md)
- [results/diagnostic_gate_summary.md](C:/Users/刘子轩/radar_experiment_configs/results/diagnostic_gate_summary.md)

Assessment:

- Physical evidence ranking and calibration-adjacent support exist.
- The package is still not final.

### T9 and T10 Robustness

Current evidence:

- [results/robustness_pgdr_screen_report.md](C:/Users/刘子轩/radar_experiment_configs/results/robustness_pgdr_screen_report.md)
- [results/point_dropout_voting_gate_summary.md](C:/Users/刘子轩/radar_experiment_configs/results/point_dropout_voting_gate_summary.md)

Assessment:

- Robustness screening exists.
- Final corruption-grid closure is still missing.

### T11 Efficiency

Current evidence:

- [results/efficiency_report.md](C:/Users/刘子轩/radar_experiment_configs/results/efficiency_report.md)
- [results/detector_latency_from_logs.md](C:/Users/刘子轩/radar_experiment_configs/results/detector_latency_from_logs.md)
- [results/t1_t11_closure_memo.md](C:/Users/刘子轩/radar_experiment_configs/results/t1_t11_closure_memo.md)

Assessment:

- Parameter and latency evidence are present and coherent.
- This is one of the closest-to-closed rows, but the matrix still labels it screening.

### T12 Calibration

Current evidence:

- [results/calibration_report_seed2028.md](C:/Users/刘子轩/radar_experiment_configs/results/calibration_report_seed2028.md)
- [results/calibration_comparison_seed2028.md](C:/Users/刘子轩/radar_experiment_configs/results/calibration_comparison_seed2028.md)
- [results/calibration_sequential_astyx_seed2028.md](C:/Users/刘子轩/radar_experiment_configs/results/calibration_sequential_astyx_seed2028.md)
- [results/calibration_stable_four_modules_seed5623.md](C:/Users/刘子轩/radar_experiment_configs/results/calibration_stable_four_modules_seed5623.md)
- [results/calibration_full_m1_m2_m3_m4_seed2028.md](C:/Users/刘子轩/radar_experiment_configs/results/calibration_full_m1_m2_m3_m4_seed2028.md)
- [results/t12_calibration_gap_report.md](C:/Users/刘子轩/radar_experiment_configs/results/t12_calibration_gap_report.md)

Assessment:

- Calibration tooling exists.
- Calibration reports exist.
- The full baseline/M1–M4 paired-prediction requirement is now satisfied by the closed `M1+M2+M3+M4` outputs.
- The q55 calibration comparison already covers all four datasets with populated metrics, and the new four-module calibration report does as well.
- The historical stable-four non-Astyx `result.pkl` files remain useful as a historical contrast, but they are no longer the active blocker for T12 closure.
- The q55 calibration branch and the new four-module report are both populated across Astyx, TruckScenes, V2X-Radar-V, and K-Radar.

### T13 Convergence

Current evidence:

- [results/convergence_report_m0_radarpillar_seed2027_2030.md](C:/Users/刘子轩/radar_experiment_configs/results/convergence_report_m0_radarpillar_seed2027_2030.md)

Assessment:

- Convergence evidence exists.
- It is still an event-file audit, not the final convergence package described by the matrix.

### T14 Qualitative

Current evidence:

- [results/qualitative_case_candidates_seed2028.md](C:/Users/刘子轩/radar_experiment_configs/results/qualitative_case_candidates_seed2028.md)

Assessment:

- Fixed candidate frames exist.
- Final qualitative selection and manuscript-ready ordering are still pending.

### T15 Sensitivity

Current evidence:

- [results/diagnostic_gate_summary.md](C:/Users/刘子轩/radar_experiment_configs/results/diagnostic_gate_summary.md)
- [results/voting_sensitivity_summary.md](C:/Users/刘子轩/radar_experiment_configs/results/voting_sensitivity_summary.md)

Assessment:

- Sensitivity evidence exists.
- The shared-global closure across datasets is still incomplete.

## Practical conclusion

- `T1` and `T11` are the closest to closure.
- `T2` through `T10`, `T13`, `T14`, and `T15` remain incomplete.
- The matrix is still not paper-ready overall, but `T12` is now supported.


