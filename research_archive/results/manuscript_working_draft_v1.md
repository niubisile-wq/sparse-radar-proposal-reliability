# Manuscript working draft v1

Working title: **Robust Proposal Preservation and Quality Alignment for Sparse Radar 3D Object Detection**

Status: integrated manuscript draft for internal revision. Body-text citation placeholders have been replaced with temporary reference keys from `verified_reference_plan.md`; final BibTeX metadata and journal-specific citation formatting are still pending. Figure and table numbers follow the current manuscript plan and may change after template selection.

## Abstract

Sparse radar 3D object detection is sensitive to proposal suppression, missed weak objects, and confidence scores that are poorly aligned with localization quality. These issues make average AP insufficient as the only evidence of improvement, because a method can improve the macro mean while regressing on a particular dataset or random seed. We propose a proposal-level radar detection framework that combines candidate-preserving suppression, residual proposal recovery, confidence-quality alignment, and consistency-aware proposal voting. Across Astyx, TruckScenes, V2X-Radar-V, and K-Radar, the strict proposal-voting route improved RDAR in all 12 paired seed-dataset comparisons, with a mean gain of +0.9726 AP\(_{R40}\) at 3D IoU 0.50 and a minimum gain of +0.1718. A separate high-performance route achieved the largest macro AP, increasing the macro mean from 35.3552 for RDAR to 39.1214, but was not used for the strict no-regression claim because one TruckScenes seed regressed. Calibration, point-dropout, threshold-sensitivity, efficiency, and qualitative analyses further define the strengths and boundaries of the method. These results show that proposal-level refinement can improve sparse radar detection reliability when strict robustness and high average performance are evaluated as distinct objectives.

## 1. Introduction

Radar-only 3D object detection is important for perception systems that must operate under poor illumination, adverse weather, and long-range sensing conditions where cameras and lidar may be degraded [KRadar2022, TruckScenes2024, V2XRadar2024]. Compared with lidar point clouds, radar point clouds are typically sparser, noisier, and more sensitive to object aspect, multipath, and sensor-specific acquisition patterns [Astyx2019, KRadar2022]. These properties make radar detection depend not only on feature extraction, but also on whether weak proposals survive post-processing and whether confidence scores rank well-localized boxes correctly.

Existing radar 3D detection pipelines often adapt efficient lidar-style voxel or pillar detectors to radar point clouds [PointPillars2019, OpenPCDet2020]. This design is attractive because it is reproducible and computationally practical, but it also inherits proposal-level failure modes. A weak radar object may be represented by only a few returns. If the corresponding candidate box receives a low score or partially overlaps a higher-scored but poorly localized box, standard score filtering and non-maximum suppression can remove it before later processing. In this study, RDAR denotes our recovery-oriented primary baseline route in the experimental framework. Because average AP alone does not show whether an improvement is reliable across datasets and random seeds, we evaluate RDAR and the proposed strict route with paired multi-seed comparisons [HendersonSeeds2018, ColasSeeds2018].

A second issue is evaluation reliability. A method can improve the mean score while producing a regression in one seed-dataset pair. This matters for sparse radar detection because performance variance can be driven by dataset-specific density, annotation protocol, and sensor configuration. For deployment-oriented radar perception, a strict robustness claim should therefore be separated from a high-average-performance claim. The former requires paired no-regression evidence, whereas the latter can be useful as an operating point even if it contains isolated regressions.

Here we propose a reliability-oriented radar proposal refinement framework. The method decomposes proposal failure into four components: candidate loss during suppression, residual missed-object evidence, confidence-localization mismatch, and local proposal jitter. Candidate-preserving NMS keeps a broader set of boxes; residual proposal recovery conservatively reintroduces weak candidates; a quality-aligned scoring head trains confidence to reflect localization quality; and consistency-aware proposal voting constructs a strict robust route by reinforcing locally consistent predictions. We evaluate the framework on four radar datasets with three random seeds and explicitly separate the strict robust route from a separate high-performance route. This strategy allows the paper to make a conservative no-regression claim without discarding the larger macro-AP gains of the high-performance variant.

The main contributions are:

