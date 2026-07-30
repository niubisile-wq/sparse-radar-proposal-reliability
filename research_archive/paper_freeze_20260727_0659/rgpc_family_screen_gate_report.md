# RGPC Family Screen Gate Report

This report formalizes the current T5 evidence for the RGPC family.

## Evidence Sources

- `results/rgpc_vs_rdar_screen_gate.md`
- `results/pvd_rgpc_vs_rdar_screen_gate.md`
- `results/q55rgpc_vs_rdar_screen_gate.md`
- `results/q55pvd_rgpc_vs_rdar_screen_gate.md`
- `results/drav_rgpc_vs_rdar_screen_gate.md`
- `results/q55drav_rgpc_vs_rdar_screen_gate.md`
- `results/final_ablation_report.md`

## Current Screen Snapshot

The current artifacts are sufficient to show that RGPC-family variants were
actually evaluated, but they are not yet complete enough for a final paper
claim. The screen-gate files still show pending cells in most datasets.

| Variant | Astyx | TruckScenes | V2X-Radar-V | K-Radar | Screen status |
|---|---|---|---|---|---|
| rgpc | 32.8459 (-1.5081) | pending | pending | pending | fail / partial |
| pvd_rgpc | 34.4606 (+0.1066) | 12.6728 (-2.6313) | 46.3428 (+5.0043) | pending | partial |
| drav_rgpc | pending | pending | pending | pending | pending |
| q55rgpc | 32.8459 (-1.5081) | pending | pending | pending | fail / partial |
| q55pvd_rgpc | 34.8820 (+0.5280) | pending | pending | pending | partial |
| q55drav_rgpc | pending | pending | pending | pending | pending |

## Interpretation

- The RGPC family is not ready for a final positive claim.
- The screen gate does prove the family was exercised and that some variants
  can improve selected cells while others regress.
- This is enough to move T5 from `pending` to `screening`, but not to `complete`.

## Status

T5 now has frozen screening evidence.
