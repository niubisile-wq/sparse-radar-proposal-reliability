# Final experiment audit and manuscript plan

## One-sentence argument

In sparse radar 3D object detection, we show that proposal preservation, residual recovery, confidence-quality alignment, and complementary proposal voting improve cross-dataset and cross-seed reliability over RDAR, supported by four radar datasets, three random seeds, progressive ablation, diagnostic analysis, robustness stress tests, runtime profiling, and qualitative BEV cases, with the boundary that the high-performance variant is not a strict no-regression method and the strict voting stage has measurable post-processing overhead.

## Terminology ledger

| Canonical term | Meaning / first-use definition | Decision |
|---|---|---|
| RDAR | The main baseline detector / recovery baseline used for formal comparison | Use as baseline name consistently |
| M1 / RC-NMS | Candidate-preserving NMS module | Use as the first progressive ablation module |
| M2 / RDAR recovery | Residual candidate recovery stage | Use as the second progressive ablation module |
| M3 / quality alignment | Quality-aware score/ranking alignment route, represented by qflr55 in the screen table | Use for progressive contribution only; avoid strict formal claim |
| M4 / strict robust proposal voting | `m3rob_q15p25_viou0p24_s0p40` | Use as the main strict robustness method |
| High-performance route | `q55rpa50_kprior` | Use as high-performance variant, not strict all-seed no-regression |
| AP_R40@3D IoU 0.50 | Main AP metric | Report dataset, seed protocol, and IoU threshold whenever numbers are quoted |
| ECE | Expected calibration error diagnostic | Keep for q55 calibration evidence; do not use for strict route |

## Completion audit

| Requirement / experiment | Evidence file | Status | Paper decision |
|---|---|---|---|
| Formal 3-seed main comparison on four datasets | `results/formal_seed_summary.md`, `results/paper_tables_package.md` Table A | Complete | Keep in main paper |
| Strict route deltas vs RDAR over 4 datasets × 3 seeds | `results/paper_tables_package.md` Table B | Complete: 12/12 positive | Keep in main paper |
| Paired statistical summary for strict route | `results/strict_paired_stats.md`, Table L | Complete: mean ΔAP +0.9726, bootstrap 95% CI [0.6468, 1.3536], two-sided sign-test p=0.000488 | Keep; p-values auxiliary |
| Five-row progressive ablation | `results/paper_tables_package.md` Table C | Complete for seed2028 | Keep as progressive/screen ablation; do not call it 3-seed monotonic ablation |
| High-performance route formal comparison | `results/paper_tables_package.md` Table D | Complete; macro +3.7662 over RDAR, but TruckScenes seed2027 is negative | Keep as high-performance variant / supplement, not strict no-regression |
| Calibration diagnostic | `results/diagnostic_gate_summary.md`, Table E/H | Complete | Keep q55 ECE; strict route ECE internal |
| Range/sparsity diagnostic | `results/diagnostic_gate_summary.md`, Table H | Complete but mixed | Internal only as global claim; optional failure/trade-off analysis |
| Parameter count | `results/efficiency_report.md`, Table F | Complete | Keep |
| Detector latency profiler | `results/fixed_detector_profiler.md`, Table I | Complete | Keep with conservative wording: q55 is slower but under 10 ms/frame in fixed profiler |
| Strict voting runtime | `results/efficiency_report.md`, Table F | Complete: about 22 ms/frame | Keep transparently; do not claim free runtime |
| Threshold sensitivity | `results/voting_sensitivity_summary.md`, Table J | Complete: 4/20 settings are 12/12 positive | Keep, likely supplement |
| Qualitative BEV cases | `results/figures/qualitative_bev_main.svg/pdf/png/tiff`, `results/qualitative_cases/` | Complete and QA passed | Keep as qualitative proposal-refinement evidence |
| Random point dropout robustness | `results/point_dropout_gate_summary.md`, Table K | Complete: q55 wins 11/12 cells, mean margin +6.2902; one TruckScenes 30% loss | Keep as average robustness / supplement; not strict |
| Dropout prediction voting probe | `results/point_dropout_voting_gate_summary.md`, Table M | Complete: q55+voting gives 12/12 vs RDAR but min margin is +0.0010 and voting worsens q55 in 8/12 cells | Internal only or at most supplementary caveat |
| Failed sweeps and weak module attempts | `results/final_experiment_decision.md`, internal logs | Complete enough for decision | Internal only |

## Paper-writing deliverables