1. We propose a four-stage proposal-level framework for sparse radar 3D detection that addresses candidate suppression, residual missed-object recovery, confidence-quality alignment, and prediction consensus as distinct failure modes.
2. We introduce a strict 4-dataset by 3-seed evaluation gate and show that the strict proposal-voting route improves RDAR in all 12 paired seed-dataset comparisons.
3. We separate strict robustness from high macro performance: the strict route supports the no-regression claim, while a high-performance route achieves the largest macro mean AP.
4. We provide calibration, point-dropout, threshold-sensitivity, efficiency, and qualitative analyses, and explicitly mark mixed or post-hoc findings as supplementary or internal rather than main evidence.

## 2. Related Work

### 2.1 Radar 3D object detection

Radar 3D detection has developed from adapting lidar-style point-cloud detectors toward radar-specific designs that account for sparsity, Doppler cues, and sensor noise [Astyx2019, KRadar2022, TruckScenes2024, V2XRadar2024]. Pillar-based detectors remain a practical foundation because they convert unordered point sets into efficient bird's-eye-view representations and can be trained with established 3D detection toolchains [PointPillars2019, OpenPCDet2020]. However, radar point clouds differ substantially from lidar point clouds: objects may contain few returns, localization can be noisy, and proposal confidence can be unstable. These properties make proposal generation and post-processing especially important.

### 2.2 Proposal filtering, recovery, and box refinement

Non-maximum suppression is widely used to remove duplicate detections, but its behavior depends strongly on score thresholds and overlap thresholds [NMS2006, SoftNMS2017]. In sparse radar scenes, aggressive filtering can discard useful candidates before they are evaluated by later ranking or fusion steps. Proposal recovery and box voting provide two complementary responses. Recovery attempts to preserve weak or missed candidates, whereas voting uses local agreement among nearby boxes to reduce localization jitter [BoxVoting2015, VoteNet2019]. The present work combines these ideas in a bounded radar-specific pipeline and evaluates them under paired multi-seed conditions.

### 2.3 Confidence-quality alignment

Single-stage detectors typically learn classification and localization through separate losses, and the resulting classification score may not be well aligned with localization quality [FocalLoss2017, GFL2020]. Quality-aware classification targets and IoU-aware scoring have been used to improve ranking behavior in object detection [GFL2020, VarifocalNet2021, NoisyAnchors2020]. Our quality-aligned head follows this principle by assigning positive anchors an IoU-derived soft target with a residual objectness term, so that confidence retains objectness information while reflecting localization quality.

### 2.4 Robust evaluation across datasets and seeds

Multi-dataset and multi-seed evaluation is necessary when the claimed improvement is reliability rather than only peak performance [HendersonSeeds2018, ColasSeeds2018]. Reporting only a single seed or a macro average can obscure regressions in particular datasets. We therefore define strict robustness as positive improvement over RDAR for every dataset and random seed in the formal comparison. This definition is deliberately conservative: it may exclude a higher-average variant from the main robustness claim, but it makes the supported claim easier to audit.

## 3. Method

### 3.1 Task formulation

Given a radar point cloud for a frame, the detector predicts a set of 3D bounding boxes, class labels, and confidence scores. We focus on single-class car detection under the dataset protocols used for Astyx, TruckScenes, V2X-Radar-V, and K-Radar. Let a detector output be denoted as \(P=\{(b_i,s_i)\}_{i=1}^{N}\), where \(b_i \in \mathbb{R}^{7}\) represents the 3D box parameters and \(s_i\) is the confidence score. The objective is not only to increase the mean AP, but also to reduce seed- and dataset-specific regressions that are often hidden by average performance.

Sparse radar scenes create three practical difficulties for proposal ranking. First, useful low-confidence proposals may be removed by strict score filtering or overly aggressive non-maximum suppression. Second, weak-object evidence may appear in a complementary residual proposal stream but remain absent from the primary output. Third, classification confidence is not always aligned with localization quality, so a poorly localized box can outrank a better candidate. The proposed framework addresses these failure modes through four progressive components: candidate-preserving NMS, residual proposal recovery, quality-aligned scoring, and consistency-aware proposal refinement.

### 3.2 Framework overview

The framework is built on a PointPillars-style radar detector and refines its proposal generation and ranking behavior rather than replacing the entire backbone. The baseline detector uses a PillarVFE, a 2D BEV backbone, and a single-stage anchor head. In the baseline configuration, car anchors use size \([4.003, 1.800, 1.510]\), bottom height \(-0.180\), matched/unmatched IoU thresholds of 0.60/0.45, score threshold 0.10, NMS threshold 0.01, and pre-/post-NMS limits of 4096/500.

