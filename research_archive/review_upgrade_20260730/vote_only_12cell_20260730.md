# Complete proposed vote-only audit

The proposed vote-only operation was applied to all 12 frozen RDAR cells with
the common settings `vote_iou=0.24`, `strength=0.40`, BEV-center mode, and a
50-entry residual exclusion. No expert predictions were used.

| Dataset | 2026 | 2027 | 2028 | Dataset mean | Positive cells |
|---|---:|---:|---:|---:|---:|
| Astyx | +0.1280 | +0.1608 | +0.2190 | +0.1693 | 3/3 |
| TruckScenes | -0.1660 | -0.3526 | +0.4530 | -0.0219 | 1/3 |
| V2X-Radar-V | +0.3331 | -0.8661 | -0.0988 | -0.2106 | 1/3 |
| K-Radar | -0.1540 | +0.1909 | -0.1756 | -0.0462 | 1/3 |
| Overall |  |  |  | **-0.0274** | **6/12** |

This result is important for attribution: the proposed geometric voting step
is not independently no-regressive across seeds. The four-cell gate/vote
diagnostic therefore supports a gate-led interpretation of the strict route,
while voting should be described as a conditional refinement rather than a
uniformly improving contribution.

Raw evaluation logs are stored under `vote_only_12cell/` and the reproducible
launcher is `run_vote_only_all.sh`.
