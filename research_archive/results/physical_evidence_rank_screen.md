# Physical Evidence Rank Screen

This report formalizes the current T8 screen using the evidence-rank sweep.

## Scope

- Seed: 2028
- Sweep source: `run_radar_evidence_rank_screen.sh`
- Evaluation source: `screen_radar_evidence_rank.py`
- Dataset coverage available in the frozen JSON packages:
  - Astyx
  - TruckScenes
  - V2X-Radar-V
  - K-Radar

## What the sweep does

The sweep computes per-box evidence ranks from:

- count
- center occupancy
- median RCS
- Doppler coherence

It then evaluates score reweighting under:

- `mul` and `logit` transforms
- `alpha` sweeps
- range-power sweeps
- mixed evidence combinations such as `count_rcs`, `count_doppler`, and `all`

This is a direct physical-analysis screen, not a post-hoc table edit.

## Frozen JSON packages

- `results/rer_grid_astyx_seed2028.json`
- `results/rer_grid_truckscenes_seed2028.json`
- `results/rer_grid_v2xradarv_seed2028.json`
- `results/rer_grid_kradar_seed2028.json`

## Best observed configurations

| Dataset | Best config | AP |
|---|---|---:|
| Astyx | `rer_all_p0p0_logit_a0p200` | 35.7324 |
| TruckScenes | `rer_count_p0p0_logit_a1p600` | 18.3579 |
| V2X-Radar-V | `rer_count_doppler_p0p0_mul_a0p400` | 43.4016 |
| K-Radar | `rer_count_rcs_p0p0_logit_a1p600` | 54.2241 |

## Reference deltas

For the three datasets with an explicit baseline reference in the sweep script:

- Astyx baseline 35.6059 -> best 35.7324, delta +0.1265
- TruckScenes baseline 16.2348 -> best 18.3579, delta +2.1231
- V2X-Radar-V baseline 42.5422 -> best 43.4016, delta +0.8594

## Interpretation

The sweep is useful as a frozen screen because it shows:

- physical evidence components are not interchangeable;
- the best settings differ by dataset;
- RCS and Doppler evidence can help, but the gains are not yet a universal
  quartile-based claim;
- this evidence is sufficient to move T8 from `pending` to `screening`, but it
  is not a completed acceptance table.

## Status

T8 now has frozen physical-analysis evidence.
