# Evidence upgrade audit — 2026-07-30

## Completed in this round

- Confirmed the remote instance has two NVIDIA GeForce RTX 4080 SUPER GPUs with approximately 32 GB memory each.
- Reconstructed the leave-one-dataset-out threshold audit from the frozen quality-alignment grid and per-seed logs.
- Ran the missing standard box-voting sweeps for TruckScenes and V2X-Radar-V, seed 2028, with 20 parameter points per dataset.

## Held-out threshold audit

The threshold was selected from the other three datasets using the frozen grid, and the candidate was compared with RDAR (M1+M2).

- Astyx: mean delta `+0.9871 AP`; all 3 seeds positive.
- TruckScenes: mean delta `+0.9157 AP`; all 3 seeds positive.
- V2X-Radar-V: mean delta `+0.2392 AP`; 2/3 seeds positive, one seed `-0.2945 AP`.
- K-Radar: mean delta `+1.5059 AP`; all 3 seeds positive.
- Overall: 11/12 held-out seed differences are positive and all four dataset-level means are positive.

This supports a cross-dataset held-out mean-gain claim, but does not support a new 12/12 held-out seed claim.

### Strict training-positive selection rule

A stronger audit was also generated using the following frozen rule: among grid settings whose nine training dataset-seed deltas are all positive, select the setting with the largest training mean delta, then evaluate once on the held-out dataset.

- Astyx: selected `0.22/0.40`; held-out mean `+0.5026 AP`; 3/3 seeds positive.
- TruckScenes: selected `0.22/0.40`; held-out mean `+0.5264 AP`; 3/3 seeds positive.
- V2X-Radar-V: selected `0.24/0.35`; held-out mean `+0.2392 AP`; 2/3 seeds positive.
- K-Radar: selected `0.22/0.40`; held-out mean `+1.6836 AP`; 3/3 seeds positive.

This gives 4/4 positive held-out dataset means and 11/12 positive held-out seed cells under an explicit training-only selection rule.

## Standard box-voting baseline

- TruckScenes, seed 2028: best AP `16.9217`, RDAR `15.3041`, delta `+1.6176 AP`.
- V2X-Radar-V, seed 2028: best AP `42.1186`, RDAR `41.3385`, delta `+0.7801 AP`.

The manuscript must report this baseline explicitly and distinguish it from the quality-aligned strict route.

The four-dataset core sweep is now complete (20 points per dataset, using the available seed-specific RDAR outputs):

- Astyx, seed 2026: best `+1.1061 AP`.
- TruckScenes, seed 2028: best `+1.6176 AP`.
- V2X-Radar-V, seed 2028: best `+0.7801 AP`.
- K-Radar, seed 2028: best `+0.0537 AP`.

The gains are heterogeneous; this is useful evidence that the proposed quality-aligned route cannot be equated with ordinary box voting.

### Fixed-parameter three-seed follow-up

The best control parameters from the initial sweeps were then frozen and evaluated across all three seeds:

- Astyx: mean `+0.4723 AP`, all 3 seeds positive.
- TruckScenes: mean `-0.0831 AP`, not all positive.
- V2X-Radar-V: mean `+0.5342 AP`, all 3 seeds positive.
- K-Radar: mean `+0.0097 AP`, not all positive.

This is a useful negative control: ordinary box voting improves some datasets but does not reproduce the cross-dataset robustness pattern of the quality-aligned route.

## Protocol issue intercepted

The first newly launched LODO jobs for seeds 2026/2027 used `m3_stable_stage` inputs, whereas the frozen sensitivity grid uses the quality-alignment/frozen input branch. Those outputs were not used in the LODO report and remain only as audit artifacts. This confirms that future runs need an explicit input-branch identifier in every manifest row.

## Source artifacts

- `lodo_holdout_report_20260730.md`
- `lodo_holdout_seed_results_20260730.csv`
- `standard_box_voting_seed2028.md`
- `standard_box_voting_seed2028.csv`

## Soft-NMS baseline

Gaussian Soft-NMS was implemented on the same frozen RDAR prediction sets. A seed-2028 sigma screen used `{0.1, 0.5, 1.0}`; sigma `0.5` was then fixed globally for the three-seed comparison.

- Astyx: mean `-0.1831 AP`.
- TruckScenes: mean `+0.0909 AP`.
- V2X-Radar-V: mean `-0.2098 AP`.
- K-Radar: mean `+0.0196 AP`.

No dataset had all three seeds positive. This provides a direct standard Soft-NMS control and strengthens the argument that the observed robustness is not explained by generic score decay alone.

## WBF baseline

Weighted Box Fusion was implemented as a separate GPU baseline. The seed-2028 screen selected a common IoU threshold of `0.5`, which was then fixed globally for the three-seed comparison.

- Astyx: mean `-0.0118 AP`.
- TruckScenes: mean `-0.1305 AP`.
- V2X-Radar-V: mean `-0.2474 AP`.
- K-Radar: mean `-0.1896 AP`.

No dataset had all three seeds positive. Together with the box-voting and Soft-NMS controls, this provides direct evidence against the explanation that the strict-route gains are ordinary generic box post-processing.
