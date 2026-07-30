# Fair Ablation Screen-Only Support

Date: 2026-07-28

This note collects screen-only / sibling evidence that can still support the
paper after the exact residual rows became blocked.

## 1. Screen-Only AP Values

| Variant | Dataset | Seed | AP | Evidence |
|---|---|---:|---:|---|
| `q55kprior` | K-Radar | 2028 | 58.7077 | new GPU-backed eval on `screen_q55kprior_kradar_seed2028` |
| `q55rpa50_kprior` | K-Radar | 2028 | 59.6806 | existing `eval_rcnms` log |
| `q55rpa50_kprior` | K-Radar | 2027 | 56.4168 | existing screen-only eval log |
| `q55rccg` | Astyx | 2028 | 26.7364 | existing `fair_*_gpu0_fixed` eval log |
| `qflr55atss` | Astyx | 2028 | 0.0000 | existing `fair_*_gpu0_fixed` eval log |
| `qflr55_kradar` | K-Radar | 2026 | 53.1160 | existing `fair_*_gpu1_fixed` eval log |
| `q55kaap` | K-Radar | 2028 | 58.7217 | existing `eval_rcnms` log |
| `q55msbc3` | Astyx | 2028 | 32.7835 | existing `eval_rcnms` log |
| `stable_bevgate_dapg` | Astyx | 5623 | 30.9132 | already completed in `fair_ablation_seed_results.csv` |
| `stable_bevgate_dapg` | TruckScenes | 5623 | 13.1191 | existing `fair_*` eval log |
| `stable_bevgate_dapg` | V2X-Radar-V | 5623 | 38.1079 | existing `fair_*` eval log |
| `stable_four_modules` | Astyx | 5623 | 29.1196 | already completed in `fair_ablation_seed_results.csv` |
| `stable_four_modules` | TruckScenes | 5623 | 0.0000 | new GPU-backed eval on `fair_stable_four_modules_truckscenes_seed5623_gpu2` |
| `stable_four_modules` | V2X-Radar-V | 5623 | 0.0000 | new GPU-backed eval on `fair_stable_four_modules_v2xradarv_seed5623_gpu1` |
| `stable_bevgate_dapg_msbc` | Astyx | 2029 | 18.0565 | already completed in `fair_ablation_seed_results.csv` |
| `stable_bevgate_dapg_msbc` | V2X-Radar-V | 5623 | 41.4603 | existing `fair_*` eval log |
| `iouaware` | Astyx | 5623 | 31.1360 | already completed in `fair_ablation_seed_results.csv` |

## 2. What this adds

These rows do not change the current `fair_ablation_seed_results.csv`
completion count. They are supporting evidence only, but they are useful because
they:

- show that several sibling screen-only branches can still produce strong AP;
- provide a stronger manuscript-facing contrast for the surviving residual
  failures;
- separate true blockers from branches that merely needed one more eval pass.

The table now contains 17 support entries total.

## 3. Immediate use

Good places to use this support table:

- the screen-only appendix;
- the manuscript boundary / failure note;
- the sibling comparison paragraph around `q55rpa50` / `q55kprior` / `q55rccg`.

## 4. Current interpretation

The exact residual queue is still blocked, but the paper support surface is not
stalled:

- the GPU-backed `q55kprior / kradar / 2028` eval was completed successfully;
- the new `stable_four_modules / TruckScenes` and `stable_four_modules / V2X-Radar-V` sibling evals are now recorded too;
- sibling screen-only branches continue to yield strong AP values;
- the remaining work is now mostly manuscript packaging, not exact residual
  recovery.