The full pipeline contains four stages (Fig. 1). M1 relaxes the post-processing gate to preserve more candidate boxes. M2 adds a residual recovery stage that either fuses residual boxes with matched primary boxes or appends them with conservative scores. M3 replaces binary classification targets with IoU-derived soft quality targets so that proposal confidence better reflects localization quality. M4 constructs the strict robust route by applying expert quality gating and local box voting, selecting the operating point by a no-regression criterion over all paired dataset-seed comparisons. M1, M2, and M4 are proposal-level refinement steps, whereas M3 is the trainable scoring head.

### 3.3 Candidate-preserving NMS

The first stage reduces premature candidate removal. Standard post-processing can be brittle for radar point clouds because only a small number of returns may support an object. A strict score threshold or very low NMS threshold can remove boxes that are not top-ranked initially but could still support later recovery or consensus refinement.

We therefore replace the baseline post-processing with a candidate-preserving configuration. The score threshold is reduced from 0.10 to 0.0, the NMS threshold is increased from 0.01 to 0.50, and the pre-/post-NMS proposal limits remain 4096 and 500. This stage does not introduce a new trainable layer. Its role is to keep a broader proposal set so that subsequent residual recovery and voting have access to borderline candidates.

### 3.4 Residual proposal recovery

Candidate preservation alone cannot recover information that exists only in a complementary residual proposal list. The second stage therefore re-examines residual predictions and merges them into the primary prediction set with conservative scoring. This stage is designed to improve proposal availability without allowing residual boxes to dominate the final ranking.

For each frame, the method takes a primary proposal set \(P=\{(b_i,s_i)\}\) and a residual proposal set \(R=\{(r_j,t_j)\}\). The top 50 residual boxes are retained by residual score. For each residual box \(r_j\), the method finds the primary box with the maximum 3D IoU. If this IoU is at least 0.10, the two boxes are fused by score-weighted averaging, with heading averaged in doubled-angle circular space. If no primary box reaches the threshold, the residual box is appended unchanged. Recovered residual proposals receive scores below the primary positive-score ceiling:

\[
s^{\mathrm{rec}}_j =
\left(\frac{1}{2}\min_{i:s_i>0}s_i\right)
\cdot
\left(0.5 + 0.5 \frac{t_j}{\max_k t_k}\right).
\]

This score assignment preserves weak-object evidence while preventing residual proposals from overwhelming the primary ranking. In the progressive ablation, the recovery stage gives only a small macro-AP gain, so it should be interpreted as a stabilizing component rather than the dominant source of improvement.

### 3.5 Quality-aligned scoring

The third stage addresses the mismatch between classification confidence and localization quality. In anchor-based single-stage detection, a positive anchor is usually trained with a binary class target. This can assign the same target to boxes with different localization quality, causing AP degradation when poorly localized proposals receive high confidence scores. We replace the binary positive target with an online IoU-derived quality target.

For each positive anchor, the predicted box and its assigned target box are decoded, and their aligned 3D IoU is computed as \(q \in [0,1]\). The quality target is then defined as

\[
\hat{q} = \rho + (1-\rho)q^{\gamma},
\]

where \(\rho=0.55\) is the objectness residual and \(\gamma=1.0\) is the IoU power. The residual term keeps a base objectness signal for positive anchors, while the IoU term differentiates better-localized positives from weaker ones. With predicted probability \(p=\sigma(z)\), the quality focal classification loss is

\[
\mathcal{L}_{\mathrm{qf}} =
\left|\hat{q}-p\right|^{\beta}
\cdot
\mathrm{BCEWithLogits}(z,\hat{q}),
\]

with \(\beta=2.0\). The quality-aligned head is implemented as `AnchorHeadQualityFocal`; the corresponding route uses score threshold 0.0, NMS threshold 0.50, pre-/post-NMS limits of 4096/500, and matched/unmatched anchor thresholds of 0.50/0.35 in the RPA-style configuration.

