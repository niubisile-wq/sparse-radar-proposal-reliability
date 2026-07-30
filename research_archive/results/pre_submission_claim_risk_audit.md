# Pre-submission claim-risk audit

## Audit stance

This audit assumes a skeptical reviewer will check whether every claim is
supported by the actual experiment protocol. The safest manuscript strategy is
to lead with strict 3-seed evidence and explicitly separate main, supplementary,
and internal results.

## High-confidence claims

### Claim 1. The strict route improves RDAR across all tested seed-dataset pairs

Evidence:

- 4 datasets x 3 seeds = 12 paired comparisons.
- 12/12 positive deltas.
- Mean Delta AP = +0.9726.
- Min Delta AP = +0.1718.
- Bootstrap 95% CI for mean Delta AP = [0.6468, 1.3536].

Safe wording:

> The strict robust proposal-voting route improved RDAR in all 12 paired
> seed-dataset comparisons, with a mean gain of +0.9726 AP_R40@3D IoU 0.50.

Unsafe wording:

> The method is universally robust under all radar conditions.

Reason: only four datasets and three seeds were tested.

### Claim 2. The high-performance route gives the largest macro mean

Evidence:

- RDAR macro: 35.3552.
- q55rpa50_kprior macro: 39.1214.
- Strict route macro: 36.3278.

Safe wording:

> The high-performance route achieved the largest macro mean AP, but it did not
> satisfy the strict all-seed no-regression criterion.

Unsafe wording:

> q55 consistently outperforms RDAR across all seeds.

Reason: TruckScenes seed2027 is -1.2770.

### Claim 3. The progressive ablation supports the module design chain

Evidence:

- Seed2028 five-row ablation improves macro average from 33.9907 to 39.7825.

Safe wording:

> In the seed2028 progressive ablation, the four modules increased macro AP
> from 33.9907 to 39.7825.

Unsafe wording:

> Every module monotonically improves performance across all seeds.

Reason: only the five-row progressive ablation is seed2028; formal qflr55/q55
results include regressions in some seed-level comparisons.

### Claim 4. q55 improves confidence calibration

Evidence:

- q55 ECE diagnostic: 12/12 wins vs RDAR.
- Seed2028 ECE improves on all four datasets.

Safe wording:

> The high-performance route reduced ECE in all 12 diagnostic comparisons,
> supporting its role as a confidence-quality alignment variant.

Unsafe wording:

> The strict route improves calibration.

Reason: strict route ECE worsens in 12/12 diagnostic comparisons.

### Claim 5. The method has transparent parameter and runtime cost

Evidence:

- RDAR/q55/qflr55: 4.830M trainable parameters.
- Strict-route expert: 4.868M parameters.
- Strict voting adds 0 trainable parameters.
- q55 fixed profiler: about 7.880-8.601 ms/frame.
- RDAR fixed profiler: about 3.851-5.887 ms/frame.
- Voting overhead: about 22 ms/frame.

Safe wording:

> The high-performance route preserves the RDAR parameter count but is slower
> in the fixed profiler; the strict voting stage adds no trainable parameters
> but introduces measurable post-processing overhead.

Unsafe wording:

> The proposed method is cost-free or faster than RDAR.

Reason: q55 is slower than RDAR in the fixed profiler, and voting has
additional overhead.

## Medium-confidence / bounded claims

### Claim 6. q55 is robust to point dropout on average

Evidence:

- q55 wins 11/12 dropout cells vs RDAR.
- Mean q55 - RDAR AP margin = +6.2902.
- Macro AP remains higher at 10%, 20%, and 30% dropout.

Safe wording:

> Under inference-time point dropout, q55 maintained higher macro AP than
> RDAR at all tested dropout rates and won 11/12 per-dataset cells.

Unsafe wording:

> q55 is strictly robust to point dropout on all datasets.

Reason: TruckScenes 30% dropout is -0.0606.

### Claim 7. Strict voting threshold selection is stable

Evidence:

- 20 full threshold settings.
- 4 settings are 12/12 all-positive.
- Selected setting is the best all-positive macro.

Safe wording:

> Neighboring voting settings also achieved 12/12 positive paired comparisons,
> indicating that the selected threshold is not an isolated successful point.

Unsafe wording:

> The method is insensitive to all voting thresholds.

Reason: only a bounded local grid was tested; many settings are not all-positive.

## Claims to avoid

### Avoid 1. Global range/sparsity superiority

Evidence against:

- Strict route range bins: 26 wins / 13 ties / 9 losses.
- Strict route sparsity bins: 18 wins / 19 ties / 8 losses / 3 missing.
- q55 range/sparsity bins are also mixed.

Allowed alternative:

> Range- and sparsity-binned diagnostics revealed mixed behavior, so we treat
> these analyses as failure-boundary evidence rather than global superiority
> evidence.

### Avoid 2. qflr55 as a formal strict method

Evidence against:

- TruckScenes seed2027 regresses.

Allowed alternative:

> qflr55 is useful in the progressive seed2028 screen and as an internal route,
> but not as the formal strict method.

### Avoid 3. q55 as strict no-regression

Evidence against:

- TruckScenes seed2027 regresses by -1.2770.

Allowed alternative:

> q55 is the high-performance route and achieves the largest macro mean, but
> the strict robustness claim is assigned to proposal voting.

### Avoid 4. Dropout prediction voting as a main robustness result

Evidence against:

- It was selected after probing the only failed dropout cell.
- It repairs TruckScenes 30% by only +0.0010 AP over RDAR.
- It worsens q55 in 8/12 cells.

Allowed alternative:

> We explored dropout prediction voting and found that it can repair the only
> negative RDAR cell, but because it was post-hoc and reduced q55 in most
> cells, we did not use it for the main robustness claim.

### Avoid 5. Real-time strict route claim

Evidence against:

- Voting overhead is about 22 ms/frame in the current implementation.

Allowed alternative:

> The current strict-voting implementation trades additional post-processing
> time for cross-seed robustness; optimizing this stage is left as an
> engineering improvement.

## Reviewer attack points and prepared responses

| Reviewer concern | Evidence-based response |
|---|---|
| "The improvement is small." | The strict route's average gain is moderate, but the key claim is consistency: 12/12 paired seed-dataset gains, min Delta AP +0.1718. The high-performance route is separately reported for larger macro gains. |
| "The best macro method has a regression." | Correct; q55 is not used for the strict no-regression claim. It is labelled as a high-performance variant. |
| "The ablation is only one seed." | Correct; the five-row ablation is labelled as seed2028 progressive evidence. Formal robustness is supported by separate 3-seed strict-route comparisons. |
| "Runtime overhead is nontrivial." | Correct; the paper reports fixed detector latency and voting overhead separately and does not claim free runtime. |
| "Range/sparsity claims are not supported." | The manuscript should not make those claims. Those diagnostics are retained as failure-boundary analysis. |
| "Dropout robustness is cherry-picked." | The main q55 dropout result reports all 12 cells and explicitly notes the one negative TruckScenes 30% cell. The post-hoc voting probe is internal/supplement only. |

## Required wording discipline checklist

Before submission, scan the manuscript for these terms:

| Term / phrase | Action |
|---|---|
| "always", "universally", "under all conditions" | Remove unless referring specifically to 12/12 tested paired comparisons |
| "no overhead", "free", "real-time" | Remove; replace with measured runtime wording |
| "strict q55" | Replace with "high-performance route" |
| "range robustness" | Remove or convert to boundary/failure analysis |
| "sparsity robustness" | Remove or restrict to point-dropout macro evidence |
| "significant improvement" | Use only if paired-test context is stated; otherwise use "improved" with effect size |
| "full ablation across seeds" | Remove unless a 3-seed ablation is later run |

## Final recommended abstract-level claim

Safe abstract claim:

> Across four radar datasets and three random seeds, the strict proposal-voting
> variant improved RDAR in all 12 paired comparisons, while a separate
> high-performance variant achieved the largest macro AP. Additional diagnostics
> showed improved calibration for the high-performance route and identified
> runtime and sparsity-bin boundaries.

Unsafe abstract claim:

> The proposed method universally improves sparse radar detection with no
> added cost.

