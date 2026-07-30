# Frozen split and potential temporal leakage audit

The converted info files were inspected directly on the instance. Every
train/validation pair has zero exact overlap in the available `point_cloud.pc_idx`
field, but the files do not contain a scene, sequence, vehicle, or timestamp
identifier. Therefore exact frame-ID disjointness cannot establish
scene-level disjointness.

| Conversion | Train frames | Validation frames | Train cars | Validation cars | Validation IDs adjacent to train |
|---|---:|---:|---:|---:|---:|
| Astyx | 300 | 100 | 1629 | 531 | 82/100 |
| TruckScenes-mini | 320 | 80 | 7861 | 3950 | 4/80 |
| V2X-Radar-V-400 | 320 | 80 | 1096 | 268 | 1/80 |
| K-Radar-400 | 320 | 80 | 606 | 198 | 80/80 |

Exact `pc_idx` overlap is zero for all four conversions. Here `adjacent` is the
symmetric numeric rule
`abs(val.point_cloud.pc_idx - train.point_cloud.pc_idx) == 1`. It is an audit
signal, not proof that adjacent frames belong to the same scene; `pc_idx` is not
documented as a timestamp in the converted files. The corresponding strict
exclusion sensitivity would retain 18/100 Astyx, 76/80 TruckScenes, 79/80
V2X-Radar-V, and 0/80 K-Radar validation frames. K-Radar therefore has no
estimable AP under this rule. The available archive contains aggregate AP
tables but not a complete per-frame prediction archive for recomputing the main
strict 12-cell endpoint after filtering; no filtered AP is reported. The
generator `scripts/build_adjacency_clean_manifest.py` records exact retained
row indices when the original info files are available.

The manuscript now treats all results as evidence under a frame-level frozen
protocol and explicitly does not claim scene-disjoint or deployment-level
generalization.

The audit script is `scripts/audit_frozen_split_overlap.py`.