This stage provides the main trainable change in the framework. Its role is supported by the progressive ablation and by the expected calibration error diagnostics for the high-performance Q55 route. However, calibration should not be claimed for the final strict voting route, because the current diagnostics show that strict-route ECE worsens despite improving paired AP.

### 3.6 Consistency-aware proposal refinement

The fourth stage constructs the strict robust route. It combines expert quality gating with local proposal voting. Unlike the high-performance route, which is selected for macro AP, the strict route is selected only if it improves RDAR in every paired dataset-seed comparison.

The quality gate first compares the primary proposals with an expert proposal set. Let \(E=\{(e_j,u_j)\}\) denote the expert boxes and scores. For each primary box \(b_i\), the method finds the expert box with the highest 3D IoU. If the best IoU is at least 0.30, the primary score is reweighted as

\[
s_i' = s_i^{1-\alpha} \cdot u_j^{\alpha} \cdot
\mathrm{IoU}(b_i,e_j)^{\eta},
\]

where \(\alpha=0.30\) and \(\eta=0.25\). If no expert match reaches the threshold, the score is multiplied by 0.50. The final 50 residual boxes are preserved and are not quality-gated, preventing the gate from erasing recovered residual candidates.

The box-voting step then refines local proposal geometry. For each primary proposal, neighboring boxes are selected by 3D IoU threshold 0.24. If a proposal has more than one neighbor, the method computes a score-weighted consensus box using weights \(w_j=\max(s_j,10^{-8})\). Coordinates and dimensions are averaged linearly, while heading is averaged in doubled-angle circular space. In the strict setting, only the BEV center coordinates are updated:

\[
b_i^{xy} \leftarrow (1-\lambda)b_i^{xy} + \lambda c_i^{xy},
\]

with voting strength \(\lambda=0.40\). Heading is also interpolated circularly between the original box and the consensus heading. Box dimensions are not changed in the strict `xy` mode. As in the quality gate, the final 50 residual boxes are preserved outside the voting pool.

This design makes the strict route conservative. Matched proposals are reinforced by expert agreement, unmatched proposals are down-weighted rather than removed, and local voting reduces BEV localization jitter without resizing boxes. The trade-off is additional post-processing latency, which is reported separately in the efficiency analysis.

### 3.7 Algorithm summary

```text
Algorithm 1: Reliability-oriented radar proposal refinement

Input:
  Radar point cloud X
  Baseline detector D
  Optional residual proposal stream R
  Optional expert proposal stream E

Output:
  Refined prediction set B

1. Run the detector D on X and obtain primary proposals P.
2. Apply candidate-preserving NMS with score threshold 0.0 and NMS threshold 0.50.
3. Recover top-50 residual proposals by IoU-based fusion or conservative appending.
4. Train quality-aligned scoring with q_hat = rho + (1-rho) * IoU^gamma.
5. Apply strict-route quality gating with match IoU 0.30.
6. Apply box voting with vote IoU 0.24, strength 0.40, and xy-mode updates.
7. Return the refined prediction set B.
```

### 3.8 Implementation and reproducibility details

All detectors are implemented in the OpenPCDet codebase [OpenPCDet2020]. The baseline uses a PointPillars-style architecture with PillarVFE, PointPillarScatter, and a 2D BEV backbone [PointPillars2019]. Experiments use AP\(_{R40}\) at 3D IoU 0.50 as the main metric [KITTI2012, SimonelliR40_2019] and are evaluated on Astyx, TruckScenes, V2X-Radar-V, and K-Radar [Astyx2019, TruckScenes2024, V2XRadar2024, KRadar2022]. The formal comparison uses three random seeds, 2026, 2027, and 2028. The strict robust route is selected by paired no-regression over the 12 dataset-seed comparisons, whereas the high-performance route is reported separately as the highest-macro operating point.

Runtime and parameter counts should be interpreted according to the route being evaluated. The trainable Q55 detector keeps the same parameter scale as the RDAR/PointPillars detector, whereas the strict voting route adds measurable post-processing time. Therefore, the method should be described as a reliability-cost trade-off rather than a zero-cost refinement.

## 4. Experiments and Results

This section has been formalized in `results/results_section_formal_v2.md`. The v2 draft should be treated as the current authoritative Results prose because it follows the final evidence hierarchy: main three-seed comparison, paired 12/12 strict robustness, progressive seed-2028 ablation, bounded diagnostics, point-dropout robustness, efficiency, and qualitative BEV analysis.

