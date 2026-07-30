# Reviewer-response evidence map (2026-07-30)

This file maps the main reviewer risks to evidence now included in the
manuscript or supplementary audit directory. It is an internal drafting aid;
the manuscript must retain the stated protocol boundaries.

| Reviewer concern | Evidence added | Manuscript location / artifact | Remaining boundary |
|---|---|---|---|
| Generic post-processing may explain the gain | Three-seed fixed controls for standard box voting, Gaussian Soft-NMS, and WBF | `paper.tex`, Table 5; `standard_box_voting_three_seed_20260730.csv`, `soft_nms_three_seed_20260730.csv`, `wbf_three_seed_20260730.csv` | These controls do not replace architecture-level comparisons such as GFL/VarifocalNet. |
| Expert gate and voting contributions are confounded | Four-cell decomposition: neither, gate-only, vote-only, and gate+vote on the same primary lane | `paper.tex`, Table 6; `gate_vote_factorial_seed2027.md` and frozen remote logs | Three rows use seed-2027 expert checkpoints; K-Radar uses the available seed-2028 expert checkpoint, so this is component evidence rather than a new 12-cell claim. |
| Threshold was selected on the same four-dataset protocol | Leave-one-dataset-out threshold-selection and threshold-transfer screens, including complete seed-level rows | `paper.tex`, Tables 7--8; `lodo_strict_selection_20260730.*`, `lodo_holdout_seed_results_20260730.csv` | Frozen-output audit, not a newly isolated development split; V2X-Radar-V seed 2027 is -0.2945 AP in the unconstrained transfer screen. |
| Twelve cells are not twelve independent datasets | Dataset-clustered means and exact cluster bootstrap | `paper.tex`, paired-reliability discussion; `clustered_statistics_20260730.md` | Four dataset clusters remain a finite evidence set. |
| Small positive margins may be noise | Exact four-decimal paired audit and held-out seed-level results | `paper.tex`, Tables 4 and 7 | No claim is made that every positive margin is practically large. |
| Strict-route cost is understated | Existing full voting-loop profile plus proposal-budget scaling profile and a same-process primary+expert endpoint profile | `paper.tex`, Efficiency; `strict_route_cost_audit.md`, `voting_runtime_scaling_20260730.*`, `e2e_profile_20260730.md` | The endpoint uses final returned proposals rather than the offline 500-proposal raw-candidate path, so it is not advertised as complete strict-route FPS. |
| Expert detector is under-specified | Added architecture, stable BEV gate equation, training schedule, checkpoint epoch, and dataset-specific configuration names | `paper.tex`, `expert_specification_20260730.md` | Raw datasets and large checkpoints remain governed by provider/storage constraints; exact provenance is archived separately. |
| Reproducibility materials are incomplete | Source, PDF, figures, frozen summaries, controls, LODO outputs, component diagnostic, and runtime logs packaged | `EAAI_submission_package_20260730.zip` and `review_upgrade_20260730/` | Raw datasets and checkpoints remain governed by provider/storage constraints. |

## New split-validity audit

Direct inspection of the eight frozen train/validation info files found zero
exact overlap in `point_cloud.pc_idx` for every dataset. It also found
validation IDs adjacent to a training ID for 82/100 Astyx frames, 4/80
TruckScenes frames, 1/80 V2X-Radar-V frames, and 80/80 K-Radar frames. The
conversion records contain no scene, sequence, vehicle, or timestamp key, so
this audit cannot prove scene-disjointness or exclude same-scene correlation.
The manuscript now reports this explicitly and limits all conclusions to the
frame-level frozen protocol.

Artifact: `frozen_split_audit_20260730.md` and
`scripts/audit_frozen_split_overlap.py`.

## Recommended response posture

Keep the formal statement that the strict route improves all 12 matched cells
under the frozen main protocol. Support it with the dataset-clustered interval
and the leave-one-dataset-out audit, but describe the latter as a robustness
audit rather than an independent confirmation. Do not call the result a
universal guarantee or claim measured end-to-end latency from separately
profiled stages.

## Additional attribution evidence: complete vote-only audit

The proposed vote-only operation was also run on all 12 frozen RDAR cells,
without expert predictions. The AP differences were:

| Dataset | 2026 | 2027 | 2028 | Mean | Positive |
|---|---:|---:|---:|---:|---:|
| Astyx | +0.1280 | +0.1608 | +0.2190 | +0.1693 | 3/3 |
| TruckScenes | -0.1660 | -0.3526 | +0.4530 | -0.0219 | 1/3 |
| V2X-Radar-V | +0.3331 | -0.8661 | -0.0988 | -0.2106 | 1/3 |
| K-Radar | -0.1540 | +0.1909 | -0.1756 | -0.0462 | 1/3 |
| Overall |  |  |  | **-0.0274** | **6/12** |

The manuscript now makes the gate-led interpretation explicit: voting is a
conditional geometric refinement, not a uniformly improving component. A
complete expert-gate-by-vote factorial remains explicitly marked as unavailable
in the frozen checkpoint set.
