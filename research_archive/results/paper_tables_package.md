# Paper tables package

## Table A. Main formal comparison (3 seeds)

This table is safe for the main paper if the claim is method-level performance rather than strict incremental M4 gain.

| Method | Astyx | TruckScenes | V2X-Radar-V | K-Radar | Macro mean | Strict 12/12 > RDAR |
|---|---:|---:|---:|---:|---:|:---:|
| RDAR baseline | 32.8347 ± 1.4689 | 16.3671 ± 1.7480 | 41.7029 ± 1.1490 | 50.5163 ± 2.0546 | 35.3552 | reference |
| High-performance route (q55rpa50_kprior) | 36.9801 ± 0.9748 | 16.8063 ± 1.1764 | 44.3786 ± 0.5122 | 58.3208 ± 1.6943 | 39.1214 | no |
| Strict robust proposal voting (m3rob_q15p25_viou0p24_s0p40) | 33.6898 ± 1.7215 | 17.2878 ± 1.7127 | 42.1245 ± 1.0852 | 52.2091 ± 2.5654 | 36.3278 | yes |

## Table B. Strict robust route deltas vs RDAR

| Dataset | Δ2026 | Δ2027 | Δ2028 | Mean Δ |
|---|---:|---:|---:|---:|
| astyx | 0.8222 | 0.6202 | 1.1228 | 0.8551 |
| truckscenes | 0.4765 | 0.8135 | 1.4721 | 0.9207 |
| v2xradarv | 0.2167 | 0.1718 | 0.8763 | 0.4216 |
| kradar | 2.6060 | 1.0864 | 1.3861 | 1.6928 |

## Table C. Seed-2028 progressive ablation

Use this as a screen/progressive ablation table, not as a 3-seed strict formal claim.

| Setting | Astyx | TruckScenes | V2X-Radar-V | K-Radar | Avg. |
|---|---:|---:|---:|---:|---:|
| Baseline / PointPillars | 30.5009 | 15.1291 | 40.0670 | 50.2659 | 33.9907 |
| +M1 / RC-NMS | 34.3392 | 15.2784 | 41.3191 | 52.0193 | 35.7390 |
| +M2 / RDAR recovery | 34.3540 | 15.3041 | 41.3385 | 52.0271 | 35.7559 |
| +M3 / quality alignment (qflr55) | 37.0318 | 17.4530 | 42.5979 | 59.4687 | 39.1379 |
| +M4 / high-performance calibration (q55rpa50_kprior) | 37.8373 | 17.8028 | 43.7939 | 59.6960 | 39.7825 |

## Table D. High-performance route formal deltas vs RDAR

This table explains why the high-performance route should not be used for a strict no-regression claim.

| Dataset | Δ2026 | Δ2027 | Δ2028 | Mean Δ | All positive |
|---|---:|---:|---:|---:|:---:|
| astyx | 3.1916 | 5.7613 | 3.4833 | 4.1454 | yes |
| truckscenes | 0.0959 | -1.2770 | 2.4987 | 0.4392 | no |
| v2xradarv | 3.8141 | 1.7578 | 2.4554 | 2.6758 | yes |
| kradar | 7.4932 | 8.2514 | 7.6689 | 7.8045 | yes |

## Table E. Calibration diagnostic (seed=2028)

ECE is useful because the detection AP gain is primarily ranking/calibration-driven; range/sparsity recall is mixed and should stay internal unless selectively discussed.

| Dataset | RDAR ECE | qflr55 ECE | q55rpa50_kprior ECE |
|---|---:|---:|---:|
| astyx | 0.5442 | 0.5041 | 0.4693 |
| truckscenes | 0.3313 | 0.3028 | 0.2906 |
| v2xradarv | 0.6034 | 0.5497 | 0.5680 |
| kradar | 0.6533 | 0.6309 | 0.5688 |

## Table F. Efficiency and overhead

Parameter counts are static trainable parameters from OpenPCDet configs. Voting latency measures only the strict robust box-voting refinement loop; it excludes pickle I/O and KITTI evaluation.

