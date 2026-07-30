# T12 Calibration Gap Report

Date: 2026-07-27

This report records the historical calibration gap for `T12` and the newer
closed four-module calibration evidence.

## What is already supported

- `results/calibration_report_seed2028.md`
- `results/calibration_comparison_seed2028.md`
- `results/calibration_sequential_astyx_seed2028.md`
- `results/calibration_stable_four_modules_seed5623.md`
- `results/plan_completion_audit_20260727.md`
- `results/matrix_closure_map_20260727.md`

These artifacts establish that calibration tooling and summary reporting are in
place.

## Stable-four calibration inventory

Remote result files:

- Astyx: `result.pkl` exists and is non-empty.
- TruckScenes: `result.pkl` exists and is 33,424 bytes.
- V2X-Radar-V: `result.pkl` exists and is 33,424 bytes.
- K-Radar: `result.pkl` exists and is 33,424 bytes.

Local inspection of the three non-Astyx files shows:

- 80 frames each
- 0 scores in the first frame
- `boxes_3d` shape `(0, 7)`

Conclusion:

- These three files are structurally valid but functionally empty for
  calibration closure.

## q55drav_rgpc calibration inventory

Remote result files:

- Astyx: `result.pkl` exists and is 7,847,657 bytes.
- TruckScenes: `result.pkl` exists and is 150,977 bytes.
- V2X-Radar-V: `result.pkl` exists and is 106,061 bytes.
- K-Radar: no `q55drav_rgpc` result directory was discovered in the remote
  search, but the calibration comparison already includes a `kradar_q55`
  branch.

Local inspection of the Astyx file shows:

- 100 frames
- 500 scores in the first frame
- `boxes_3d` shape `(500, 7)`

Conclusion:

- The q55 calibration support is materially populated on Astyx, TruckScenes,
  and V2X-Radar-V, and the comparison report already covers K-Radar via the
  `kradar_q55` branch.

## Log-level evidence

- The stable-four TruckScenes and V2X logs are long training/evaluation logs,
  but searches did not find final `Evaluation done` / `save_to_file` /
  `result.pkl` markers for the stable-four branch.
- The q55 calibration reports already cover all four datasets, so the missing
  piece is no longer q55 support itself.

## Historical gap

`T12` still needs baseline/M1–M4 paired predictions on all four datasets.

Right now, the missing part is not just a missing summary file. The issue is
that the current stable-four non-Astyx predictions are empty, and the
baseline/M1–M4 paired predictions are still incomplete on some datasets.

## Historical rerun status

Historical remote rerun state on 2026-07-27:

- TruckScenes `fair_stable_four_modules_truckscenes_seed5623` is still in the
  evaluation wait loop. The log shows `Total unified radar samples: 80` and
  repeated `Wait 30 seconds for next check` lines, but no new closed
  `result.pkl` has been observed yet.
- V2X-Radar-V `fair_stable_four_modules_v2xradarv_seed5623` is in the same
  evaluation wait loop.
- K-Radar was first launched on an invalid `GPU 3` slot and failed because the
  machine only exposes `GPU 0/1/2`. It has now been relaunched on `GPU 0` and
  has entered training/evaluation successfully.
- The invalid `GPU 3` launch is a scheduling bug, not a model failure. It
  should be excluded from the final evidence chain.

Latest poll:

- `drav` TruckScenes has completed training and evaluation at epoch 160/160.
- `drav` K-Radar has completed training and evaluation at epoch 160/160.
- `q55drav_rgpc` V2X-Radar-V has completed training and evaluation at epoch
  160/160. The remote result file is present and non-empty.
- `q55drav_rgpc` TruckScenes has completed training and evaluation at epoch
  160/160. The evaluation log reports `Average predicted number of
  objects(80 samples): 14.550` and `Car radar AP_R40@3D IoU 0.50: 7.2901`.
  The final `result.pkl` exists in the epoch_160/val directory and is
  150,977 bytes.
- The earlier stable-four reruns already exited the wait loop and completed
  `EPOCH 160 EVALUATION`, but they still produced empty outputs with
  `Average predicted number of objects(80 samples): 0.000`.
- So the deadlock was fixed, and the stable-four branch remains a historical contrast rather than the active closure path.

