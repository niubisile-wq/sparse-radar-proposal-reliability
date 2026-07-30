# Method details and reproducible pseudocode for the radar proposal refinement framework

This document converts the current implementation into manuscript-ready method details. It is intended to support the Method section, the ablation explanation, and reproducibility notes. Claims here are bounded to what the current code and experiments support.

## Recommended method framing

The method should be described as a lightweight proposal refinement framework for radar-only 3D object detection, not as a fully new detector backbone. The detector backbone remains PointPillars/RDAR-style. The proposed contribution is the progressive refinement of candidate preservation, residual recovery, quality-aligned scoring, and proposal-consistency voting.

Recommended module names:

- M1: candidate-preserving NMS (RC-NMS)
- M2: residual proposal recovery (RDAR recovery)
- M3: quality-aligned scoring (Q55 / quality focal head)
- M4: consistency-aware proposal refinement (quality gate + box voting)

Important boundary: M1, M2, and M4 are evaluation-time or proposal-level refinement components. M3 is the trainable quality-aligned head. Do not describe all four as trainable network layers.

## Baseline detector

The baseline is a PointPillars-style radar detector with:

- PillarVFE with `NUM_FILTERS=[64]`
- BaseBEVBackbone with layer counts `[3, 5, 5]`
- PointPillarScatter
- voxel size `[0.25, 0.25, 5.0]`
- point cloud range `[0, -25, -3, 60, 25, 2]`
- baseline car anchor size `[4.003, 1.800, 1.510]`
- baseline car anchor bottom height `-0.180`
- baseline car anchor thresholds: matched `0.60`, unmatched `0.45`
- baseline post-processing: score threshold `0.10`, NMS threshold `0.01`, pre-NMS max `4096`, post-NMS max `500`

These details should be reported in Implementation Details or Supplementary Reproducibility.

## M1: candidate-preserving NMS

### Motivation

Radar detections are sparse and noisy. Very strict NMS or score filtering can remove low-confidence but spatially plausible candidates before later refinement has a chance to recover them. M1 therefore keeps more proposals for downstream processing.

### Mechanism

Compared with the baseline post-processing, M1 relaxes candidate filtering:

- score threshold: `0.0`
- NMS threshold: `0.50`
- pre-NMS max: `4096`
- post-NMS max: `500`
- BEV attention disabled in the relevant no-attention/RPA-style configurations

### Manuscript-safe wording

Use:

> We first replace the overly aggressive candidate filtering with a candidate-preserving NMS setting, increasing the overlap tolerance and removing the score threshold before final ranking.

Avoid:

> We add a new neural module for NMS.

## M2: residual proposal recovery

### Motivation

Candidate-preserving NMS keeps more boxes, but it does not recover proposals that are present in a complementary detector stream and absent or poorly localized in the primary output. M2 uses a residual proposal list to either fuse with a matched primary box or append a low-score residual candidate.

### Mechanism

Implementation source: `evaluate_residual_dual_expert.py`.

Default settings:

- `match_iou = 0.10`
- `residual_topk = 50`
- residual addition score ceiling: `0.5 * min_positive_primary_score`

For each frame, the script loads a primary prediction list and a residual prediction list. Frame order is validated before fusion.

Pseudocode:

```text
Input:
  primary predictions P = {(b_i, s_i)}
  residual predictions R = {(r_j, t_j)}
  match_iou = 0.10
  residual_topk = 50

Keep top residual_topk residual boxes by residual score.
Set residual_ceiling = 0.5 * min positive primary score.

For each residual box r_j:
  Find the primary box b_i with maximum 3D IoU to r_j.

  If max_i IoU(r_j, b_i) >= match_iou:
      Fuse geometry by score-weighted averaging:
          b_fused = weighted_average(b_i, r_j; weights=s_i, t_j)
      Average heading in doubled-angle circular space.
      Add b_fused to the recovered proposal list.

  Else:
      Add r_j unchanged to the recovered proposal list.

  Assign a conservative residual score:
      s_residual = residual_ceiling * (0.5 + 0.5 * t_j / max_k t_k)

Output:
  concatenate primary proposals and recovered residual proposals
```

### Manuscript-safe wording

Use:

> The residual stream is not allowed to dominate ranking: recovered proposals are assigned scores below the positive primary-score ceiling.

This guards against the reviewer concern that the method simply floods evaluation with extra boxes.

## M3: quality-aligned scoring head

### Motivation

In single-stage anchor detectors, the classification score is not necessarily aligned with localization quality. A high classification logit may correspond to a poorly localized box, which harms proposal ranking and downstream NMS. M3 trains the classification target to encode localization quality.

### Mechanism

Implementation source: `pcdet/models/dense_heads/anchor_head_quality_focal.py`.

Config source: `pointpillars_q55rpa50_kprior_*_car.yaml`.

Core settings:

- dense head: `AnchorHeadQualityFocal`
- `QUALITY_FOCAL_BETA = 2.0`
- `QUALITY_IOU_POWER = 1.0`
- `QUALITY_TARGET_FLOOR = 0.0`
- `QUALITY_OBJECTNESS_RESIDUAL = 0.55`
- post-processing score threshold `0.0`
- NMS threshold `0.50`
- NMS pre/post max `4096 / 500`
- RPA-style anchor thresholds: matched `0.50`, unmatched `0.35`

Quality target:

```text
For each positive anchor:
  Decode the predicted box and the assigned target box.
  Compute aligned 3D IoU q in [0, 1].
  Apply optional power transform:
      q <- q ^ QUALITY_IOU_POWER
  Apply objectness residual:
      q_target = rho + (1 - rho) * q
      where rho = 0.55

For negative or ignored anchors:
  q_target follows the cared-anchor mask.

Classification loss:
  p = sigmoid(logit)
  modulation = |q_target - p| ^ beta
  L_cls = BCEWithLogits(logit, q_target) * modulation
```

Interpretation:

- `rho = 0.55` preserves a base objectness signal even when the online IoU target is imperfect.
- `beta = 2.0` emphasizes examples where predicted confidence and localization quality disagree.
- The module improves expected calibration error in the high-performance Q55 route, but the strict M4 route should not be claimed as calibration-improving because its ECE worsens in the current diagnostics.

### Manuscript-safe wording

Use:

> M3 aligns proposal confidence with localization quality by replacing binary positive labels with IoU-derived soft targets and a residual objectness floor.

Avoid:

> M3 universally improves calibration.

## M4: consistency-aware proposal refinement

The strict robust final model uses a two-step proposal-level refinement: expert quality gating followed by local proposal voting. This is the correct strict route for the main no-regression claim.

### M4a: expert quality gate

Implementation source: `evaluate_expert_quality_gate.py`.

Settings used by `run_m3_stable_one.sh`:

- `match_iou = 0.30`
- `alpha = 0.30`
- `iou_power = 0.25`
- `unmatched_scale = 0.50`
- `residual_count = 50`

Pseudocode:

```text
Input:
  RDAR/refined primary predictions P = {(b_i, s_i)}
  expert predictions E = {(e_j, u_j)}
  residual_count = 50

Define primary_count = len(P) - residual_count.
Only the first primary_count boxes are quality-gated;
the final residual_count boxes are preserved as residual additions.

For each primary box b_i:
  Find expert box e_j with maximum 3D IoU.

  If best IoU >= 0.30:
      s_i <- s_i^(1 - alpha) * u_j^alpha * IoU(b_i, e_j)^iou_power
      where alpha = 0.30 and iou_power = 0.25

  Else:
      s_i <- unmatched_scale * s_i
      where unmatched_scale = 0.50
```

Role:

- matched proposals are reweighted using both primary confidence and expert consensus;
- unmatched primary proposals are kept but down-weighted;
- residual additions are preserved to avoid erasing recovered candidates.

### M4b: box voting

Implementation source: `evaluate_box_voting.py`.

Settings used by `run_m3_stable_one.sh`:

- `vote_iou = 0.24`
- `strength = 0.40`
- `mode = xy`
- `score_power = 1.0`
- `residual_count = 50`

Pseudocode:

```text
Input:
  proposal boxes B = {(b_i, s_i)}
  vote_iou = 0.24
  strength = 0.40
  mode = xy
  residual_count = 50

Define primary_count = len(B) - residual_count.
Only boxes 1...primary_count participate in voting.
The final residual_count boxes are preserved.

For each primary box b_i:
  Find neighbors N_i = {b_j | IoU3D(b_i, b_j) >= vote_iou}.

  If |N_i| <= 1:
      keep b_i unchanged.

  Else:
      Compute weights w_j = max(s_j, 1e-8)^score_power.
      Compute a weighted consensus box c_i:
          coordinates and dimensions by weighted average;
          heading by doubled-angle circular averaging.

      Update only x and y coordinates:
          b_i[x,y] <- (1 - strength) * b_i[x,y] + strength * c_i[x,y]

      Update heading by circular interpolation between b_i and c_i
      using weights [1 - strength, strength].
```

Role:

- voting smooths local proposal jitter without changing box size in the strict `xy` mode;
- the low `vote_iou` threshold is intentional for sparse radar proposals, where near-duplicate boxes may have modest 3D IoU because of height and size noise;
- preserving residual additions prevents the voting step from undoing the recovery step.

### Manuscript-safe wording

Use:

> The final module refines localization through agreement among nearby proposals while preserving residual candidates. In the strict variant, only BEV position and heading are adjusted, which reduces localization jitter without resizing boxes.

Avoid:

> M4 is a zero-cost module.

The current efficiency diagnostics show that voting introduces a measurable post-processing cost. It is better to frame this as a reliability-cost trade-off.

## How the ablation should be interpreted

The five-row ablation table is a progressive construction table, not proof that every component is independently optimal. The correct interpretation is:

```text
Baseline detector
  + M1: keep candidates that strict filtering would remove
  + M2: recover complementary residual proposals
  + M3: align confidence with localization quality
  + M4: enforce local proposal consistency
```

The seed-2028 progressive table supports the construction story. The 3-seed strict comparison supports the final reliability claim.

Do not overclaim monotonic 3-seed improvement for every intermediate module unless the full 3-seed progressive ablation is run.

## Evidence hooks for the manuscript

Use the following evidence mapping:

| Claim | Supporting experiment | Safe status |
|---|---|---|
| The final strict variant improves RDAR reliably | 12/12 paired seed-dataset comparisons; sign test and bootstrap CI | Main text |
| The progressive design improves the macro average | seed-2028 five-row ablation across four datasets | Main text, but label as progressive/screening |
| Q55 improves confidence-quality behavior | ECE diagnostics for Q55 route | Supplement or short diagnostic paragraph |
| The strict route is not a calibration method | strict-route ECE worsens 12/12 | Limitation / do not claim calibration |
| The method improves dropout robustness on average | point dropout 10/20/30%, q55 wins 11/12 cells vs RDAR | Supplement or robustness subsection |
| Proposal voting trades runtime for reliability | profiler and detector-latency logs | Efficiency section |
| Visual localization quality improves in selected cases | BEV qualitative cases on Astyx, TruckScenes, V2X | Main figure |

## Recommended Method section paragraph order

1. Task formulation and baseline detector.
2. Overview of the four-stage proposal refinement pipeline.
3. M1 candidate-preserving NMS.
4. M2 residual proposal recovery.
5. M3 quality-aligned scoring.
6. M4 quality gate and box voting.
7. Training/evaluation implementation details.
8. Reproducibility and computational cost boundaries.

## Reviewer-risk notes

Expected reviewer attack:

> Several proposed components are post-processing heuristics rather than trainable model innovations.

Response:

> The paper's contribution is deliberately framed as a reliability-oriented radar proposal refinement framework. We separate the trainable quality-aligned head from the proposal-level refinement steps and evaluate the entire pipeline under paired multi-seed, multi-dataset conditions. The ablation table isolates the contribution of each stage to the final detection behavior.

Expected reviewer attack:

> The high-performance model is not strictly better on every seed.

Response:

> The paper reports two variants with different operating points. The high-performance variant gives the best macro AP, whereas the strict robust variant is selected for the main no-regression claim because it improves all 12 paired dataset-seed comparisons.

Expected reviewer attack:

> Voting adds runtime.

Response:

> We explicitly report the post-processing overhead and frame the strict variant as a reliability-cost trade-off. For latency-sensitive deployment, the Q55 detector remains below 10 ms/frame in the fixed detector profiler.