### 4.1 Experimental setup

We evaluated the proposed radar detection pipeline on Astyx, TruckScenes, V2X-Radar-V, and K-Radar. All formal comparisons used AP\(_{R40}\) at 3D IoU 0.50 as the primary metric. To reduce the risk of reporting seed-specific effects, the main comparison was repeated with three random seeds for each dataset and reported as mean and standard deviation. Unless otherwise specified, RDAR served as the primary baseline because it represents the strongest directly comparable recovery-oriented detector in the current experimental setting.

The evaluation was designed to separate three questions. First, we tested whether the final strict variant improved RDAR consistently across datasets and random seeds. Second, we used a progressive ablation to isolate the contribution of candidate preservation, residual recovery, quality alignment, and the high-performance route. Third, we analyzed calibration, robustness, efficiency, and qualitative behavior to determine which improvements were reliable enough for the main paper and which results should remain supplementary or internal.

### 4.2 Main comparison across four radar datasets

The strict robust proposal-voting variant improved RDAR on all four datasets in the three-seed formal comparison (Table 2). RDAR achieved a macro mean AP of 35.3552, while the strict robust route achieved 36.3278. The gains were moderate in average magnitude but consistent across all datasets: Astyx improved from 32.8347 ± 1.4689 to 33.6898 ± 1.7215, TruckScenes from 16.3671 ± 1.7480 to 17.2878 ± 1.7127, V2X-Radar-V from 41.7029 ± 1.1490 to 42.1245 ± 1.0852, and K-Radar from 50.5163 ± 2.0546 to 52.2091 ± 2.5654.

The high-performance route produced the highest macro mean AP, increasing the macro score to 39.1214. This variant delivered large gains on Astyx, V2X-Radar-V, and K-Radar, but it did not satisfy the strict no-regression criterion because TruckScenes seed2027 was lower than RDAR by 1.2770 AP. We therefore treat this route as a high-performance variant rather than the main robustness claim.

### 4.3 Progressive ablation

The progressive ablation showed how the final design emerged from the baseline detector (Table 4). In the seed2028 screen, the baseline PointPillars setting obtained a macro average of 33.9907. Adding candidate-preserving NMS increased the average to 35.7390, indicating that preserving more candidate boxes was beneficial before explicit recovery. Adding RDAR recovery further increased the average to 35.7559, giving a small but positive refinement. The quality-alignment route then produced the largest single improvement, raising the average to 39.1379. The high-performance calibration variant further increased the average to 39.7825.

This ablation is used as a module-contribution screen rather than as a strict three-seed monotonic ablation. The formal three-seed robustness claim is instead supported by the strict proposal-voting route, which was evaluated against RDAR in all 12 seed-dataset comparisons.

### 4.4 Cross-seed robustness of the strict route

We defined strict robustness as positive improvement over RDAR for every dataset and random seed, rather than allowing a tolerance band for small regressions. Under this definition, the strict proposal-voting route improved RDAR in all 12 paired comparisons. The minimum paired gain was +0.1718 AP on V2X-Radar-V seed2027, and the maximum gain was +2.6060 AP on K-Radar seed2026. Across the 12 paired differences, the mean gain was +0.9726 AP and the median gain was +0.8493 AP. A bootstrap estimate of the mean paired gain yielded a 95% confidence interval of [0.6468, 1.3536]. An exact sign test gave a two-sided p-value of 0.000488; this statistic is reported only as auxiliary evidence because the number of paired comparisons is limited.

These results support the main robustness claim: the strict route does not merely improve the macro mean, but avoids seed-dataset regressions under the formal comparison protocol.

### 4.5 Calibration and diagnostic analysis

The diagnostic analysis separated calibration improvements from proposal-voting robustness. The high-performance route improved expected calibration error against RDAR in all 12 diagnostic comparisons. In the seed2028 diagnostic table, ECE decreased from 0.5442 to 0.4693 on Astyx, from 0.3313 to 0.2906 on TruckScenes, from 0.6034 to 0.5680 on V2X-Radar-V, and from 0.6533 to 0.5688 on K-Radar. This supports the interpretation that the high-performance route improves confidence-quality alignment and ranking behavior.

