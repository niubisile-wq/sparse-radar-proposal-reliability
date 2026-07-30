# Verified reference plan for manuscript working draft v1

Status: draft reference-support map. This file lists references that have been checked against primary or near-primary sources and maps each reference to the manuscript claim it should support. It does not yet replace a final BibTeX file.

## Verification rules used

- Prefer primary sources: arXiv/CVF/NeurIPS proceedings/KITTI official pages/dataset official GitHub pages.
- Use secondary sources only when the primary source is unavailable or only to triangulate metadata.
- Do not cite unsupported claims.
- Do not invent RDAR metadata. No reliable public RDAR citation was found in the project files or targeted web searches. Until the exact source is provided, treat RDAR as an experimental baseline/route name rather than a cited external method.

## Core references by manuscript role

### Radar datasets

| Manuscript use | Reference | Verified source | Status | Notes |
|---|---|---|---|---|
| Astyx dataset description | Meyer and Kuschk, "Automotive Radar Dataset for Deep Learning Based 3D Object Detection", EuRAD 2019 | IEEE Xplore metadata found; document 8904734 | Verified enough for draft | BibTeX now includes IEEE EuRAD 2019, pp.129-132, and IEEE URL. DOI can still be checked before final submission. |
| TruckScenes dataset | Fent et al., "MAN TruckScenes: A multimodal dataset for autonomous trucking in diverse conditions", NeurIPS Datasets and Benchmarks 2024 / arXiv:2407.07462 | NeurIPS page and arXiv found | Verified | Supports 740+ scenes, 4 cameras, 6 lidar, 6 radar, 4D radar, annotated 3D boxes. |
| V2X-Radar / V2X-Radar-V | Yang et al., "V2X-Radar: A Multi-modal Dataset with 4D Radar for Cooperative Perception", arXiv:2411.10962 and official GitHub | arXiv and official GitHub citation found | Verified for draft | Official repository lists final authors and NeurIPS 2025 citation. Supports V2X-Radar-I/V/C split, V2X-Radar-V, 20K LiDAR frames, 20K 4D radar data, 350K boxes, 5 classes. |
| K-Radar | Paek, Kong, and Wijaya, "K-Radar: 4D Radar Object Detection for Autonomous Driving in Various Weather Conditions", NeurIPS Datasets and Benchmarks 2022 / arXiv:2206.08171 | NeurIPS PDF and arXiv found | Verified | Supports 35K 4D radar frames, adverse weather, 3D boxes, 5 classes. |

### Detector backbone and implementation

| Manuscript use | Reference | Verified source | Status | Notes |
|---|---|---|---|---|
| PointPillars baseline | Lang et al., "PointPillars: Fast Encoders for Object Detection from Point Clouds", CVPR 2019 / arXiv:1812.05784 | arXiv and CVF found | Verified | Supports pillar representation and efficient point-cloud detector backbone. |
| OpenPCDet implementation basis | OpenPCDet Development Team, "OpenPCDet: An Open-source Toolbox for 3D Object Detection from Point Clouds", GitHub, 2020 | official GitHub found | Verified as software citation | Use the repository citation style if no formal DOI is available. |
| RDAR baseline | Internal experimental baseline/route name | Project files and targeted web search checked | No external citation used | Manuscript wording now defines RDAR as the recovery-oriented primary baseline route in this study. If the user later provides an original RDAR paper/source, add it to Related Work and BibTeX. |

### Proposal filtering, NMS, and voting

| Manuscript use | Reference | Verified source | Status | Notes |
|---|---|---|---|---|
| General NMS background | Neubeck and Van Gool, "Efficient Non-Maximum Suppression", ICPR 2006 | Semantic Scholar and PDF found | Verified enough | Cite for NMS as standard suppression primitive if needed. |
| Soft/non-removal NMS motivation | Bodla et al., "Soft-NMS -- Improving Object Detection With One Line of Code", ICCV 2017 / arXiv:1704.04503 | CVF and arXiv found | Verified | Supports the idea that hard suppression can hurt and score decay/preservation can help. |
| Box voting / localization refinement | Gidaris and Komodakis, "Object Detection via a Multi-region & Semantic Segmentation-Aware CNN Model", ICCV 2015 / arXiv:1505.01749 | CVF and arXiv found | Verified | Use cautiously: supports iterative localization/box refinement and box-voting lineage, not our exact 3D radar voting. |
| 3D voting intuition | Qi et al., "Deep Hough Voting for 3D Object Detection in Point Clouds", ICCV 2019 / arXiv:1904.09664 | arXiv/PDF found | Verified | Use only as background for voting-based 3D object localization, not as equivalent method. |

### Confidence-quality alignment and loss design