| Deliverable | File | Status | Use |
|---|---|---|---|
| Consolidated table package | `results/paper_tables_package.md` | Complete | Source for all main/supplement/internal numeric tables |
| Story and next-experiment plan | `results/paper_story_and_next_experiments.md` | Complete and updated | Working roadmap and evidence boundary notes |
| Final experiment audit and manuscript plan | `results/final_experiment_audit_and_manuscript_plan.md` | Complete and current | Top-level index for experiment status and section skeleton |
| Method details and pseudocode | `results/method_details_pseudocode.md` | Complete draft | Reproducible Method-section source for M1/M2/M3/M4 mechanisms, parameters, pseudocode, and reviewer-risk boundaries |
| Method section draft | `results/method_section_draft.md` | Complete draft | Manuscript-ready Method section with equations and Algorithm 1 text |
| Access-surpass experiment plan | `results/access_surpass_experiment_plan.md` | Complete draft | Prioritized experiment/story plan to exceed the Access paper's evidence package |
| Figure 1 method overview specification | `results/figure1_method_overview_spec.md` | Complete draft | Panel layout, Mermaid sketch, caption, and visual constraints for the main method figure |
| Manuscript working draft v1 | `results/manuscript_working_draft_v1.md` | Complete working draft | Integrated abstract, introduction, related work scaffold, method, results, discussion, conclusion, and missing-input list |
| Verified reference plan | `results/verified_reference_plan.md` | Mostly complete for draft: core references mapped; RDAR treated as internal baseline name; Astyx DOI still optional final check | Reference-support map for citation keys and final BibTeX audit |
| Draft BibTeX file | `results/references_draft.bib` | Draft complete for current citation keys; Astyx DOI/style still needs final audit | Temporary citation database aligned to manuscript working draft keys |
| Citation verification update | `results/citation_verification_update.md` | Complete | Documents RDAR handling, Astyx metadata update, V2X-Radar official citation update, and citation-key consistency check |
| Results section draft | `results/results_section_draft.md` | Complete draft | Direct starting point for manuscript Results |
| Results section formal v2 | `results/results_section_formal_v2.md` | Complete draft | Current authoritative Results prose following the final evidence hierarchy and claim boundaries |
| Paper-ready figure/table plan | `results/paper_ready_figure_table_plan.md` | Complete | Decides main vs supplement vs internal figures/tables and caption boundaries |
| Final table and figure placement plan | `results/final_table_placement_and_captions.md` | Complete | Final main/supplement/internal placement, captions, allowed claims, and forbidden overclaims for all tables and figures |
| Pre-submission claim-risk audit | `results/pre_submission_claim_risk_audit.md` | Complete | Checklist to prevent overclaiming before submission |
| Manuscript skeleton with safe claims | `results/manuscript_skeleton_safe_claims.md` | Complete draft | Full manuscript structure from title through conclusion |
| Safe abstract/contributions/limitations wording | `results/safe_abstract_contributions_limitations.md` | Complete draft | Short reusable wording for abstract, contributions, limitation, and conclusion |

## Final keep / internal / rerun decision

### Keep in main paper

1. Formal 3-seed main comparison.
2. Strict route 12/12 positive deltas against RDAR.
3. Paired statistical summary for strict route, with p-values treated as auxiliary.
4. Five-row progressive ablation, explicitly labelled as seed2028 progressive evidence.
5. Efficiency: parameter count and fixed-protocol detector latency.
6. Qualitative BEV cases for strict route.

### Keep in supplement or secondary analysis

1. High-performance route `q55rpa50_kprior`.
2. q55 ECE calibration improvement.
3. Strict voting threshold sensitivity.
4. Random point dropout robustness.
5. Existing eval-log latency table.
6. Dropout prediction voting only as a caveat if needed, not as positive main evidence.

### Keep internal unless improved

1. qflr55 formal strict claim: TruckScenes seed2027 regresses.
2. q55 strict no-regression claim: TruckScenes seed2027 regresses.
3. Global range/sparsity recall superiority: diagnostic gate is mixed.
4. Strict route ECE: worsens in 12/12 diagnostic comparisons.
5. Failed sweeps.
6. Dropout prediction voting as a strong robustness claim: post-hoc selected on the failed cell and worsens q55 in most cells.

### Rerun only if a stronger claim is needed

1. Matched-seed dropout for q55 and/or strict route if the paper needs strict dropout robustness.
2. Optimized voting implementation if the paper needs a strong real-time claim.
3. Range-wise AP rather than recall if a distance-robustness figure is required.

## Experiments / Results section skeleton

### 4.1 Experimental setup

State the task, four datasets, AP metric, 3-seed protocol, and identical evaluation settings. Emphasize that the main formal comparison uses mean ± standard deviation over three seeds, while the progressive ablation is reported as a seed2028 module-contribution screen.

Claim: the evaluation is designed to test both average performance and seed-dataset robustness.  
Evidence: four datasets, three seeds, AP_R40@3D IoU 0.50, fixed evaluation protocol.  
Boundary: matched-seed strict evidence is for RDAR vs strict route; some supplementary q55/dropout evidence uses latest available checkpoints.