By contrast, range-wise and sparsity-wise recall diagnostics were mixed. The strict route achieved 11 wins and 1 loss in overall recall, but its range-bin and sparsity-bin results included both wins and losses. The high-performance route showed strong ECE improvements but also mixed recall-bin behavior. We therefore do not claim universal superiority on far-range or sparse-bin targets. These diagnostics define the boundary of the method rather than serving as global positive evidence.

### 4.6 Robustness under inference-time point dropout

We further evaluated robustness using deterministic random point dropout at inference time. Radar points were randomly dropped before voxelization at rates of 10%, 20%, and 30%, without retraining. Under this stress test, the high-performance route maintained a higher macro AP than RDAR at every dropout rate. At 10% dropout, macro AP was 39.8078 for the high-performance route and 33.0908 for RDAR. At 20% dropout, the corresponding values were 38.4806 and 31.8445. At 30% dropout, they were 37.8866 and 32.3692.

At the per-dataset level, the high-performance route exceeded RDAR in 11 of 12 dropout cells. The only negative cell was TruckScenes at 30% dropout, where the high-performance route was lower by 0.0606 AP. Consequently, we use this experiment as average robustness evidence and not as a strict all-cell robustness claim.

We also tested whether applying box voting directly to the q55 dropout prediction files could repair this single negative cell. A post-hoc setting selected on TruckScenes 30% dropout produced 12/12 positive cells against RDAR, but the minimum margin was only +0.0010 AP and the voting step reduced the original q55 dropout AP in 8 of 12 cells. We therefore keep this probe internal, or at most as a supplementary caveat, rather than using it as a main robustness result.

### 4.7 Efficiency and runtime

The quality-alignment and high-performance routes preserve the same 4.830M trainable-parameter count as RDAR. The strict-route expert has 4.868M parameters, and the final voting operation itself adds no trainable parameters. In a fixed-protocol detector profiler measuring model forward and OpenPCDet post-processing, RDAR required 4.740 ms/frame on Astyx, 3.851 ms/frame on TruckScenes, 4.834 ms/frame on V2X-Radar-V, and 5.887 ms/frame on K-Radar. The high-performance route required 8.263, 7.880, 8.124, and 8.601 ms/frame on the same datasets.

The current implementation of strict proposal voting adds approximately 22 ms/frame as a separate post-processing stage. We therefore report it transparently as a robustness-oriented variant with additional post-processing cost, rather than presenting it as a free runtime improvement.

### 4.8 Qualitative analysis

Representative BEV cases show that strict proposal voting can refine borderline detections that RDAR localizes below the matching threshold (Fig. 2). On Astyx frame 000499, the IoU for the selected target increased from 0.4203 with RDAR to 0.5235 with the strict route. On TruckScenes frame 000267, IoU increased from 0.4940 to 0.6599. On V2X-Radar-V frame 000361, IoU increased from 0.4970 to 0.5420. These examples support the proposal-refinement interpretation of the strict route, but they are not used as evidence for universal range-wise or sparsity-wise superiority.

## 5. Discussion

The main finding is that proposal-level refinement can improve sparse radar 3D detection reliability when the evaluation explicitly separates strict robustness from high average performance. The strict proposal-voting route produced only a moderate macro-AP gain over RDAR, but its paired behavior was consistent: it improved all 12 dataset-seed comparisons. This is the central evidence for the robustness claim. The high-performance route, in contrast, produced a much larger macro mean but contained one TruckScenes seed-level regression. Reporting both routes avoids conflating two different operating points.

The ablation and diagnostics suggest that the framework works through complementary proposal mechanisms. Candidate-preserving NMS keeps boxes that would otherwise be removed too early. Residual recovery conservatively reintroduces weak candidates. Quality-aligned scoring improves ranking by coupling confidence with localization quality, as supported by the ECE diagnostics for the high-performance route. Proposal voting then trades additional post-processing time for a stricter consensus route. This interpretation is consistent with the BEV examples, where borderline boxes are shifted from below-threshold localization to valid matches.

Several alternative explanations and boundaries should be stated explicitly. The progressive ablation is a seed2028 screen and should not be presented as proof that every intermediate module monotonically improves every seed. The strict route should not be described as calibration-improving, because its ECE diagnostics worsen despite its paired AP gains. Range-wise and sparsity-wise recall analyses are mixed and do not support a universal far-range or sparse-bin superiority claim. Point-dropout results support average robustness for the high-performance route, but not strict all-cell robustness.

