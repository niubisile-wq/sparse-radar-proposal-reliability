# Fair Ablation Next Actions

Date: 2026-07-28

This note turns the remaining fair-ablation gaps into an execution order.

## 1. Residual classes

From the latest gap map:

- 0 rows are `retryable`
- 0 rows are `failed evidence`
- 0 rows are `blocked`

## 2. Failed evidence items

None.

Recommended action:

- keep the logs and result artifacts;
- mark them as failed-model evidence;
- only rerun if a paper claim absolutely needs a stronger variant.

Completed reruns:

- `bevgate / K-Radar / 3407` has finished rerunning and now has AP `39.3228`.
- `bevgate_dapg_msbc / K-Radar / 2028` has finished rerunning and now has AP
  `48.7151`.
- `stable_bevgate_dapg_msbc / K-Radar / 2029` has finished rerunning and now
  has AP `52.5104`.
- `stable_four_modules / K-Radar / 2036` has finished rerunning and now has AP
  `58.4910`.
- `atss5 / Astyx / 2028` has finished rerunning with
  `AP_R40@3D IoU 0.50: 0.0000`.
- `stable_bevgate_dapg_msbc / K-Radar / 5623` has finished rerunning with
  `AP_R40@3D IoU 0.50: 54.1047`.
- `atss / K-Radar / 2028` has finished rerunning with
  `AP_R40@3D IoU 0.50: 0.0000`.
- `bevgate_replay10 / kradar / 2028` has finished rerunning on GPU0 and the
  new `result.pkl` is already saved.
- `corner / truckscenes / 2028` has finished rerunning on GPU1 and the new
  `result.pkl` is already saved.
- `rccg / kradar / 2028` has finished rerunning on GPU2 and the new
  `result.pkl` is already saved.
- `atss / truckscenes / 2028` has completed rerunning with
  `AP_R40@3D IoU 0.50: 0.0000`.
- `iouaware_radarreplay / kradar / 2028` has completed rerunning with
  `AP_R40@3D IoU 0.50: 46.6789`.
- `iouaware_radarreplay / v2xradarv / 2028` has completed rerunning with
  `AP_R40@3D IoU 0.50: 38.5645`.
- `rpa45 / truckscenes / 2028` has completed rerunning with
  `AP_R40@3D IoU 0.50: 12.0227`.
- `rpa55 / truckscenes / 2028` has completed rerunning on GPU1 and produced
  `AP_R40@3D IoU 0.50: 14.2971`.
- No waiting rows remain in the TruckScenes queue.

Priority order:

1. No residual rows remain in the current CSV

## 5. Suggested routing

- `retryable` rows: none remain in the current CSV
- `blocked` rows: none remain in the current CSV
- `failed evidence` rows: none remain in the current CSV

## 6. Current practical conclusion

The CSV is now closed and can be used as finalized evidence packaging.
