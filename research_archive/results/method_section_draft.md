# Method section draft

This draft is written as a manuscript-ready Method section. It uses the current code/config evidence and keeps the main claim bounded: the contribution is a reliability-oriented radar proposal refinement framework, not a fully new detector backbone.

## One-sentence argument

In sparse radar-only 3D detection, we improve cross-dataset and cross-seed reliability by progressively preserving weak proposals, recovering residual candidates, aligning confidence with localization quality, and refining locally consistent boxes, while explicitly separating the high-performance route from the strict no-regression route.

## 3. Method

### 3.1 Task formulation

Given a radar point cloud for a frame, the detector predicts a set of 3D bounding boxes, class labels, and confidence scores. We focus on single-class car detection under the dataset protocols used for Astyx, TruckScenes, V2X-Radar-V, and K-Radar. Let a detector output be denoted as \(P=\{(b_i,s_i)\}_{i=1}^{N}\), where \(b_i \in \mathbb{R}^{7}\) represents the 3D box parameters and \(s_i\) is the confidence score. The objective is not only to increase the mean AP, but also to reduce seed- and dataset-specific regressions that are often hidden by average performance.

Sparse radar scenes create three practical difficulties for proposal ranking. First, useful low-confidence proposals may be removed by strict score filtering or overly aggressive non-maximum suppression. Second, weak-object evidence may appear in a complementary residual proposal stream but remain absent from the primary output. Third, classification confidence is not always aligned with localization quality, so a poorly localized box can outrank a better candidate. The proposed framework addresses these failure modes through four progressive components: candidate-preserving NMS, residual proposal recovery, quality-aligned scoring, and consistency-aware proposal refinement.

### 3.2 Framework overview

The framework is built on a PointPillars-style radar detector and refines its proposal generation and ranking behavior rather than replacing the entire backbone. The baseline detector uses a PillarVFE, a 2D BEV backbone, and a single-stage anchor head. In the baseline configuration, car anchors use size \([4.003, 1.800, 1.510]\), bottom height \(-0.180\), matched/unmatched IoU thresholds of 0.60/0.45, score threshold 0.10, NMS threshold 0.01, and pre-/post-NMS limits of 4096/500.

The full pipeline contains four stages. M1 relaxes the post-processing gate to preserve more candidate boxes. M2 adds a residual recovery stage that either fuses residual boxes with matched primary boxes or appends them with conservative scores. M3 replaces binary classification targets with IoU-derived soft quality targets so that proposal confidence better reflects localization quality. M4 constructs the strict robust route by applying expert quality gating and local box voting, selecting the operating point by a no-regression criterion over all paired dataset-seed comparisons. M1, M2, and M4 are proposal-level refinement steps, whereas M3 is the trainable scoring head.

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

2. Candidate-preserving NMS:
     apply score threshold 0.0 and NMS threshold 0.50
     keep at most 500 proposals after NMS.

3. Residual proposal recovery:
     keep the top 50 residual proposals from R.
     for each residual proposal:
       if its best 3D IoU with a primary proposal is at least 0.10:
          fuse the two boxes by score-weighted averaging;
       else:
          append the residual box unchanged.
       assign a conservative residual score below the
       positive primary-score ceiling.

4. Quality-aligned scoring:
     during training, replace binary positive classification
     targets with IoU-derived quality targets:
       q_hat = rho + (1-rho) * IoU^gamma,
       where rho=0.55 and gamma=1.0.
     optimize quality focal BCE with beta=2.0.

5. Strict-route quality gate:
     for each primary proposal, find the best expert match.
     if IoU >= 0.30:
        reweight the score using primary score, expert score,
        and IoU with alpha=0.30 and iou_power=0.25;
     else:
        multiply the score by 0.50.
     preserve the final 50 residual proposals.

6. Box voting:
     for each primary proposal, find neighbors with 3D IoU >= 0.24.
     compute a score-weighted consensus box.
     update only x-y center coordinates with strength 0.40
     and interpolate heading circularly.
     preserve the final 50 residual proposals.

7. Return the refined proposal set B.
```

### 3.8 Implementation and reproducibility details

All detectors are implemented in the OpenPCDet codebase. The baseline uses a PointPillars-style architecture with PillarVFE, PointPillarScatter, and a 2D BEV backbone. Experiments use AP\(_{R40}\) at 3D IoU 0.50 as the main metric and are evaluated on Astyx, TruckScenes, V2X-Radar-V, and K-Radar. The formal comparison uses three random seeds, 2026, 2027, and 2028. The strict robust route is selected by paired no-regression over the 12 dataset-seed comparisons, whereas the high-performance route is reported separately as the highest-macro operating point.

Runtime and parameter counts should be interpreted according to the route being evaluated. The trainable Q55 detector keeps the same parameter scale as the RDAR/PointPillars detector, whereas the strict voting route adds measurable post-processing time. Therefore, the method should be described as a reliability-cost trade-off rather than a zero-cost refinement.

## Chinese notes for the manuscript

- 这版 Method 的核心是“proposal refinement framework”，不是“全新 backbone”。这样可以避免审稿人质疑 M1/M2/M4 只是后处理。
- M3 是唯一明确的 trainable scoring head，可以写得更像模型创新；M1/M2/M4 要写成 proposal-level refinement。
- 主 claim 应该绑定 strict robust route：12/12 dataset-seed positive。高性能 q55rpa50_kprior 只能写成另一个 operating point。
- ECE 只能支撑 Q55 route 的 confidence-quality alignment，不能支撑 strict final route。
- Algorithm 1 现在是文本版，后续选定 LaTeX 模板后可以转成 `algorithmic` 或 `algorithm2e`。

## Items still needing final template decisions

1. Whether the journal template supports `algorithm`, `algorithm2e`, or only plain pseudocode.
2. Whether method details stay in the main Method section or some parameter blocks move to Supplementary Methods.
3. Whether the final method name should be a short acronym. Current safe descriptive name: reliability-oriented radar proposal refinement framework.