The method also has a clear cost boundary. The Q55 route preserves the same parameter scale as RDAR but is slower in the fixed detector profiler. The strict voting route adds no trainable parameters but introduces approximately 22 ms/frame of post-processing overhead in the current implementation. This overhead is acceptable for a reliability-oriented analysis route, but it should not be presented as a zero-cost deployment method. Optimizing the voting implementation is a practical engineering target for future work.

Future work should test whether the same proposal-level reliability pattern generalizes beyond single-class car detection and beyond the current four-dataset protocol. Additional matched-seed stress tests, optimized voting kernels, and broader radar benchmark splits would clarify whether strict no-regression behavior can be maintained under stronger distribution shifts. These directions should be treated as extensions of the current evidence, not as claims already established by the present experiments.

## 6. Conclusion

This study shows that proposal-level refinement is a practical route to more reliable sparse radar 3D detection. The strict proposal-voting route improved RDAR in all 12 paired seed-dataset comparisons across four radar datasets and three random seeds, while a separate high-performance route demonstrated the larger AP potential of quality-aligned scoring. By separating strict robustness from high average performance and by reporting mixed diagnostics transparently, the evaluation provides a defensible basis for using proposal preservation, recovery, quality alignment, and voting in radar detection systems.

## Planned figures and tables

Detailed placement, captions, claim boundaries, and main/supplement/internal decisions are fixed in `results/final_table_placement_and_captions.md`.

### Main figures

- Figure 1: Method overview, based on `results/figure1_method_overview_spec.md`. This figure should show the four separable failure points and modules: RC-NMS candidate preservation, residual recovery, confidence-quality alignment, and conservative proposal voting.
- Figure 2: Qualitative BEV examples, using Astyx frame 000499, TruckScenes frame 000267, and V2X-Radar-V frame 000361. This figure supports proposal/localization improvement examples, not universal failure-mode resolution.
- Optional Figure 3: Main AP comparison or efficiency trade-off, depending on page budget. If used, it must explicitly distinguish the strict robust route from the high-performance route.

### Main tables

- Table 1: Dataset and protocol summary over Astyx, TruckScenes, V2X-Radar-V, and K-Radar.
- Table 2: Main formal comparison over four datasets and three seeds, with RDAR, strict robust proposal voting, and the high-performance route.
- Table 3: Strict paired robustness deltas and statistical summary, including the 12/12 positive paired cells and bounded statistical summary.
- Table 4: Seed2028 progressive ablation from PointPillars to M1/M2/M3/M4. This table is a controlled progressive screen, not a full three-seed monotonic ablation.
- Table 5: Efficiency and overhead, separating trainable parameters, fixed detector profiler latency, and strict voting post-processing overhead.

### Supplementary tables

- Supplementary Table S1: High-performance route paired deltas, including the TruckScenes seed2027 regression caveat.
- Supplementary Table S2: Calibration diagnostics for q55, with strict-route ECE kept out of positive calibration claims.
- Supplementary Table S3: Threshold sensitivity grid for strict voting.
- Supplementary Table S4: Point-dropout robustness, reported as average robustness with the TruckScenes 30% caveat.
- Supplementary Table S5: Detector latency traceability from existing logs.
- Supplementary Table S6: Algorithm and pseudocode if the main-text method section exceeds the target page budget.

### Internal-only evidence

- Range/sparsity recall as a global improvement claim.
- Strict-route ECE as a calibration improvement claim.
- q55 or q55+voting as a strict no-regression method.
- Dropout prediction voting as a positive main result.
- Any universal statement beyond the evaluated datasets, splits, and seeds.

## Current missing inputs before final submission draft

1. Target journal/template decision, including whether algorithm boxes are supported and whether the paper should follow an IEEE Access-style layout.
2. Final rendered Figure 1 method overview.
3. Final Astyx DOI/reference-style audit and final bibliography formatting.
4. Optional stronger detector baseline, if the target venue requires comparison beyond RDAR/PointPillars-derived routes.
5. Optional full three-seed module ablation, if we want to upgrade Table 4 from a progressive screen to formal monotonic module evidence.
