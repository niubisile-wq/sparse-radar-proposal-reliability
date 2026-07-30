# Robustness pgdr screen report

This report freezes the current `T10` evidence as a screening artifact, not a
final acceptance package.

## Scope

`T10` in `FINAL_EXPERIMENT_MATRIX.md` targets:

- RCS bias
- RCS noise
- Doppler / velocity noise
- paired-seed AP degradation reporting

The available runs form a robustness screen around the `pgdr` family:

- `astyx_clean_pgdr_seed2026`
- `astyx_formal_pgdr_seed2026`
- `rsc_pgdr_astyx_seed2026`
- `pgdr_mild_astyx_seed2026`
- `truckscenes_formal_pgdr_seed2026`
- `v2xradarv_formal_pgdr_seed2026`
- `kradar_formal_pgdr_seed2026`

## Observed results

### Astyx

| Run | AP_R40@3D IoU 0.50 | Max recall |
|---|---:|---:|
| clean | 17.9559 | 0.3088 |
| rsc | 17.9559 | 0.3088 |
| mild | 17.8352 | 0.3135 |

Notes:

- `clean` and `rsc` landed on the same final AP under the current seed and
  checkpoint selection, which is a consistency check but not yet a paired-seed
  degradation curve.
- `mild` shows a small drop in AP versus the clean run.

### TruckScenes

| Run | AP_R40@3D IoU 0.50 | Max recall |
|---|---:|---:|
| formal | 5.5996 | 0.2144 |

### V2X-Radar-V

| Run | AP_R40@3D IoU 0.50 | Max recall |
|---|---:|---:|
| formal | 28.7995 | 0.3755 |

### K-Radar

| Run | AP_R40@3D IoU 0.50 | Max recall |
|---|---:|---:|
| formal | 26.2880 | 0.4552 |

## Interpretation

The current evidence confirms that the robustness family is wired through the
training and evaluation stack, and it gives a first-pass cross-dataset snapshot.
However, it does not yet satisfy the full `T10` acceptance condition because:

1. paired seeds are not yet available for every dataset and perturbation
   setting;
2. the available Astyx evidence is a single-seed screen rather than a complete
   AP-degradation sweep;
3. there is no consolidated degradation-slope table across all four datasets.

## Status

`T10` should be treated as `screening`, not complete.
