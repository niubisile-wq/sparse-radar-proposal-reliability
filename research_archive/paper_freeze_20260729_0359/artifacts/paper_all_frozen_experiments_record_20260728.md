# Paper all frozen experiments record

Date: 2026-07-28

Canonical freeze bundles:

- earlier freeze: `../paper_freeze_20260727_0659/`
- merged freeze entry: `../paper_freeze_20260729_0359/`

This file is the master checklist for the paper-facing experiment package. It
collects the already frozen experiment evidence, the qualitative substitute for
the original Part 4, and the merged writing bundle so the whole paper can be
reviewed from one place.

## Bottom line

The paper experiment package is frozen enough for writing and submission
organization.

- Main evidence for the paper is closed and auditable.
- The original Part 4 manual-label branch is replaced by a deterministic
  hardcase audit package with no new labels.
- The merged freeze bundle now has a single entry point and a stable index.
- Some diagnostics remain partial or internal-only, but they are no longer
  blocking the paper-facing closure.

## 1. Freeze-level checklist

| Part | Name | Status | What is frozen | Canonical file(s) |
|---|---|---|---|---|
| 1 | Protocol / workspace freeze | Complete | Split protocol, baseline registry, corruption spec, run ledger, data-license audit | `00_PROTOCOL/EA_AI_EXTENSION_PROTOCOL.md`, `00_PROTOCOL/BASE_FREEZE_ID`, `00_PROTOCOL/BASELINE_REGISTRY.yaml`, `00_PROTOCOL/CORRUPTION_SPEC.yaml`, `00_PROTOCOL/DATA_LICENSE_AUDIT.md`, `runs/RUN_LEDGER.csv` |
| 2 | External baseline comparison | Complete | Formal cross-method PK on four datasets | `results/external_baseline_comparison.md`, `results/external_baseline_comparison.csv` |
| 3 | Corruption / compensation benchmark | Complete | 192-row corruption matrix and summary | `results/corruption_full_matrix.csv`, `results/corruption_summary.md`, `results/accuracy_reliability_pareto.md`, `results/failure_case_audit.md` |
| 4 | Hardcase audit | Complete by substitute | No new manual labels; deterministic qualitative audit package | `results/hardcase_audit_no_manual_labels.md`, `results/qualitative_case_candidates_seed2028.md`, `results/qualitative_cases/README.md`, `results/qualitative_cases/manifest.json`, `results/figures/qualitative_bev_README.md`, `results/figures/qualitative_bev_QA.md` |
| 5 | Merge / freeze wrapper | Complete | Single writing-facing entry point and index | `README.md`, `FREEZE_INDEX.md`, `paper_frozen_snapshot_20260729.md`, `paper_all_frozen_experiments_record_20260728.md` |

## 2. Experiment inventory by paper role

