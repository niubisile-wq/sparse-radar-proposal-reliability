# M3 candidate: radar-safe classification–localization alignment

## Evidence from prior work

- GFL merges localization quality into the class score so NMS ranks boxes by a
  joint objectness/quality representation:
  https://proceedings.neurips.cc/paper/2020/hash/f0bda020d2470f2e74990a07a607ebd9-Abstract.html
- VarifocalNet learns an IoU-aware classification score and reports that a
  separate quality branch or multiplication of two imperfect scores can be
  suboptimal:
  https://openaccess.thecvf.com/content/CVPR2021/html/Zhang_VarifocalNet_An_IoU-Aware_Dense_Object_Detector_CVPR_2021_paper.html
- TOOD argues that classification and localization optima are spatially
  misaligned and addresses the problem with task-aligned learning:
  https://openaccess.thecvf.com/content/ICCV2021/html/Feng_TOOD_Task-Aligned_One-Stage_Object_Detection_ICCV_2021_paper.html
- GFLV2 uses predicted localization uncertainty to improve quality estimation:
  https://openaccess.thecvf.com/content/CVPR2021/html/Li_Generalized_Focal_Loss_V2_Learning_Reliable_Localization_Quality_Estimation_for_CVPR_2021_paper.html

## Observed radar-specific failure

Pure 3D-IoU soft classification targets improve denser radar datasets but
over-suppress sparse Astyx positives:

| Variant (seed 2028, after RC-NMS + RDAR) | Astyx | TruckScenes | V2X-Radar-V |
|---|---:|---:|---:|
| Pure QFL | 31.2389 | 16.3512 | 42.1657 |
| QFL with target floor 0.25 | 31.2768 | 18.2725 | 43.9726 |
| Existing RDAR reference | 34.3540 | 15.3041 | 41.3385 |

Conclusion: localization quality is useful, but it must not replace object
presence supervision when radar geometry is sparse.

## Prepared corrections

1. `qflr`: soft target `0.5 + 0.5 * IoU`, retaining an objectness residual.
2. `qflr75`: soft target `0.75 + 0.25 * IoU`, a more conservative residual.
3. `qflh`: convex loss `0.75 * binary_focal + 0.25 * quality_focal`, preserving
   the original objective while using quality only as ranking regularization.

The fixed global variant must pass all four datasets on seed 2028 before
formal seeds 2026/2027 are trained. Formal acceptance requires every paired
delta to be positive, mean gain at least 1 AP per dataset, and paired 95% CI
lower bound above zero.

## Failure diagnosis and DTQC correction

The fixed residual targets fail formal stability:

- residual 0.55 passes Astyx, but fails TruckScenes and V2X confidence
  intervals;
- residual 0.50 fails Astyx and TruckScenes confidence intervals;
- residual 0.525 regresses TruckScenes on the seed-2028 screen.

This is evidence that one logit is receiving two partially conflicting
learning signals. Sparse/noisy radar anchors need strong binary objectness
supervision, while AP ranking needs localization quality. A fixed convex
target cannot adapt when the relative reliability of these signals changes
across datasets or seeds.

DTQC therefore uses:

1. a residual-IoU quality-focal branch;
2. an independent binary-focal objectness branch;
3. geometric probability consensus for the final NMS score.

The design draws on the classification/localization misalignment identified
by TOOD, the ranking motivation of GFL/VarifocalNet, and the empirical radar
finding that pure IoU supervision suppresses sparse positives. Unlike the
failed single-logit target, each branch retains a well-defined task and the
fusion coefficient can be screened at inference without retraining.

The current screen evaluates a single global fusion coefficient first, then
checks `0.25, 0.35, 0.65, 0.75` from the same checkpoint. A coefficient is
eligible only if the same value improves all datasets; dataset-specific
coefficients are forbidden.
