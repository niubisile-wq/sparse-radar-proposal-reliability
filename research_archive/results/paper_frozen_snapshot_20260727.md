# Paper Frozen Snapshot

Date: 2026-07-27

This file freezes the current paper-facing experiment state. It is the single
place to check what the paper is trying to say, which experiments exist, and
which evidence files currently support each part of the story.

## 1. One-sentence story

This paper argues that a sparse 4D radar detector can be made stronger and
more trustworthy by restoring the historical four-module design, then showing
that the same protocol improves main AP, cross-dataset transfer, robustness,
calibration, and efficiency under fair comparisons.

## 2. Story line

The intended narrative is:

1. protocol is correct and the baseline is strong;
2. the four modules are individually useful and interact sensibly;
3. the same method improves all four core datasets;
4. the method transfers across datasets;
5. the method is robust to dropout and corruption;
6. the method is reasonably calibrated and efficient;
7. the comparison is fair and reproducible.

This matches the plan-level chain:
`protocol correct -> strong baseline -> four modules work -> four-dataset gain ->
cross-domain generalization -> robust / trustworthy / deployable -> fair SOTA`.

## 3. Frozen experiment map

### Main results

- [T1 main comparison](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/main_comparison_13x4_ap_report.md)
- [T2 sequential ablation](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/final_ablation_report.md)
- [T3 standalone factorial](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/final_ablation_report.md)

### Module and geometry analyses

- [T4 component ablation](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/component_ablation_screen_report.md)
- [T5 RGPC ablation](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/rgpc_family_screen_gate_report.md)
- [T6 range analysis](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/range_sparsity_diagnostic_seed2028.md)
- [T7 sparsity analysis](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/range_sparsity_diagnostic_seed2028.md)
- [T8 physical analysis](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/physical_evidence_rank_screen.md)

### Robustness, trust, deployment

- [T9 point-dropout robustness](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/point_dropout_voting_gate_summary.md)
- [T10 RCS / Doppler robustness](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/robustness_acceptance_final_20260727.md)
- [T11 efficiency](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/efficiency_report.md)
- [T12 calibration](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/calibration_full_m1_m2_m3_m4_seed2028.md)

### Supporting / remaining narrative material

- [T13 convergence](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/convergence_report_m0_radarpillar_seed2027_2030.md)
- [T14 qualitative](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/qualitative_case_candidates_seed2028.md)
- [T15 sensitivity](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/voting_sensitivity_summary.md)

## 4. Current closure state

The plan checkbox block is fully checked: `14/14`.

The matrix is still mixed:

- supported: `T1`, `T3`, `T11`, `T12`
- partial / screening: `T2`, `T4`, `T5`, `T6`, `T7`, `T8`, `T9`, `T10`, `T13`, `T14`, `T15`

That means:

- the paper can be written now;
- the paper should still treat some rows as screening/supporting evidence;
- the final manuscript claims should stay aligned with the strongest closed rows.

## 5. What each experiment is for

### T1 Main comparison

Shows the method is competitive on the four core datasets under the chosen
fair protocol.

### T2 Sequential ablation

Shows the effect of adding the modules in order, so the method is not a
single-shot score jump.

### T3 Standalone factorial

Shows the four-module interaction is real rather than accidental.

### T4 and T5

Break the method down into component-level and identity-safe variants so the
story can say which parts matter.

### T6 and T7

Show the method is not only good on the full set, but also behaves sensibly
with respect to range and sparsity.

### T8, T9, T10

Provide physical robustness evidence:

- physical evidence ranking;
- point dropout;
- RCS / Doppler corruption.

### T11

Shows the method is not too expensive to run.

### T12

Shows the method is reasonably calibrated and not just high AP.

### T13

Shows the method converges in a reasonable way and does not depend on a
one-off lucky epoch.

### T14

Provides qualitative examples for recoveries, suppressions, and failure modes.

### T15

Checks sensitivity to key levers so the paper can say where the method is
stable and where it is not.

## 6. Recommended writing order

1. Abstract, intro, and method: write from the story line.
2. Main comparison and four-module story: `T1` to `T3`.
3. Sensitivity / geometry / module analyses: `T4` to `T8`.
4. Robustness, calibration, efficiency: `T9` to `T12`.
5. Convergence, qualitative, and remaining sensitivity: `T13` to `T15`.
6. Keep the screening language explicit for rows that are not fully closed.

## 7. Files to open first next time

- [plan completion audit](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/plan_completion_audit_20260727.md)
- [matrix closure map](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/matrix_closure_map_20260727.md)
- [final experiment matrix](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/FINAL_EXPERIMENT_MATRIX.md)
- [robustness final package](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/robustness_acceptance_final_20260727.md)

## 8. Frozen note

This is a frozen snapshot, not an active experiment queue.

If you resume work later, use this file as the index and only change the
paper-facing wording or supporting presentation unless you explicitly decide
to reopen experiment execution.

