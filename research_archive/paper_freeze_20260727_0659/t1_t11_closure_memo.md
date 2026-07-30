# T1/T11 Closure Memo

Date: 2026-07-27

This memo records the closest-to-closure evidence in the current matrix. It is
not a claim that the full matrix is complete.

## T1 Main comparison

Current evidence:

- [results/main_comparison_13x4_ap_report.md](C:/Users/刘子轩/radar_experiment_configs/results/main_comparison_13x4_ap_report.md)
- [results/13x4_ap_evidence.json](C:/Users/刘子轩/radar_experiment_configs/results/13x4_ap_evidence.json)
- [results/13x4_ap_results.csv](C:/Users/刘子轩/radar_experiment_configs/results/13x4_ap_results.csv)

What this supports:

- A frozen four-dataset AP_R40 comparison table exists.
- The table is backed by a method-to-log evidence package, not a synthetic
  summary.
- The table covers the four core datasets required by the matrix.

What it does not yet establish by itself:

- It does not prove every baseline is a final manuscript winner.
- It does not replace the need to cite the relevant source logs in the paper.

## T11 Efficiency

Current evidence:

- [results/efficiency_report.md](C:/Users/刘子轩/radar_experiment_configs/results/efficiency_report.md)
- [results/detector_latency_from_logs.md](C:/Users/刘子轩/radar_experiment_configs/results/detector_latency_from_logs.md)

What this supports:

- The strict voting module has 0 additional trainable parameters.
- The strict-route and high-performance routes have measured latency summaries
  on RTX 3090.
- The reports separate parameter count, voting overhead, and detector latency.

What it does not yet establish by itself:

- It does not establish a fully profiled end-to-end real-time claim.
- It does not replace a dedicated profiler run if the manuscript needs one
  fixed batch-size latency number.

## Practical reading

- T1 is now usable as a frozen comparison evidence package.
- T11 is usable as an efficiency evidence package with clear claim boundaries.
- Both remain `screening` in the matrix until the manuscript-facing claim
  language is finalized.

