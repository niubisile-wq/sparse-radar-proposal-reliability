# Fixed-expert 12-cell gate/vote factorial audit

This audit uses the formal strict-route gate/vote parameters but a deliberately
fixed-expert cross-seed diagnostic protocol: Astyx, TruckScenes, and
V2X-Radar-V share the epoch-160 expert
checkpoint trained with seed 2027; K-Radar uses the available epoch-160 expert
checkpoint trained with seed 2028. The three primary RDAR streams use seeds
2026, 2027, and 2028. This separates primary-seed variation from expert
variation and directly tests component attribution. It is not numerically
identical to the selected formal strict endpoint: that endpoint uses a
seed-matched expert checkpoint for each primary seed. The different expert
stream changes score ranking and, after voting, box geometry, so the two
protocols are complementary rather than contradictory.

Parameters: expert match IoU 0.30, score mixing alpha 0.30, IoU exponent 0.25,
unmatched scale 0.50, residual exclusion 50, vote IoU 0.24, vote strength
0.40, lower-score-neighbor restriction, and xy/heading geometry mode.

| Conversion | Gate-only differences (2026 / 2027 / 2028) | Gate-only positive | Gate+vote differences (2026 / 2027 / 2028) | Gate+vote positive |
|---|---:|---:|---:|---:|
| Astyx | +0.0535 / +0.5686 / -0.4282 | 2/3 | -0.2650 / +1.6178 / -1.7107 | 1/3 |
| TruckScenes | +3.4379 / +2.8000 / +3.0339 | 3/3 | +1.9138 / +2.0084 / +4.0684 | 3/3 |
| V2X-Radar-V | +1.0020 / +1.6363 / +1.2755 | 3/3 | +1.2324 / +1.6202 / +1.7304 | 3/3 |
| K-Radar | +1.7508 / +1.6357 / +2.2242 | 3/3 | +2.2178 / +2.0732 / +2.1091 | 3/3 |
| Overall | mean +1.5825 AP | **11/12** | mean +1.5513 AP | **10/12** |

The result strengthens the gate-led interpretation: with the formal fixed-expert
protocol, gate-only improves 11/12 primary dataset-seed cells and has positive
means on all four conversions. Adding the unrestricted local geometry vote to
the gated lane improves 10/12 cells; the two Astyx regressions show why voting
must remain conditional rather than being presented as an independently stable
module. This factorial audit is complementary to the selected seed-matched
strict endpoint; it is not used to replace the pre-existing 12/12 selected-
route claim. The correct interpretation is that gate-only is more reproducible
than vote-only under the fixed-expert stress test, while geometry refinement
remains conditional.

The raw prediction outputs and logs are stored on the instance under:
`results/review_upgrade_20260730/strict_fixed_expert_factorial_12cell/`.
The fixed-expert choice was made before reading the factorial AP values and was
based on checkpoint availability: seed 2027 is the common central checkpoint
for Astyx, TruckScenes, and V2X-Radar-V, while seed 2028 is the available
epoch-160 expert checkpoint for K-Radar. No factorial result was used to select
these checkpoints.