| Method/config group | Astyx | TruckScenes | V2X-Radar-V | K-Radar |
|---|---:|---:|---:|---:|
| RDAR / PointPillars-TAAC | 4.830 M | 4.830 M | 4.830 M | 4.830 M |
| M3 quality alignment (qflr55) | 4.830 M | 4.830 M | 4.830 M | 4.830 M |
| M4 high-performance (q55rpa50_kprior) | 4.830 M | 4.830 M | 4.830 M | 4.830 M |
| Strict-route expert (stable_bevgate) | 4.868 M | 4.868 M | 4.868 M | 4.868 M |

| Voting dataset | Frames | Stage seed | Voted boxes | Neighbor links | ms/frame |
|---|---:|---:|---:|---:|---:|
| astyx | 100 | 2027 | 47790 | 216560 | 22.7095 ± 0.1031 |
| truckscenes | 80 | 2027 | 37277 | 135592 | 22.0086 ± 0.1826 |
| v2xradarv | 80 | 2027 | 38009 | 148862 | 22.5393 ± 0.0471 |
| kradar | 80 | 2027 | 38457 | 149142 | 22.8485 ± 0.1735 |

## Table G. Detector latency from existing logs

Parsed from completed OpenPCDet eval logs containing `sec_per_example`. Unit: ms/frame. These values are useful for evidence tracking; use in the main paper only if the exact eval setting is stated.

| Method/log group | Astyx | TruckScenes | V2X-Radar-V | K-Radar |
|---|---:|---:|---:|---:|
| RDAR / TAAC + RC-NMS eval | 87.73 ± 7.26 (3 seeds) | 18.17 ± 1.50 (3 seeds) | 22.97 ± 2.59 (3 seeds) | 23.90 ± 3.05 (3 seeds) |
| M3 qflr55 + RC-NMS eval | 96.23 ± 12.33 (3 seeds) | 24.07 ± 3.43 (3 seeds) | 26.80 ± 6.37 (3 seeds) | 24.30 ± 0.89 (3 seeds) |
| M4 high-perf q55rpa50_kprior + RC-NMS eval | 73.50 ± 11.60 (2 seeds) | 17.95 ± 0.49 (2 seeds) | 21.65 ± 1.48 (2 seeds) | 23.47 ± 0.55 (3 seeds) |
| Strict-route expert stable_bevgate + RC-NMS eval | 77.27 ± 9.22 (3 seeds) | 17.77 ± 2.86 (3 seeds) | 20.10 ± 2.52 (3 seeds) | 21.33 ± 1.37 (3 seeds) |

## Table H. Diagnostic gate summary

Compares each variant against RDAR across 3 seeds × 4 datasets. Positive means better than RDAR; for ECE, positive means lower ECE.

| Variant | Metric | Win | Tie | Loss | Mean delta | Paper decision |
|---|---|---:|---:|---:|---:|---|
| m3rob_q15p25_viou0p24_s0p40 | overall_recall | 11 | 0 | 1 | 0.0045 | internal only |
| m3rob_q15p25_viou0p24_s0p40 | range_bins | 26 | 13 | 9 | 0.0038 | internal only |
| m3rob_q15p25_viou0p24_s0p40 | sparsity_bins | 18 | 19 | 8 | 0.0084 | internal only |
| m3rob_q15p25_viou0p24_s0p40 | ece_hit | 0 | 0 | 12 | -0.0270 | selective/internal |
| m3rob_q15p25_viou0p24_s0p40 | top10_iou | 9 | 0 | 3 | 0.0124 | selective/internal |
| m3rob_q15p25_viou0p24_s0p40 | score_iou_corr | 7 | 0 | 5 | 0.0102 | selective/internal |
| q55rpa50_kprior | overall_recall | 4 | 0 | 8 | -0.0010 | internal only |
| q55rpa50_kprior | range_bins | 17 | 10 | 21 | -0.0031 | internal only |
| q55rpa50_kprior | sparsity_bins | 19 | 9 | 17 | 0.0106 | internal only |
| q55rpa50_kprior | ece_hit | 12 | 0 | 0 | 0.0504 | keep |
| q55rpa50_kprior | top10_iou | 6 | 0 | 6 | 0.0052 | selective/internal |
| q55rpa50_kprior | score_iou_corr | 8 | 0 | 4 | 0.0155 | selective/internal |

