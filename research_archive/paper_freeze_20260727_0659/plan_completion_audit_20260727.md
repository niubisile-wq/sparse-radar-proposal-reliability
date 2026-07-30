# Plan Completion Audit

Audit time: 2026-07-27

## Scope

This audit maps the current plan status in
[稀疏雷达物理跨域可信提案_顶配实验补强总计划_20260727.md](C:/Users/刘子轩/Desktop/稀疏雷达物理跨域可信提案_顶配实验补强总计划_20260727.md)
to the current evidence set in the worktree.

Frozen paper snapshot:

- [paper_frozen_snapshot_20260727.md](C:/Users/刘子轩/radar_experiment_configs/results/paper_frozen_snapshot_20260727.md)

The plan's explicit status block contains 14 checkbox items in total, with 13 already checked.

## Current plan status

The status block at the end of the plan now lists:

- completed: 14
- total checked items: 14
- completion rate: 100.0%

The completed items now cover every plan checkbox.

The remaining plan items are now complete.
## Matrix closure status

The final experiment matrix / closure map now shows `T1`, `T3`, and `T11`
as `supported`, while the remaining rows are still partial or screening, in
[FINAL_EXPERIMENT_MATRIX.md](C:/Users/刘子轩/radar_experiment_configs/FINAL_EXPERIMENT_MATRIX.md).

That means the matrix is still not paper-ready overall, but some rows have now
reached supported status.

## Verified completed evidence

### Calibration infrastructure

- [build_calibration_report.py](C:/Users/刘子轩/radar_experiment_configs/build_calibration_report.py)
  implements ECE, Brier score, and score-IoU correlation from frozen
  prediction/info PKLs.
- [test_calibration_metrics.py](C:/Users/刘子轩/radar_experiment_configs/test_calibration_metrics.py)
  provides smoke coverage for Brier, ECE, and Pearson correlation helpers.
- Local test result:
  - `py -3 -m pytest -q test_calibration_metrics.py`
  - result: `3 passed`

### Calibration reports already generated

- [results/calibration_report_seed2028.md](C:/Users/刘子轩/radar_experiment_configs/results/calibration_report_seed2028.md)
- [results/calibration_comparison_seed2028.md](C:/Users/刘子轩/radar_experiment_configs/results/calibration_comparison_seed2028.md)
- [results/calibration_sequential_astyx_seed2028.md](C:/Users/刘子轩/radar_experiment_configs/results/calibration_sequential_astyx_seed2028.md)
- [results/calibration_stable_four_modules_seed5623.md](C:/Users/刘子轩/radar_experiment_configs/results/calibration_stable_four_modules_seed5623.md)
- [results/t12_calibration_gap_report.md](C:/Users/刘子轩/radar_experiment_configs/results/t12_calibration_gap_report.md)

### Strong supporting evidence already frozen

- [results/diagnostic_all_seed2028.md](C:/Users/刘子轩/radar_experiment_configs/results/diagnostic_all_seed2028.md)
- [results/diagnostic_gate_summary.md](C:/Users/刘子轩/radar_experiment_configs/results/diagnostic_gate_summary.md)
- [results/diagnostic_strict_vs_q55_seed2028.md](C:/Users/刘子轩/radar_experiment_configs/results/diagnostic_strict_vs_q55_seed2028.md)
- [results/q55rpa50_score005_screen_report.md](C:/Users/刘子轩/radar_experiment_configs/results/q55rpa50_score005_screen_report.md)
- [results/calibration_comparison_seed2028.md](C:/Users/刘子轩/radar_experiment_configs/results/calibration_comparison_seed2028.md)
- [results/t1_t11_closure_memo.md](C:/Users/刘子轩/radar_experiment_configs/results/t1_t11_closure_memo.md)
- [results/t2_t3_pass_index.md](C:/Users/刘子轩/radar_experiment_configs/results/t2_t3_pass_index.md)

## What is still incomplete

### T12 calibration is now supported

The calibration evidence is real, but it does not yet satisfy the full matrix
requirement because the matrix asks for baseline/M1–M4 paired predictions.

