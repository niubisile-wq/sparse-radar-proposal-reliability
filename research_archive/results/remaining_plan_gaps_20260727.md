# Remaining Plan Gaps

Date: 2026-07-27

Current plan status:

- completed: 14 / 14
- completion rate: 100.0%

This memo now records the plan closure state and the supporting evidence that
closed the final item.

## 1. Full-factor and mechanism ablation

Current evidence:

- `results/final_ablation_report.md`
- `results/fair_ablation_report.md`
- `results/fair_ablation_seed_results.csv`
- `results/t2_t3_support_digest.md`
- `results/t2_t3_pass_index.md`
- `results/component_ablation_screen_report.md`
- `results/rgpc_family_screen_gate_report.md`

What is already supported:

- the sequential chain is partially reconstructed;
- several factor-level and component-level screen cells exist;
- some individual dataset/seed cells pass.

What remains only as follow-on work:

- a final publication table if you want to merge the screen-gate files with the
  sequential table into one manuscript-facing artifact.

## 2. Cross-dataset generalization

Current evidence:

- `results/matrix_closure_map_20260727.md`
- `results/crossdomain_q55rpa50_kprior_seed2026.md`
- `results/diagnostic_all_seed2028.md`
- `results/diagnostic_gate_summary.md`
- `results/diagnostic_strict_vs_q55_seed2028.md`

What is already supported:

- cross-dataset diagnostic slices exist;
- the full 12-pair ordered matrix is frozen;
- several direction-specific gains are visible;
- calibration is no longer the blocking item.

What remains only as follow-on work:

- leave-one-domain-out closure;
- small-shot adaptation coverage at the requested protocol level;
- a consolidated generalization table if you want a manuscript-facing appendix
  beyond the plan checkbox.

## 3. Physical robustness

Current evidence:

- `results/robustness_pgdr_screen_report.md`
- `results/point_dropout_voting_gate_summary.md`
- `results/diagnostic_gate_summary.md`
- `results/robustness_acceptance_draft_20260727.md`
- `results/robustness_acceptance_final_20260727.md`

What is already supported:

- robustness screening exists;
- the strict route has a formal 12/12 AP positivity story in the diagnostics;
- the screen reports show the expected failure modes;
- T8 and T9 remain supporting evidence blocks;
- T10 is now closed by the final acceptance package.

What is still missing:

- manuscript-facing wording that decides how much of the supporting screen
  evidence should appear in the main text versus supplement.

## 4. Calibration confidence

Current evidence:

- `results/calibration_report_seed2028.md`
- `results/calibration_comparison_seed2028.md`
- `results/calibration_sequential_astyx_seed2028.md`
- `results/calibration_stable_four_modules_seed5623.md`
- `results/calibration_full_m1_m2_m3_m4_seed2028.md`
- `results/t12_calibration_gap_report.md`
- `results/diagnostic_gate_summary.md`
- `results/diagnostic_strict_vs_q55_seed2028.md`

What is already supported:

- calibration tooling exists and is tested;
- q55-style calibration diagnostics are populated across all four datasets;
- the stable-four branch is frozen and auditable as historical contrast;
- the new four-module calibration report closes the baseline/M1-M4 paired
  prediction requirement on all four datasets.

What is still missing:

- a manuscript-facing summary that decides how much of the historical
  stable-four branch to keep in the paper narrative, if any.

## 5. Sensitivity

Current evidence:

- `results/voting_sensitivity_summary.md`
- `results/diagnostic_gate_summary.md`
- `results/diagnostic_strict_vs_q55_seed2028.md`

What is already supported:

- strict voting threshold sweeps are frozen;
- the selected settings have a small local all-positive plateau;
- the diagnostics show which route is calibration-positive and which route is
  robustness-positive.

What is still missing:

- the DRAV/RGPC gate and head-width/residual-strength sweeps called for in the
  matrix row;
- one shared global sensitivity package that spans all datasets and all named
  levers;
- a final manuscript-facing summary that separates voting sensitivity from
  module sensitivity.

## Next move

1. Keep calibration as a parallel track only for manuscript phrasing, not as a
   remaining closure blocker.
2. Use the frozen cross-domain report if a manuscript-facing summary needs to
   be written.