## Table I. Fixed-protocol detector profiler

Protocol: batch_size=4, workers=2, warmup_batches=3, max_measure_batches=20. Measures model forward including OpenPCDet post-processing; excludes AP evaluation and result serialization.

| Method | Astyx | TruckScenes | V2X-Radar-V | K-Radar |
|---|---:|---:|---:|---:|
| rdar_taac | 4.740 ± 0.297 ms (seed 2028) | 3.851 ± 0.311 ms (seed 2028) | 4.834 ± 1.092 ms (seed 2028) | 5.887 ± 2.409 ms (seed 2028) |
| q55rpa50_kprior | 8.263 ± 1.163 ms (seed 2027) | 7.880 ± 1.257 ms (seed 2027) | 8.124 ± 1.334 ms (seed 2027) | 8.601 ± 1.471 ms (seed 2028) |

## Table J. Strict voting threshold sensitivity

All rows are evaluated on 4 datasets × 3 seeds. Shown are the top ranked settings by all-positive status and macro mean.

| Tag | vote_iou | strength | Macro | Pos/12 | Min Δ | All positive |
|---|---:|---:|---:|---:|---:|:---:|
| m3rob_q15p25_viou0p22_s0p40 | 0.22 | 0.40 | 36.1364 | 12/12 | 0.0252 | yes |
| m3rob_q15p25_viou0p24_s0p50 | 0.24 | 0.50 | 36.0479 | 12/12 | 0.1354 | yes |
| m3rob_q15p25_viou0p24_s0p35 | 0.24 | 0.35 | 36.3020 | 11/12 | -0.2945 | no |
| m3rob_q15p25_viou0p25_s0p35 | 0.25 | 0.35 | 36.2947 | 11/12 | -0.4330 | no |
| m3rob_q15p25_viou0p28_s0p40 | 0.28 | 0.40 | 36.2069 | 11/12 | -0.8951 | no |
| m3rob_q15p25_viou0p28_s0p35 | 0.28 | 0.35 | 36.2011 | 11/12 | -0.9079 | no |
| m3rob_q15p25_viou0p22_s0p35 | 0.22 | 0.35 | 36.1989 | 10/12 | -0.0705 | no |
| m3rob_q15p25_viou0p26_s0p40 | 0.26 | 0.40 | 36.1972 | 10/12 | -0.1494 | no |

## Keep / internal decision

| Evidence | Decision |
|---|---|
| Strict robust proposal voting | Keep in paper if the paper claims 3-seed all-dataset robustness. |
| q55rpa50_kprior | Keep as high-performance route or supplementary; do not claim strict all-seed no-regression. |
| qflr55 formal incremental result | Internal risk / partial formal evidence; TruckScenes seed2027 regresses. |
| Efficiency: parameter count | Keep. qflr55/q55rpa50_kprior keep the same 4.830M parameter count as RDAR; strict voting adds 0 trainable parameters. |
| Efficiency: current voting runtime | Keep as transparent overhead or optimize before claiming real-time; current implementation is about 22 ms/frame. |
| Detector latency from existing logs | Keep as evidence tracking; if used in main paper, state eval settings and missing q55 seeds. Dedicated profiler is still cleaner. |
| Fixed detector profiler | Keep for main-paper runtime if needed. q55 is slower than RDAR but still under 10 ms/frame in this profiler; strict voting overhead remains a separate post-processing cost. |
| Strict voting threshold sensitivity | Keep. 4/20 full-grid settings are 12/12 all-positive; selected s0p40 is best all-positive macro, supporting a stable plateau rather than a one-off setting. |
| Range and sparsity recall | Internal only as global claim; three-seed diagnostic gate has losses in bins for both strict and high-performance variants. |
| q55rpa50_kprior ECE | Keep. Three-seed diagnostic gate: 12/12 ECE improvements vs RDAR. |
| Strict route ECE | Internal. It worsens ECE in 12/12 diagnostics despite strict AP gains. |
| Failed sweeps | Internal exploration, not main paper. |