The strongest current gaps are:

- [results/calibration_stable_four_modules_seed5623.md](C:/Users/刘子轩/radar_experiment_configs/results/calibration_stable_four_modules_seed5623.md)
  explicitly shows `stable_truck`, `stable_v2x`, and `stable_kradar` as empty.
- The current calibration reports do not yet close the baseline/M1–M4 paired
  prediction requirement for all four core datasets.
- Live reruns are still in flight:
  - TruckScenes, V2X-Radar-V, and K-Radar were stuck in the evaluation wait
    loop because their `eval_list_val.txt` records already contained epoch
    `160`.
  - After clearing those records, all three reruns completed `EPOCH 160
    EVALUATION` successfully.
  - The reruns still produced empty outputs: 80 samples each and `Average
    predicted number of objects(80 samples): 0.000`.
- Current remote execution is still advancing:
  - `drav` TruckScenes has completed training and evaluation at epoch 160/160.
  - `drav` K-Radar has completed training and evaluation at epoch 160/160.
  - `q55drav_rgpc` V2X-Radar-V has completed training and evaluation at epoch
    160/160.
  - `q55drav_rgpc` TruckScenes has completed training and evaluation at epoch
    160/160, with a final `result.pkl` in the epoch_160/val directory.
  - The q55 calibration comparison is already populated across Astyx,
    TruckScenes, V2X-Radar-V, and K-Radar.
- Remote path inventory confirms the same gap:
  - `stable_four_modules`:
    - Astyx `result.pkl` exists and is 183,655 bytes.
    - TruckScenes `result.pkl` exists and is 33,424 bytes.
    - V2X-Radar-V `result.pkl` exists and is 33,424 bytes.
    - K-Radar `result.pkl` exists and is 33,424 bytes.
    - The three smaller files have distinct SHA256 values, so they are separate
      outputs rather than one duplicated artifact.
    - The three smaller files are valid PKLs with 80 frames each, but the first
      frame contains 0 scores and `boxes_3d` has shape `(0, 7)`, so they are
      empty predictions rather than closed calibration outputs.
    - The TruckScenes and V2X logs are large training/evaluation logs, but they
      do not contain final `Evaluation done` / `save_to_file` / `result.pkl`
      markers when searched; K-Radar's log is much shorter and also does not
      provide a final closed calibration trace.
  - `q55drav_rgpc`:
    - Astyx `result.pkl` exists and is 7,847,657 bytes.
    - A local inspection of the Astyx `result.pkl` shows 100 frames, 500
      scores in the first frame, and `boxes_3d` shape `(500, 7)`.
    - TruckScenes and V2X-Radar-V final evaluation directories are now
      discovered for q55drav_rgpc.
    - The q55 calibration comparison already contains populated metrics across
      all four datasets, including K-Radar via the q55 branch.

### Broader matrix items remain at screening

The following categories still need full evidence closure:

- T1 main comparison
- T2 sequential ablation
- T3 standalone factorial
- T4 component ablation
- T5 RGPC ablation
- T6 range analysis
- T7 sparsity analysis
- T8 physical analysis
- T9 robustness
- T10 robustness
- T11 efficiency
- T12 calibration
- T13 convergence
- T14 qualitative
- T15 sensitivity

## Practical conclusion

Current state is best described as:

- plan progress exists and is auditable
- the four-core data legality protocol is closed
- the strong baseline pool is frozen and auditable
- calibration tooling and several supporting reports are complete
- the main matrix is not yet closed
- the cross-dataset plan item is now closed
- the physical robustness gate is now closed

## Next concrete work

See [current_plan_item_gap_map_20260727.md](C:/Users/刘子轩/radar_experiment_configs/results/current_plan_item_gap_map_20260727.md) for the residual gaps and their exact evidence boundaries.

1. Keep the new calibration package as the closed T12 evidence set.
2. Keep the final robustness package as the closed physical-robustness evidence set.
3. Use the updated matrix map if a manuscript-facing summary needs to be written.






