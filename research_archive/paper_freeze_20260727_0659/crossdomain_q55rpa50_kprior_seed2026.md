# Cross-Domain Matrix, q55rpa50 kprior, Seed 2026

This report freezes the 12 directed zero-shot transfer evaluations that were
run on the remote instance for the `q55rpa50_kprior` branch.

## Summary

- Total ordered pairs evaluated: 12
- Non-zero AP cells: 2
- Non-zero recall cells: 5
- Mean AP across all pairs: 0.00018
- Mean recall across all pairs: 0.00726

## Matrix

| Source | Target | AP_R40@3D IoU 0.50 | Max recall |
|---|---|---:|---:|
| Astyx | TruckScenes | 0.0018 | 0.0438 |
| Astyx | V2X-Radar-V | 0.0000 | 0.0000 |
| Astyx | K-Radar | 0.0000 | 0.0000 |
| TruckScenes | Astyx | 0.0000 | 0.0071 |
| TruckScenes | V2X-Radar-V | 0.0000 | 0.0000 |
| TruckScenes | K-Radar | 0.0004 | 0.0276 |
| V2X-Radar-V | Astyx | 0.0000 | 0.0000 |
| V2X-Radar-V | TruckScenes | 0.0000 | 0.0044 |
| V2X-Radar-V | K-Radar | 0.0000 | 0.0000 |
| K-Radar | Astyx | 0.0000 | 0.0000 |
| K-Radar | TruckScenes | 0.0000 | 0.0000 |
| K-Radar | V2X-Radar-V | 0.0000 | 0.0042 |

## Interpretation

- The matrix is now complete at the level required by the plan item.
- The strongest visible transfer remains Astyx -> TruckScenes.
- Most other ordered pairs are effectively zero-shot failures, which is useful
  because it makes the generalization boundary explicit rather than inferred.