| Area | Representative evidence | Status | Paper role | Notes |
|---|---|---|---|---|
| Main four-dataset comparison | `results/main_comparison_13x4_ap_report.md`, `results/13x4_ap_evidence.json`, `results/13x4_ap_results.csv` | Frozen / supported | Main paper | Baseline vs strict route vs high-performance route |
| Strict route paired stats | `results/final_experiment_audit_and_manuscript_plan.md`, `results/paper_experiment_status.md` | Frozen / supported | Main paper | 12/12 positive paired comparisons |
| Sequential ablation | `results/final_ablation_report.md`, `results/fair_ablation_report.md`, `results/fair_ablation_seed_results.csv` | Frozen / supported | Main paper | Seed2028 progressive chain is the main ablation narrative |
| High-performance route | `results/paper_experiment_status.md`, `results/final_experiment_audit_and_manuscript_plan.md` | Frozen / supported | Supplement / main note | Best macro mean, but not strict no-regression |
| Calibration diagnostics | `results/diagnostic_gate_summary.md`, `results/diagnostic_all_seed2028.md`, `results/calibration_report_seed2028.md`, `results/calibration_comparison_seed2028.md` | Frozen / supported | Supplement and boundary analysis | q55 calibration is supportive; strict route calibration is not the main claim |
| Efficiency / latency | `results/efficiency_report.md`, `results/detector_latency_from_logs.md`, `results/t1_t11_closure_memo.md` | Frozen / supported | Main paper + supplement | Parameter and runtime cost are explicit |
| Point-dropout robustness | `results/point_dropout_voting_gate_summary.md`, `results/robustness_acceptance_final_20260727.md` | Frozen / supported | Supplement | Average-positive, not all-cell strict |
| Corruption grid / robustness | `results/corruption_summary.md`, `results/corruption_full_matrix.csv` | Frozen / complete | Supplement / diagnostic | Closed matrix, useful for reliability discussion |
| Qualitative BEV cases | `results/qualitative_case_candidates_seed2028.md`, `results/qualitative_cases/README.md`, `results/figures/qualitative_bev_README.md`, `results/figures/qualitative_bev_QA.md` | Frozen / complete | Main qualitative evidence | Selected cases are traceable and QA-passed |
| Hardcase audit substitute | `results/hardcase_audit_no_manual_labels.md` | Frozen / complete by substitute | Supplement / appendix | Replaces manual-label Part 4 |
| Range / sparsity diagnostics | `results/range_sparsity_diagnostic_seed2028.md`, `results/diagnostic_all_seed2028.md` | Frozen / partial | Internal / selective | Mixed diagnostic behavior; not a universal claim |
| Physical evidence ranking | `results/physical_evidence_rank_screen.md` | Frozen / partial | Internal / selective | Supporting analysis, not a final acceptance gate |
| RGPC / component screens | `results/rgpc_family_screen_gate_report.md`, `results/component_ablation_screen_report.md` | Frozen / partial | Internal | Screen-only / partial evidence |
| Sensitivity sweeps | `results/voting_sensitivity_summary.md`, `results/diagnostic_gate_summary.md` | Frozen / partial | Supplement / internal | Useful boundary evidence, not a global closure package |
| Convergence audit | `results/convergence_report_m0_radarpillar_seed2027_2030.md` | Frozen / partial | Internal | Event-file audit, not a final convergence bundle |
| Failed sweeps / weak variants | `results/final_experiment_audit_and_manuscript_plan.md`, `results/pre_submission_claim_risk_audit.md` | Frozen / internal | Internal only | Keep for reviewer defense, not main paper |

## 3. Checklist by claim tier

### Main paper

- [x] Four-dataset formal comparison
- [x] Strict route is 12/12 positive against RDAR
- [x] Sequential ablation is frozen and readable
- [x] Efficiency and runtime cost are explicit
- [x] Qualitative BEV evidence is frozen and QA-passed

### Supplement / secondary analysis

- [x] High-performance route comparison
- [x] Calibration diagnostics
- [x] Point-dropout robustness
- [x] Corruption-grid reliability matrix
- [x] Hardcase audit substitute

### Internal / boundary evidence

- [x] Range / sparsity diagnostics
- [x] Physical evidence ranking
- [x] RGPC and component screens
- [x] Sensitivity sweeps
- [x] Convergence audit
- [x] Failed sweeps and weak controls retained for defense

## 4. What is still not meant to be promoted as a main claim

These items are frozen, but should remain internal or selective unless the
paper is rewritten around them:

- global range/sparsity superiority
- strict route calibration superiority
- dropout prediction voting as a main robustness result
- any claim that the current voting stage is free in runtime
- any claim that the high-performance route is strict no-regression

## 5. Final record

If you need the shortest possible summary for the notebook or lab log, use:

> The paper experiment package is frozen. Main comparison, sequential ablation,
> corruption benchmark, qualitative evidence, calibration, efficiency, and the
> hardcase audit substitute are all archived in the merged freeze bundle at
> `paper_freeze_20260729_0359`.

