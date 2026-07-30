# Results Section Formal Draft v2

## One-sentence argument

Across four radar 3D detection datasets and three random seeds, the strict proposal-voting route provided the strongest no-regression evidence against RDAR, while the quality-aligned high-performance route exposed the larger AP headroom but was kept separate because it did not satisfy the paired no-regression criterion.

## Section outline

1. Experimental setup and evidence hierarchy.
2. Main three-seed comparison.
3. Paired strict robustness.
4. Progressive module ablation.
5. Calibration and diagnostic boundaries.
6. Inference-time point-dropout robustness.
7. Efficiency and runtime.
8. Qualitative BEV evidence.

## Draft

### 4. Experiments and Results

#### 4.1 Experimental setup

We evaluated the proposed proposal-reliability pipeline on four radar 3D detection datasets: Astyx, TruckScenes, V2X-Radar-V, and K-Radar. All formal comparisons used AP_R40 at 3D IoU 0.50 for the car class as the primary metric. The main comparison was repeated with three random seeds, 2026, 2027, and 2028, and is reported as mean and standard deviation across seeds. RDAR denotes the recovery-oriented primary baseline used in our experimental framework. The results were organized to separate two operating goals: strict paired robustness, where a method must improve RDAR in every seed-dataset pair, and high average performance, where a method may achieve a larger macro AP but is not treated as a no-regression route.

#### 4.2 Main comparison across four radar datasets

The strict robust proposal-voting route improved RDAR on all four datasets in the three-seed formal comparison (Table 2). RDAR achieved 32.8347 +/- 1.4689 AP on Astyx, 16.3671 +/- 1.7480 on TruckScenes, 41.7029 +/- 1.1490 on V2X-Radar-V, and 50.5163 +/- 2.0546 on K-Radar, corresponding to a macro mean of 35.3552. The strict route increased these results to 33.6898 +/- 1.7215, 17.2878 +/- 1.7127, 42.1245 +/- 1.0852, and 52.2091 +/- 2.5654, respectively, giving a macro mean of 36.3278. The absolute gains were therefore moderate in average magnitude but consistent in direction across all four datasets.

The high-performance route produced the largest macro mean AP, reaching 39.1214 across the four datasets. It achieved 36.9801 +/- 0.9748 AP on Astyx, 16.8063 +/- 1.1764 on TruckScenes, 44.3786 +/- 0.5122 on V2X-Radar-V, and 58.3208 +/- 1.6943 on K-Radar. However, this route did not satisfy the strict no-regression criterion because TruckScenes seed 2027 was 1.2770 AP below RDAR. We therefore report it as a high-performance route rather than as the main robustness route.

#### 4.3 Paired cross-seed robustness

To test robustness more directly than a mean AP comparison, we analyzed the paired AP difference between the strict route and RDAR for each dataset and seed (Table 3). The strict route improved RDAR in all 12 paired comparisons. The per-dataset mean gains were +0.8551 AP on Astyx, +0.9207 on TruckScenes, +0.4216 on V2X-Radar-V, and +1.6928 on K-Radar. Across the 12 paired cells, the mean gain was +0.9726 AP and the median gain was +0.8493 AP. The smallest positive gain was +0.1718 AP on V2X-Radar-V seed 2027, and the largest was +2.6060 AP on K-Radar seed 2026.

We used paired statistics only as supporting evidence for this finite evaluation set. A bootstrap estimate of the mean paired gain gave a 95% confidence interval of [0.6468, 1.3536], and an exact sign test gave a one-sided p-value of 0.000244 and a two-sided p-value of 0.000488. Because the sample contains 12 paired comparisons, these statistics are reported as auxiliary evidence rather than as a claim of universal improvement beyond the evaluated datasets, splits, and seeds.

#### 4.4 Progressive module ablation

The progressive ablation quantified how the proposed modules changed performance when added sequentially under the seed-2028 screen (Table 4). The PointPillars baseline achieved an average AP of 33.9907 across the four datasets. Adding M1, the candidate-preserving RC-NMS stage, increased the average to 35.7390, with gains on all four datasets. Adding M2, the RDAR recovery stage, further increased the average to 35.7559, indicating a small but consistent refinement over candidate preservation alone.

The largest improvement in the progressive screen came from M3, the quality-aligned scoring route. This module increased the average AP from 35.7559 to 39.1379 and improved all four datasets in the seed-2028 comparison. Adding M4 in the high-performance calibration route further increased the average to 39.7825, with AP values of 37.8373 on Astyx, 17.8028 on TruckScenes, 43.7939 on V2X-Radar-V, and 59.6960 on K-Radar. This table is used as a controlled module-contribution screen, not as a full three-seed monotonic ablation. The formal no-regression evidence is provided by the strict paired comparison in Section 4.3.

#### 4.5 Calibration and diagnostic boundaries

