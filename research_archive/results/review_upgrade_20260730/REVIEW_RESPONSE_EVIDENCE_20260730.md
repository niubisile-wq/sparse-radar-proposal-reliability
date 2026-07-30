# Reviewer-response evidence map (2026-07-30)

This file maps the main reviewer risks to evidence now included in the
manuscript or supplementary audit directory. It is an internal drafting aid;
the manuscript must retain the stated protocol boundaries.

| Reviewer concern | Evidence added | Manuscript location / artifact | Remaining boundary |
|---|---|---|---|
| Generic post-processing may explain the gain | Three-seed fixed controls for standard box voting, Gaussian Soft-NMS, and WBF | `paper.tex`, Table 5; `standard_box_voting_three_seed_20260730.csv`, `soft_nms_three_seed_20260730.csv`, `wbf_three_seed_20260730.csv` | These controls do not replace architecture-level comparisons such as GFL/VarifocalNet. |
| Threshold was selected on the same four-dataset protocol | Training-only leave-one-dataset-out selection and held-out application | `paper.tex`, Table 7; `lodo_strict_selection_20260730.*` | Frozen-output audit, not a newly isolated development split. |
| Twelve cells are not twelve independent datasets | Dataset-clustered means and exact cluster bootstrap | `paper.tex`, paired-reliability discussion; `clustered_statistics_20260730.md` | Four dataset clusters remain a finite evidence set. |
| Small positive margins may be noise | Exact four-decimal paired audit and held-out seed-level results | `paper.tex`, Tables 4 and 7 | No claim is made that every positive margin is practically large. |
| Strict-route cost is understated | Existing full voting-loop profile plus proposal-budget scaling profile | `paper.tex`, Efficiency; `strict_route_cost_audit.md`, `voting_runtime_scaling_20260730.*` | Same-process detector+expert endpoint timing is unavailable because checkpoints are not in the instance root. |
| Reproducibility materials are incomplete | Source, PDF, figures, frozen summaries, controls, LODO outputs, and runtime logs packaged | `EAAI_submission_package_20260730.zip` and `review_upgrade_20260730/` | Raw datasets and checkpoints remain governed by provider/storage constraints. |

## Recommended response posture

Keep the formal statement that the strict route improves all 12 matched cells
under the frozen main protocol. Support it with the dataset-clustered interval
and the leave-one-dataset-out audit, but describe the latter as a robustness
audit rather than an independent confirmation. Do not call the result a
universal guarantee or claim measured end-to-end latency from separately
profiled stages.
