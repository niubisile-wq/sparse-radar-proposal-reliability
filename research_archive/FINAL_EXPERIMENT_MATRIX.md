# Final experiment matrix

This document defines the evidence required after M3/M4 pass. A row is not
paper-ready until its artifact and acceptance condition both exist.

| ID | Experiment | Comparison / breakdown | Required evidence | Status |
|---|---|---|---|---|
| T1 | Main comparison | Published baselines on four datasets | identical split/metric, AP_R40, source citation | screening |
| T2 | Sequential ablation | baseline → M1 → M2 → M3 → M4 | 3 paired seeds, mean±SD, Δ, CI95 | screening |
| T3 | Standalone factorial | DRAV, RGPC, DRAV+RGPC | main effects and interaction per dataset | screening |
| T4 | Component ablation | raw `vr`, fixed vectorization, reliability gate inputs | one-variable-at-a-time paired runs | screening |
| T5 | RGPC ablation | position, density, residual gate, attention | identity-safe variants | screening |
| T6 | Range analysis | 0–20, 20–40, 40–60 m | AP/recall and object count per bin | screening |
| T7 | Sparsity analysis | objects by radar-return quartile | AP/recall, bootstrap CI | screening |
| T8 | Physical analysis | RCS and `|vr|` quartiles | recall and score calibration | screening |
| T9 | Robustness | point dropout 10/20/30% | AP degradation slope | screening |
| T10 | Robustness | RCS bias/noise and Doppler noise | AP degradation, paired seeds | screening |
| T11 | Efficiency | parameters, FLOPs, latency, peak memory | warm-up + 200 timed iterations | screening |
| T12 | Calibration | ECE, Brier score, score–IoU correlation | baseline/M1–M4 paired predictions | screening |
| T13 | Convergence | validation AP and loss vs. epoch | 3-seed curves and time-to-target | screening |
| T14 | Qualitative | recoveries, suppressions, failures | fixed frame list, no cherry-picking | screening |
| T15 | Sensitivity | DRAV/RGPC gates, heads, residual strength | shared global setting across datasets | screening |

## Locked reporting rules

1. The four-dataset test settings and random seeds are fixed before formal
   training.
2. M3 and M4 must each pass all-positive, mean ≥ +1 AP, paired CI95 lower > 0
   on all four datasets.
3. Hyperparameters are global unless a dataset-specific physical constant is
   justified before evaluation.
4. Failed and interrupted runs remain in the ledger; hardware failures are
   rerun unchanged and never counted as model failures.
5. Efficiency uses the same GPU, batch size, precision mode, warm-up, and
   synchronization protocol.
6. Qualitative examples use a deterministic frame list derived before viewing
   candidate outputs.

## Existing automation

- `evaluate_variant_gate.py`: screen/formal paired gate, including
  candidate-vs-candidate references.
- `build_final_ablation_report.py`: T2/T3 table and seed-level provenance CSV.
- `build_calibration_report.py`: prediction-PKL plus info-PKL calibration
  report generator with ECE, Brier, and score-IoU metrics.
- `watch_physics_context_factorial.sh`: conditional screen/formal scheduling.
- `test_physics_gates.py`: self-contained smoke coverage for
  `RangeAwareSpatialGate`, `PhysicsSoftForegroundGate`, and
  `PhysicsGuidedAnisotropicPillarScatter`.
- `test_calibration_metrics.py`: pure-function smoke coverage for Brier, ECE,
  and score correlation helpers.

## Current evidence already available

- `results/point_dropout_voting_gate_summary.md`: point-dropout robustness
  summary with RDAR comparison and per-dropout macro/per-dataset deltas.
- `results/13x4_ap_evidence.json` and `results/13x4_ap_results.csv`: frozen
  four-dataset main-comparison data package backing the publication table.
- `results/main_comparison_13x4_ap_report.md`: frozen four-dataset main
  comparison report with method-to-log mapping and AP_R40 snapshot.
- `results/fair_ablation_report.md` and `results/fair_ablation_seed_results.csv`:
  frozen fair-ablation module and seed ledger covering the broader module family.
- `results/t2_t3_support_digest.md`: compact T2/T3 digest highlighting the
  strongest pass cells and the remaining blockers.
- `results/range_sparsity_diagnostic_seed2028.md`: frozen seed-2028 range and
  sparsity diagnostics with mixed outcome notes.
- `results/diagnostic_all_seed2028.md`: frozen seed-2028 range, sparsity, and
  calibration diagnostics with ECE(hit), score-IoU correlation, and top-10 IoU
  for RDAR / qflr55 / q55rpa50_kprior.
- `results/calibration_report_seed2028.md`: formal calibration report for
  `rdar_q55rpa50_kprior` against the frozen info PKLs, with ECE, Brier, and
  score-IoU metrics.
- `results/calibration_comparison_seed2028.md`: three-way calibration
  comparison across RDAR, M3-like, and q55 variants on all four datasets.
- `results/calibration_sequential_astyx_seed2028.md`: five-stage Astyx
  calibration sequence from baseline to DRAV+RGPC, with ECE, Brier, and
  score-IoU metrics for each stage.
- `results/calibration_stable_four_modules_seed5623.md`: stable-four-modules
  calibration report showing one non-empty Astyx stage and explicit empty
  outputs for TruckScenes / V2X-Radar-V / K-Radar.
- `results/diagnostic_gate_summary.md`: frozen calibration gate summary with
  win/tie/loss counts for recall, range bins, sparsity bins, ECE(hit), and
  score-IoU correlation.
- `results/diagnostic_strict_vs_q55_seed2028.md`: frozen strict-vs-q55
  calibration slice showing the high-performance route as the calibration
  positive variant.
- `results/rgpc_family_screen_gate_report.md`: RGPC family screen evidence
  showing partial and pending cells across variants.
- `results/component_ablation_screen_report.md`: frozen component-ablation
  screen for PVD / DRAV / RGPC / SCPE, with explicit fail and partial cells.
- `results/physical_evidence_rank_screen.md`: frozen physical-analysis screen
  from the evidence-rank sweep over count / center / RCS / Doppler features.
- `results/robustness_pgdr_screen_report.md`: frozen robustness screen for
  `clean` / `mild` / `rsc` / `formal` pgdr-family runs, with explicit
  paired-seed gap notes.
- `results/final_ablation_report.md`: frozen sequential-ablation screen for
  baseline / M1 / M2 / M3 / M4, with incomplete M3/M4 coverage called out.
- `results/efficiency_report.md` and `results/detector_latency_from_logs.md`:
  parameter counts and latency evidence for the strict route and detector logs.
- `results/pre_submission_claim_risk_audit.md`: manuscript-claim boundary audit
  covering efficiency, calibration, dropout, and strict-route wording.
- `results/q55rpa50_score005_screen_report.md`: calibration-adjacent score
  threshold screen for q55rpa50 against RDAR and qflr55.
- `results/plan_completion_audit_20260727.md`: current plan completion audit
  with explicit completed, partial, and blocked evidence mapping.
- `results/matrix_closure_map_20260727.md`: row-by-row closure map for T1-T15
  with current evidence strength and remaining gaps.
- `results/convergence_report_m0_radarpillar_seed2027_2030.md`: event-file
  audit for train loss and validation AP convergence on the m0 seed family.
- `results/qualitative_case_candidates_seed2028.md`: fixed qualitative frame
  candidates for manuscript figures.
- `results/voting_sensitivity_summary.md`: strict voting threshold sensitivity
  grid.
