# Accuracy / reliability Pareto snapshot

Date: 2026-07-28

Part 3 is now closed and this snapshot reflects the final closed matrix.

## Best observed point per dataset

| Dataset | Best AP | range_power | support_scale | alpha |
|---|---:|---:|---:|---:|
| Astyx | 34.4981 | 0.0 | 8.0 | 0.05 |
| TruckScenes | 18.7540 | 0.0 | 4.0 | 0.30 |
| V2X-Radar-V | 42.6786 | 2.0 | 1.0 | 0.05 |
| K-Radar | 53.7522 | 2.0 | 8.0 | 0.20 |

## Pareto reading

- Astyx prefers the strongest support scale at weak range compensation.
- TruckScenes peaks at moderate support with no range exponent.
- V2X-Radar-V prefers a stronger range exponent and minimal support scale.
- K-Radar prefers the strongest range exponent in the closed matrix and the
  widest support scale among the tested settings.

## What this does and does not mean

- It does mean the compensation family is not a trivial no-op.
- It does not mean the closed matrix is globally optimal beyond the tested
  grid.
- Any new sweep should be treated as an extension to this snapshot, not a
  revision of the closed evidence.
