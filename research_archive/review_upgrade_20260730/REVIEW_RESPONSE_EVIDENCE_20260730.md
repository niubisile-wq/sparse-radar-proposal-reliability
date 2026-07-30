# Reviewer-response evidence map (2026-07-30)

This file maps the main reviewer risks to evidence now included in the
manuscript or supplementary audit directory. It is an internal drafting aid;
the manuscript must retain the stated protocol boundaries.

| Reviewer concern | Evidence added | Manuscript location / artifact | Remaining boundary |
|---|---|---|---|
| Generic post-processing may explain the gain | Three-seed fixed controls for standard box voting, Gaussian Soft-NMS, and WBF | `paper.tex`, Table 5; `standard_box_voting_three_seed_20260730.csv`, `soft_nms_three_seed_20260730.csv`, `wbf_three_seed_20260730.csv` | These controls do not replace architecture-level comparisons such as GFL/VarifocalNet. |
| Threshold was selected on the same four-dataset protocol | Leave-one-dataset-out threshold-selection and threshold-transfer screens, including complete seed-level rows | `paper.tex`, Tables 7--8; `lodo_strict_selection_20260730.*`, `lodo_holdout_seed_results_20260730.csv` | Frozen-output audit, not a newly isolated development split; V2X-Radar-V seed 2027 is -0.2945 AP in the unconstrained transfer screen. |
| Twelve cells are not twelve independent datasets | Dataset-clustered means and exact cluster bootstrap | `paper.tex`, paired-reliability discussion; `clustered_statistics_20260730.md` | Four dataset clusters remain a finite evidence set. |
| Small positive margins may be noise | Exact four-decimal paired audit and held-out seed-level results | `paper.tex`, Tables 4 and 7 | No claim is made that every positive margin is practically large. |
| Strict-route cost is understated | Existing full voting-loop profile plus proposal-budget scaling profile; manuscript now labels 22--23 ms as isolated voting-kernel cost | `paper.tex`, Efficiency; `strict_route_cost_audit.md`, `voting_runtime_scaling_20260730.*` | A synchronized same-process end-to-end endpoint is still a separate measurement task. |
| Expert detector is under-specified | Added architecture, stable BEV gate equation, training schedule, checkpoint epoch, and dataset-specific configuration names | `paper.tex`, `expert_specification_20260730.md` | Raw datasets and large checkpoints remain governed by provider/storage constraints; exact provenance is archived separately. |
| Reproducibility materials are incomplete | Source, PDF, figures, frozen summaries, controls, LODO outputs, component diagnostic, and runtime logs packaged | `EAAI_submission_package_20260730.zip` and `review_upgrade_20260730/` | Raw datasets and checkpoints remain governed by provider/storage constraints. |

## Recommended response posture

Keep the formal statement that the strict route improves all 12 matched cells
under the frozen main protocol. Support it with the dataset-clustered interval
and the leave-one-dataset-out audit, but describe the latter as a robustness
audit rather than an independent confirmation. Do not call the result a
universal guarantee or claim measured end-to-end latency from separately
profiled stages.
