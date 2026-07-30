# Clustered statistical audit — 2026-07-30

Variant: strict robust voting `m3rob_q15p25_viou0p24_s0p40`; baseline: RDAR.

## Dataset-level paired deltas

| Dataset | Seed deltas | Dataset mean | Within-dataset bootstrap range |
|---|---|---:|---:|
| Astyx | +0.8222, +0.6202, +1.1228 | +0.8551 | [+0.6202, +1.1228] |
| TruckScenes | +0.4765, +0.8135, +1.4721 | +0.9207 | [+0.4765, +1.4721] |
| V2X-Radar-V | +0.2167, +0.1718, +0.8763 | +0.4216 | [+0.1718, +0.8763] |
| K-Radar | +2.6060, +1.0864, +1.3861 | +1.6928 | [+1.0864, +2.6060] |

The ranges above are the exact three-sample bootstrap support ranges, not normal-theory confidence intervals.

## Cluster bootstrap

The primary mean is computed from the four dataset means, with the dataset as the resampling unit. The exact cluster bootstrap distribution has `4^4 = 256` resamples.

- Cluster-level mean delta: `+0.9726 AP`.
- Exact cluster-bootstrap 95% percentile interval: `[+0.5464, +1.4834] AP`.
- All four dataset means are positive.

This is the appropriate robustness summary for the current four-dataset protocol. The original 12-cell sign test and cell-level bootstrap should be treated as auxiliary diagnostics, not as evidence of 12 independent samples.
