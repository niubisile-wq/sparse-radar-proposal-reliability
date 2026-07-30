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

Exact `pc_idx` overlap is zero for all four conversions. The adjacent-ID
counts are an audit signal, not proof that adjacent frames belong to the same
scene; the missing scene metadata prevents that determination. The manuscript
now treats all results as evidence under a frame-level frozen protocol and
explicitly does not claim scene-disjoint or deployment-level generalization.

The audit script is `scripts/audit_frozen_split_overlap.py`.
