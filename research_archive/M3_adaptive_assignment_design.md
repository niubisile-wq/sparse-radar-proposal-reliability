# M3 candidate: density-robust quality-aware assignment

## Problem exposed by the experiments

The four radar datasets use the same PointPillars detector but have very
different return density, box statistics and attribute scales. The current
anchor assigner uses fixed positive/negative IoU thresholds. Consequently,
the number and quality of positive anchors can change sharply across datasets
and random seeds.

Residual quality-focal classification demonstrates that localization quality
is useful, but it cannot pass the paired significance gate with the fixed
positive set. DTQC shows that merely adding a second objectness branch does
not solve Astyx. This localizes the next hypothesis upstream: the unstable
supervision may come from which anchors are declared positive, not only from
how their scores are trained.

## Literature basis

- ATSS (CVPR 2020) argues that positive/negative sample definition is the
  essential performance difference between anchor-based and anchor-free
  detectors, and selects positives from per-object IoU statistics:
  https://openaccess.thecvf.com/content_CVPR_2020/html/Zhang_Bridging_the_Gap_Between_Anchor-Based_and_Anchor-Free_Detection_via_Adaptive_CVPR_2020_paper.html
- TOOD (ICCV 2021) identifies classification/localization misalignment and
  uses task-aligned sample assignment and loss:
  https://openaccess.thecvf.com/content/ICCV2021/html/Feng_TOOD_Task-Aligned_One-Stage_Object_Detection_ICCV_2021_paper.html
- GFL (NeurIPS 2020) integrates localization quality into dense
  classification:
  https://proceedings.neurips.cc/paper/2020/hash/f0bda020d2470f2e74990a07a607ebd9-Abstract.html

## Candidate mechanism

For each ground-truth box:

1. select the nine nearest anchor centers;
2. calculate candidate BEV IoUs;
3. set the positive threshold to candidate `mean(IoU) + std(IoU)`;
4. require the anchor center to lie inside the target box;
5. force one unique best anchor per target if the statistical rule yields no
   positive.

The classifier then uses `q = 0.55 + 0.45 * IoU3D` for assigned positives.
This couples adaptive positive selection with quality-aware ranking while
retaining the radar-safe objectness residual.

## Factorial screen

The current experiment separates the factors:

| Variant | Adaptive assignment | Quality target | Independent objectness |
|---|---:|---:|---:|
| RDAR reference | no | no | no |
| `atss` | yes | no | no |
| `qflr55atss` | yes | yes | no |
| `dtqcatss` | yes | yes | yes |

The same `TOPK=9`, training schedule and post-processing are used for every
dataset. No dataset-specific assignment or score parameter is allowed.

## Acceptance

The best eligible formulation must:

1. improve all four datasets for all three seeds;
2. achieve at least +1.0 mean AP per dataset over the sequential RDAR
   reference;
3. have paired 95% CI lower bound above zero for every dataset;
4. show that its claimed factor contributes positively in the factorial
   comparison.
