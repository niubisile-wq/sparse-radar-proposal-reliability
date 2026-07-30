# Diagnostic gate summary

Compares each variant against RDAR across 3 seeds x 4 datasets.

Positive means better than RDAR. For ECE, positive means lower ECE than RDAR.

| Variant | Metric | Win | Tie | Loss | Missing | Mean delta | Gate decision |
|---|---|---:|---:|---:|---:|---:|---|
| m3rob_q15p25_viou0p24_s0p40 | overall_recall | 11 | 0 | 1 | 0 | 0.0045 | internal only |
| m3rob_q15p25_viou0p24_s0p40 | range_bins | 26 | 13 | 9 | 0 | 0.0038 | internal only |
| m3rob_q15p25_viou0p24_s0p40 | sparsity_bins | 18 | 19 | 8 | 3 | 0.0084 | internal only |
| m3rob_q15p25_viou0p24_s0p40 | ece_hit | 0 | 0 | 12 | 0 | -0.0270 | selective/internal |
| m3rob_q15p25_viou0p24_s0p40 | top10_iou | 9 | 0 | 3 | 0 | 0.0124 | selective/internal |
| m3rob_q15p25_viou0p24_s0p40 | score_iou_corr | 7 | 0 | 5 | 0 | 0.0102 | selective/internal |
| q55rpa50_kprior | overall_recall | 4 | 0 | 8 | 0 | -0.0010 | internal only |
| q55rpa50_kprior | range_bins | 17 | 10 | 21 | 0 | -0.0031 | internal only |
| q55rpa50_kprior | sparsity_bins | 19 | 9 | 17 | 3 | 0.0106 | internal only |
| q55rpa50_kprior | ece_hit | 12 | 0 | 0 | 0 | 0.0504 | keep |
| q55rpa50_kprior | top10_iou | 6 | 0 | 6 | 0 | 0.0052 | selective/internal |
| q55rpa50_kprior | score_iou_corr | 8 | 0 | 4 | 0 | 0.0155 | selective/internal |

## Practical decision

- Do not use range-wise or sparsity-wise recall as a global positive claim:
  both strict and high-performance variants have losses in bins.
- Keep ECE/calibration for `q55rpa50_kprior`: it is consistently better than
  RDAR in the available diagnostics.
- For the strict robust route, use formal AP 12/12 positivity as the main
  robustness evidence, not the diagnostic recall bins.
