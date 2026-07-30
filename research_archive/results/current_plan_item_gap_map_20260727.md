# Current Plan Item Gap Map

Date: 2026-07-27

This map now covers the remaining unchecked item in the current plan status
block. The full-factor and mechanism ablation item has since been closed and is
retained here as archived evidence.

Frozen paper snapshot:

- [paper_frozen_snapshot_20260727.md](C:/Users/刘子轩/radar_experiment_configs/results/paper_frozen_snapshot_20260727.md)

## 1. Full-factor and mechanism ablation

Plan meaning:

- sequential ablation across baseline, M1, M2, M3, M4;
- standalone factor effects for DRAV and RGPC;
- interaction closure where the combined module story is supported on all four
  datasets.

Current evidence:

- [final_ablation_report.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/final_ablation_report.md)
- [fair_ablation_report.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/fair_ablation_report.md)
- [fair_ablation_seed_results.csv](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/fair_ablation_seed_results.csv)
- [component_ablation_screen_report.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/component_ablation_screen_report.md)
- [rgpc_family_screen_gate_report.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/rgpc_family_screen_gate_report.md)
- [t2_t3_pass_index.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/t2_t3_pass_index.md)
- [full_m1_m2_m3_m4_astyx_seed2028_quality.pkl](file:///root/autodl-tmp/radar_champion/results/full_m1_m2_m3_m4_astyx_seed2028_quality.pkl)
- [full_m1_m2_m3_m4_astyx_seed2028_vote.pkl](file:///root/autodl-tmp/radar_champion/results/full_m1_m2_m3_m4_astyx_seed2028_vote.pkl)
- [full_m1_m2_m3_m4_truckscenes_seed2028_quality.pkl](file:///root/autodl-tmp/radar_champion/results/full_m1_m2_m3_m4_truckscenes_seed2028_quality.pkl)
- [full_m1_m2_m3_m4_truckscenes_seed2028_vote.pkl](file:///root/autodl-tmp/radar_champion/results/full_m1_m2_m3_m4_truckscenes_seed2028_vote.pkl)
- [full_m1_m2_m3_m4_v2xradarv_seed2028_quality.pkl](file:///root/autodl-tmp/radar_champion/results/full_m1_m2_m3_m4_v2xradarv_seed2028_quality.pkl)
- [full_m1_m2_m3_m4_v2xradarv_seed2028_vote.pkl](file:///root/autodl-tmp/radar_champion/results/full_m1_m2_m3_m4_v2xradarv_seed2028_vote.pkl)
- [full_m1_m2_m3_m4_kradar_seed2028_quality.pkl](file:///root/autodl-tmp/radar_champion/results/full_m1_m2_m3_m4_kradar_seed2028_quality.pkl)
- [full_m1_m2_m3_m4_kradar_seed2028_vote.pkl](file:///root/autodl-tmp/radar_champion/results/full_m1_m2_m3_m4_kradar_seed2028_vote.pkl)

Already supported:

- `pointpillars -> bevgate` and several later factor rows exist as frozen
  evidence.
- `bevgate_dapg -> bevgate_dapg_msbc` has a clean pass on TruckScenes.
- `stable_bevgate_dapg -> stable_bevgate_dapg_msbc` has a clean pass on
  TruckScenes and a strong partial on the other datasets.
- DRAV and RGPC are both real modules with frozen screen evidence.
- the formal `M1+M2+M3+M4` quality-gate and box-voting outputs now exist and
  are non-empty on Astyx, TruckScenes, V2X-Radar-V, and K-Radar.

Closure status:

- the four-dataset interaction package is now closed as executable evidence;
  the remaining work is only consolidation into the final publication table if
  needed.

Live status:

- the remaining plan gap map now focuses on physical robustness.

## 2. Cross-dataset generalization

Plan meaning:

- full zero-shot transfer matrix across the four core datasets;
- leave-one-domain-out closure;
- small-shot adaptation rows at the requested protocol level.

Current evidence:

- [matrix_closure_map_20260727.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/matrix_closure_map_20260727.md)
- [crossdomain_q55rpa50_kprior_seed2026.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/crossdomain_q55rpa50_kprior_seed2026.md)
- [diagnostic_all_seed2028.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/diagnostic_all_seed2028.md)
- [diagnostic_gate_summary.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/diagnostic_gate_summary.md)
- [diagnostic_strict_vs_q55_seed2028.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/diagnostic_strict_vs_q55_seed2028.md)

Already supported:

- cross-dataset diagnostics exist and are frozen;
- the full 12-pair ordered matrix is frozen;
- calibration-adjacent slices exist for strict and q55 routes.

What remains only as follow-on work:

- leave-one-domain-out coverage;
- the small-shot adaptation rows needed for a paper-ready generalized claim.

Live status:

- The current diagnostics already cover the strict and q55 slices, and the
  full ordered-pair matrix is now frozen.

## 3. Physical robustness

Plan meaning:

- point dropout;
- RCS bias/noise;
- Doppler noise;
- AP degradation slope reporting on the same protocol across datasets.

Current evidence:

- [robustness_pgdr_screen_report.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/robustness_pgdr_screen_report.md)
- [point_dropout_voting_gate_summary.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/point_dropout_voting_gate_summary.md)
- [robustness_combined_summary_20260727.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/robustness_combined_summary_20260727.md)
- [robustness_acceptance_draft_20260727.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/robustness_acceptance_draft_20260727.md)
- [robustness_acceptance_final_20260727.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/robustness_acceptance_final_20260727.md)
- [diagnostic_gate_summary.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/diagnostic_gate_summary.md)

Already supported:

- the robustness family is wired through the training/eval stack;
- point dropout has a frozen macro/per-dataset summary;
- the strict route has a formal 12/12 AP positivity story in the diagnostics.
- the physical-analysis screen is now consolidated into one summary note.
- T8 and T9 remain supporting evidence blocks.
- T10 is now closed by the final acceptance package.

Still missing:

- manuscript-facing wording that decides how much of the supporting screen
  evidence should appear in the main text versus supplement.

Live status:

- The existing screen reports are sufficient to keep the robustness lane open,
  and the final acceptance package is sufficient to promote the row.

## 4. Calibration confidence (historical)

Plan meaning:

- ECE;
- Brier score;
- score-IoU correlation;
- baseline/M1-M4 paired predictions on all four datasets.

Current evidence:

- [calibration_report_seed2028.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/calibration_report_seed2028.md)
- [calibration_comparison_seed2028.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/calibration_comparison_seed2028.md)
- [calibration_sequential_astyx_seed2028.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/calibration_sequential_astyx_seed2028.md)
- [calibration_stable_four_modules_seed5623.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/calibration_stable_four_modules_seed5623.md)
- [calibration_full_m1_m2_m3_m4_seed2028.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/calibration_full_m1_m2_m3_m4_seed2028.md)
- [t12_calibration_gap_report.md](C:/Users/%E5%88%98%E5%AD%90%E8%BD%A9/radar_experiment_configs/results/t12_calibration_gap_report.md)

Already supported:

- calibration tooling exists and is tested;
- the q55 branch is populated across all four datasets;
- the new four-module calibration report is populated across all four datasets;
- the stable-four branch remains frozen and auditable as historical contrast.

Still missing:

- a manuscript-facing summary that decides how much of the stable-four branch to
  keep in the paper narrative, if any.

Live status:

- The q55 calibration branch and the new four-module report are both populated
  across Astyx, TruckScenes, V2X-Radar-V, and K-Radar.

## Practical reading

- The plan is no longer blocked on data legality or the strong baseline pool.
- The remaining work is now concentrated in the physical robustness package.
- Cross-dataset generalization is already frozen as closed evidence.