| Manuscript use | Reference | Verified source | Status | Notes |
|---|---|---|---|---|
| Focal loss basis | Lin et al., "Focal Loss for Dense Object Detection", ICCV 2017 / arXiv:1708.02002 | arXiv and CVF found | Verified | Supports focal modulation and dense-detector class imbalance. |
| Quality Focal Loss / localization quality target | Li et al., "Generalized Focal Loss: Learning Qualified and Distributed Bounding Boxes for Dense Object Detection", NeurIPS 2020 | NeurIPS page and PDF found | Verified | Strong support for joint classification-localization quality target logic. |
| IoU-aware classification score | Zhang et al., "VarifocalNet: An IoU-aware Dense Object Detector", CVPR 2021 | CVF and IEEE page found | Verified | Supports learning confidence that jointly represents object presence and localization accuracy. |
| Noisy anchor soft-label motivation | Li et al., "Learning from Noisy Anchors for One-stage Object Detection", CVPR 2020 / arXiv:1912.05086 | arXiv found | Verified | Optional; supports binary anchor labels being noisy when positives vary in quality. |

### Calibration and reliability

| Manuscript use | Reference | Verified source | Status | Notes |
|---|---|---|---|---|
| Expected calibration error / neural calibration | Guo et al., "On Calibration of Modern Neural Networks", ICML 2017 / arXiv:1706.04599 | arXiv and PMLR PDF found | Verified | Supports ECE and confidence calibration motivation. |
| Object detector calibration caveats | Kuzucu et al., "On Calibration of Object Detectors: Pitfalls, Evaluation and Baselines", ECCV 2024 / arXiv:2405.20459 | arXiv and ECCV PDF found | Verified | Supports careful separation of detection calibration and AP. |
| Multi-seed evaluation/reproducibility | Henderson et al., "Deep Reinforcement Learning that Matters", AAAI 2018 / arXiv:1709.06560 | arXiv and publication page found | Verified but cross-domain | Use cautiously as general reproducibility motivation, not radar-specific. |
| Seed count and bootstrap significance | Colas et al., "How Many Random Seeds? Statistical Power Analysis in Deep Reinforcement Learning Experiments", arXiv:1806.08295 | arXiv found | Verified but cross-domain | Optional; supports seed/statistical-power discussion. |

### Evaluation metric

| Manuscript use | Reference | Verified source | Status | Notes |
|---|---|---|---|---|
| KITTI 3D AP / official benchmark | Geiger et al., "Are we ready for Autonomous Driving? The KITTI Vision Benchmark Suite", CVPR 2012; KITTI official evaluation page | CVF/official KITTI pages found | Verified | Supports KITTI-style detection evaluation context. |
| AP_R40 motivation | Simonelli et al., "Disentangling Monocular 3D Object Detection", ICCV 2019 / arXiv:1905.12365 | CVF/arXiv found | Verified | Supports AP_R40 replacing older 11-point AP in KITTI-style 3D evaluation. |

## Suggested citation placement in manuscript

### Introduction

- Radar robustness/adverse-weather motivation: K-Radar; TruckScenes; V2X-Radar.
- Radar sparsity/noise challenge: K-Radar; radar detection/fusion papers if added later.
- Pillar-style detector background: PointPillars; OpenPCDet.
- Reliability/multi-seed motivation: Henderson et al.; Colas et al. optional.

### Related Work

- Radar 3D object detection datasets: Astyx, K-Radar, TruckScenes, V2X-Radar.
- Proposal filtering/refinement: NMS, Soft-NMS, box voting, VoteNet.
- Confidence-quality alignment: Focal Loss, Generalized Focal Loss, VarifocalNet, Noisy Anchors.
- Calibration: Guo et al.; object detector calibration paper.

### Method

- PointPillars/OpenPCDet for backbone/implementation.
- Soft-NMS/NMS only for motivation of candidate-preserving suppression.
- Generalized Focal Loss / VarifocalNet / Focal Loss for M3 quality-aligned scoring.
- Box-voting references only for high-level lineage; our exact 3D radar voting remains our implementation.

### Experiments

- Dataset citations beside each dataset name.
- KITTI/Simonelli citation near AP\(_{R40}\) definition.
- Multi-seed/reproducibility citation in protocol paragraph if the target venue expects rationale.

## Citation keys to use temporarily

Use these temporary keys until the final BibTeX is generated:

```text
[PointPillars2019]
[OpenPCDet2020]
[Astyx2019]
[TruckScenes2024]
[V2XRadar2024]
[KRadar2022]
[NMS2006]
[SoftNMS2017]
[BoxVoting2015]
[VoteNet2019]
[FocalLoss2017]
[GFL2020]
[VarifocalNet2021]
[NoisyAnchors2020]
[GuoCalibration2017]
[DetectorCalibration2024]
[HendersonSeeds2018]
[ColasSeeds2018]
[KITTI2012]
[SimonelliR40_2019]
```

## Immediate reference tasks still open

1. Optional: if RDAR has a specific original paper/source, add it only after the exact metadata is provided or verified.
2. Confirm the final Astyx DOI before final submission; draft metadata is now sufficient for manuscript development.
3. Generate final BibTeX once the target journal style is known.
4. Completed: body-text `[cite]` placeholders in `manuscript_working_draft_v1.md` have been replaced with temporary keys. Later, convert these keys into final numbered or author-year citations according to the target journal style.
5. If adding stronger detector baselines, add their original method references at the same time.
