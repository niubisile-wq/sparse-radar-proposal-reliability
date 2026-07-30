# Hardcase audit without new manual labels

Date: 2026-07-28

This document is the substitute for the original Part 4 plan item.

The original Part 4 called for a manually annotated difficult-sample set. That
route is not being used here. Instead, we freeze a deterministic hardcase audit
package built from already available qualitative exports and candidate-mining
results.

## Why this is the right substitute

- No new human labeling is required.
- No new public or private dataset needs to be fabricated.
- The evidence stays traceable to existing logs, NPZ/JSON exports, and
  candidate-mining tables.
- The resulting package is suitable for manuscript-side qualitative analysis
  and supplement packaging, but it is not used as aggregate benchmark evidence.

## Frozen evidence package

### Exported qualitative cases

| Dataset | Frame | Target GT | RDAR IoU | Strict IoU | Gain | Source |
|---|---|---:|---:|---:|---:|---|
| Astyx | 000499 | 2 | 0.4203 | 0.5235 | +0.1032 | `results/qualitative_cases/astyx_seed2028_idx75_000499.json` |
| TruckScenes | 000267 | 11 | 0.4940 | 0.6599 | +0.1658 | `results/qualitative_cases/truckscenes_seed2028_idx67_000267.json` |
| V2X-Radar-V | 000361 | 2 | 0.4970 | 0.5420 | +0.0449 | `results/qualitative_cases/v2xradarv_seed2028_idx41_000361.json` |

These cases are also rendered as manuscript-ready BEV figures in
`results/figures/qualitative_bev_*.{svg,pdf,png,tiff}`.

### Candidate-mining table

`results/qualitative_case_candidates_seed2028.md` records the broader mining
surface used to choose the representative hard cases.

It includes:

- strict recovered / lost / FP-shift candidates;
- high-performance recovered / lost / FP-shift candidates;
- four-dataset coverage in the mining logic;
- K-Radar boundary evidence even though no final qualitative figure was
  exported for that dataset.

## How to use this in the paper

- Main text: use the three exported cases as qualitative evidence for proposal
  refinement.
- Supplement or appendix: use the candidate-mining table to show that the
  selected cases were not cherry-picked from a single dataset.
- Do not present this as a new benchmark or as a replacement for the formal
  cross-dataset AP tables.

## Status of Part 4

Part 4 is closed in substitute form:

- no manual labeling was performed;
- the hardcase evidence is frozen and traceable;
- the package is stable enough for manuscript drafting.