Calibration diagnostics supported the interpretation that the high-performance route improved score-quality alignment. In the seed-2028 diagnostic table, expected calibration error decreased from 0.5442 to 0.4693 on Astyx, from 0.3313 to 0.2906 on TruckScenes, from 0.6034 to 0.5680 on V2X-Radar-V, and from 0.6533 to 0.5688 on K-Radar when comparing RDAR with the high-performance q55 route. Across the three-seed diagnostic gate, this route improved ECE in all 12 comparisons against RDAR.

The same diagnostics also defined the boundary of the method. Range-bin and sparsity-bin recall results were mixed, and the strict proposal-voting route worsened ECE despite improving AP in all paired formal comparisons. We therefore use calibration as evidence for the quality-aligned high-performance route only, and we do not claim universal range-wise, sparsity-wise, or calibration superiority for the full strict route.

#### 4.6 Robustness under inference-time point dropout

We evaluated inference-time robustness by applying deterministic random point dropout before voxelization, without retraining. At dropout rates of 10%, 20%, and 30%, the high-performance route maintained higher macro AP than RDAR. The macro AP values were 39.8078 versus 33.0908 at 10% dropout, 38.4806 versus 31.8445 at 20% dropout, and 37.8866 versus 32.3692 at 30% dropout.

At the dataset-by-dropout level, the high-performance route exceeded RDAR in 11 of 12 tested cells. The only negative cell was TruckScenes at 30% dropout, where the route was lower by 0.0606 AP. This experiment therefore supports average robustness under synthetic point sparsification, but it does not support a strict all-cell dropout robustness claim.

An additional exploratory probe applied box voting to q55 dropout predictions. This repaired the single negative q55-versus-RDAR dropout cell and produced 12/12 positive cells against RDAR, but the minimum margin was only +0.0010 AP and the voting step reduced q55 AP in 8 of 12 cells. We therefore keep this probe internal, or at most as a supplementary caveat, rather than using it as main evidence.

#### 4.7 Efficiency and runtime

The quality-aligned and high-performance routes preserved the same 4.830M trainable-parameter count as RDAR (Table 5). The strict-route expert used 4.868M parameters, and the proposal-voting operation itself added no trainable parameters. In the fixed detector profiler, RDAR required 4.740, 3.851, 4.834, and 5.887 ms/frame on Astyx, TruckScenes, V2X-Radar-V, and K-Radar, respectively. The high-performance route required 8.263, 7.880, 8.124, and 8.601 ms/frame on the same datasets, remaining below 10 ms/frame but slower than RDAR.

The current strict voting implementation added a separate post-processing overhead of approximately 22 ms/frame. Thus, the strict route should be presented as a robustness-oriented operating point with explicit overhead, not as a runtime-free improvement. This distinction is important because the high-performance route and strict route optimize different deployment goals.

#### 4.8 Qualitative analysis

Qualitative BEV examples showed how the strict route can improve borderline proposal localization (Figure 2). On Astyx frame 000499, the selected target IoU increased from 0.4203 with RDAR to 0.5235 with the strict route. On TruckScenes frame 000267, IoU increased from 0.4940 to 0.6599. On V2X-Radar-V frame 000361, IoU increased from 0.4970 to 0.5420. These examples support the interpretation that conservative proposal refinement can move borderline detections across the matching threshold, while remaining illustrative rather than exhaustive evidence.

## Claim-evidence map

| Claim | Evidence | Status |
|---|---|---|
| The strict route improves RDAR in every tested seed-dataset pair. | 12/12 positive paired AP deltas; min gain +0.1718 AP. | Supported for evaluated datasets/seeds. |
| The high-performance route gives the largest macro AP. | Macro AP 39.1214 versus 35.3552 for RDAR and 36.3278 for strict route. | Supported with TruckScenes seed2027 caveat. |
| The four modules form a coherent contribution chain. | Seed-2028 progressive ablation from 33.9907 to 39.7825 average AP. | Supported as screen evidence, not full three-seed monotonic evidence. |
| q55 improves calibration. | ECE improved in seed2028 on all four datasets and in 12/12 diagnostic cells. | Supported for q55/high-performance route. |
| The method universally improves range or sparsity recall. | Range/sparsity diagnostics are mixed. | Not supported; internal only as a global claim. |
| The strict route is runtime-free. | Strict voting adds about 22 ms/frame. | Not supported. |
| Point-dropout robustness is strict in all cells. | q55 wins 11/12 cells; TruckScenes 30% dropout is -0.0606 AP. | Supported only as average robustness. |

## Assumptions or missing inputs

- Final target template is still unspecified; section numbering and table limits may need adjustment.
- Table 4 remains a seed-2028 progressive screen unless a full three-seed module ablation is completed.
- Reference formatting still needs final target-journal style audit.

