# Component Ablation Screen Report

This report formalizes the current T4 component-ablation evidence.

## Scope

The T4 row in the experiment matrix asks for one-variable-at-a-time paired runs
around the radar proposal refinement components. The current evidence package is
not a full acceptance pass, but it is sufficient to freeze the present screen.

## Evidence Sources

- `M3_M4_physics_context_design.md`
- `M3_adaptive_assignment_design.md`
- `final_ablation_report.md`
- `final_ablation_seed_results.csv`
- `pvd_vs_rdar_screen_gate.md`
- `pvd_vs_qflr55_screen_gate.md`
- `drav_vs_rdar_screen_gate.json`
- `rgpc_vs_rdar_screen_gate.md`
- `pvd_rgpc_vs_pvd_screen_gate.md`

## Component Map

- PVD: raw radial velocity retained, with Cartesian Doppler decomposition
  appended as the diagnostic fixed-vectorization baseline.
- DRAV: adaptive version of PVD, where the decomposition is reliability
  modulated but never drops the raw measurement.
- RGPC: reliability-gated context aggregation in BEV.

## What Is Frozen

The frozen package shows that these components were actually evaluated and that
the resulting behavior is mixed rather than universally positive.

### PVD

- `pvd` versus `rdar` is complete, but not a pass.
- Astyx and several later comparisons remain negative or pending.
- `pvd` versus `qflr55` is complete, and every available cell is negative.

### DRAV

- `drav` versus `rdar` is incomplete on two datasets and negative on the
  completed cells.
- This is sufficient to keep DRAV in the screen ledger, but not enough for a
  positive claim.

### RGPC

- `rgpc` and `q55rgpc` gates show partial or failing behavior.
- `pvd_rgpc` now has a complete four-dataset screen, and it still shows the
  expected mixed behavior.
- `q55pvd_rgpc` remains partial and still needs the K-Radar lane.

## Representative Gate Snapshot

| Variant | Astyx | TruckScenes | V2X-Radar-V | K-Radar | Current state |
|---|---|---|---|---|---|
| pvd vs rdar | 31.9413 (-2.4127) | 16.1795 (+0.8754) | 41.7123 (+0.3738) | 53.9699 (+1.9428) | complete, fail |
| pvd vs qflr55 | 31.9413 (-5.0905) | 16.1795 (-1.2735) | 41.7123 (-0.8856) | 53.9699 (-5.4988) | complete, fail |
| drav vs rdar | 33.8614 (-0.4926) | pending | 40.2537 (-1.0848) | pending | incomplete, fail |
| rgpc vs rdar | 32.8459 (-1.5081) | pending | pending | pending | incomplete, fail |
| pvd_rgpc vs pvd | 34.4606 (+2.5193) | 12.6728 (-3.5067) | 46.3428 (+4.6305) | 53.4215 (-0.5484) | complete, fail |
| q55pvd_rgpc vs rdar | 34.8820 (+0.5280) | pending | pending | pending | partial |

## Interpretation

T4 is now a frozen screen, but not a formal acceptance:

- the components are real and separately exercised;
- the screen preserves both positive and negative cells;
- the current evidence still fails the one-variable-at-a-time paired requirement
  for every dataset and seed.

## Status

T4 should be treated as `screening`, not `pending`, but it is not complete.