### 4.2 Main cross-dataset comparison

Open with the strict route result. Report RDAR, strict robust proposal voting, and q55 high-performance route in the same table. The central sentence should be:

> The strict robust route improved RDAR on all four datasets in mean AP and achieved positive gains in all 12 seed-dataset comparisons, while the high-performance route obtained the largest macro mean but did not satisfy the strict no-regression criterion.

Use Table A and Table B.

### 4.3 Progressive module ablation

Use the five-row seed2028 ablation table to explain the role of each module. The logic should be:

1. Baseline / PointPillars establishes the starting point.
2. M1 / RC-NMS gives the first broad gain by preserving candidates.
3. M2 / RDAR recovery gives a small but consistent refinement in the seed2028 screen.
4. M3 / quality alignment provides the largest average jump.
5. M4 / high-performance calibration further improves the seed2028 macro average.

Do not overclaim this as a 3-seed monotonic ablation.

### 4.4 Strict robustness across seeds

Use the paired-delta and statistical summary. The core paragraph should state that strict robustness is defined as positive improvement over RDAR for every seed-dataset pair, not as tolerance of small regressions. Report 12/12 wins, min ΔAP +0.1718, mean ΔAP +0.9726, and bootstrap CI [0.6468, 1.3536].

Use Table L. If including p-values, write them conservatively as auxiliary evidence from 12 paired comparisons.

### 4.5 Diagnostics: calibration and failure boundaries

Separate supported and unsupported diagnostics:

- Supported: q55 improves ECE in 12/12 diagnostic comparisons; use this to support confidence-quality alignment.
- Unsupported as a global claim: range/sparsity recall is mixed; do not claim universal improvement for far-range or sparse-bin objects.
- Boundary: strict route improves AP but worsens ECE, so its role is robust proposal consensus rather than calibration.

Use Table E/H selectively.

### 4.6 Robustness under inference-time point dropout

Report this as a stress test, not as the main strict claim. The main sentence should be:

> Under deterministic inference-time point dropout, the high-performance variant maintained a higher macro AP than RDAR at 10%, 20%, and 30% dropout, but one TruckScenes cell at 30% dropout was slightly negative; therefore, we use this result as average robustness evidence rather than a strict all-cell robustness claim.

Use Table K.

### 4.7 Efficiency and deployment cost

Report parameter count, fixed-protocol latency, and voting overhead separately. Do not merge detector latency and voting latency into one favorable number.

Main wording:

> The quality-alignment and high-performance routes preserve the 4.830M parameter count of RDAR, while the strict voting variant adds no trainable parameters but introduces an additional post-processing cost of approximately 22 ms/frame in the current implementation.

Use Table F/I.

### 4.8 Qualitative analysis

Use strict-route BEV cases from Astyx, TruckScenes, and V2X-Radar-V. Focus on proposal refinement and IoU improvement rather than claiming global range/sparsity robustness.

Suggested figure caption logic:

> Representative BEV cases show that strict proposal voting refines borderline detections that RDAR localizes below the matching threshold, improving IoU from 0.4203 to 0.5235 on Astyx, 0.4940 to 0.6599 on TruckScenes, and 0.4970 to 0.5420 on V2X-Radar-V.

### 4.9 Limitations

Name the limitations explicitly:

1. The high-performance route has one TruckScenes seed regression and should not be treated as a strict no-regression method.
2. The strict route has measurable voting overhead.
3. Range/sparsity diagnostics are mixed and should not be generalized as universal far-range or sparse-object superiority.
4. Dropout robustness is average-positive but not all-cell strict.

## Claim-evidence map

| Claim | Evidence | Status |
|---|---|---|
| Strict route improves RDAR robustly across datasets and seeds | 12/12 positive paired deltas, mean ΔAP +0.9726 | Supported |
| High-performance route gives the largest macro AP | q55 macro 39.1214 vs RDAR 35.3552 | Supported with boundary |
| Every module contributes to the progressive design | Seed2028 five-row ablation | Supported as screen/progressive evidence only |
| q55 improves calibration | ECE 12/12 diagnostic wins | Supported |
| Method improves all range/sparsity bins | Mixed diagnostic gate | Not supported; keep internal |
| Method is free at runtime | q55 slower than RDAR; strict voting ~22 ms/frame | Not supported |
| q55 is robust to point dropout | 11/12 absolute AP wins, positive macro margins | Partially supported; average/supplement only |
| Dropout prediction voting makes dropout robustness strict | 12/12 vs RDAR but min margin +0.0010 and 8/12 cells worse than q55 | Not supported as main claim; internal/supplement caveat only |
