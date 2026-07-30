# M3/M4 experiment ledger

Last updated: 2026-07-27 02:38 CST

## Sequential reference

All candidate results are evaluated with RC-NMS and the existing RDAR recovery
stage. Incremental gains are computed against RDAR with the same random seed.

| Dataset | RDAR seed 2026 | RDAR seed 2027 | RDAR seed 2028 |
|---|---:|---:|---:|
| Astyx | 32.7281 | 31.4220 | 34.3540 |
| MAN TruckScenes | 15.4127 | 18.3845 | 15.3041 |
| V2X-Radar-V | 40.7802 | 42.9899 | 41.3385 |
| K-Radar | 51.3450 | 48.1767 | 52.0271 |

## Acceptance gate

A module is accepted only if:

1. all four datasets improve for every seed;
2. mean incremental gain is at least 1.0 AP on every dataset;
3. the paired 95% confidence-interval lower bound is above zero on every
   dataset;
4. training/evaluation settings remain identical except for the claimed
   module.

With three seeds, the paired confidence interval uses Student's
`t(0.975, df=2) = 4.303`.

## M3: Residual quality-aligned classification

### Principle

Binary classification targets do not distinguish a barely matched positive
anchor from a well-localized positive anchor. M3 uses a continuous target
combining objectness and matched 3D IoU:

`q = 0.55 + 0.45 * IoU3D`

and optimizes it with a quality-focal form. The 0.55 residual preserves
objectness evidence for noisy/sparse radar boxes; the IoU term aligns ranking
with localization quality.

### Seed-2028 screen

| Variant | Astyx | TruckScenes | V2X-Radar-V | Decision |
|---|---:|---:|---:|---|
| residual 0.50 | +2.3490 | +1.8317 | +0.3000 | reject |
| residual 0.55 | **+2.6778** | **+2.1489** | **+1.2594** | formal reject |
| residual 0.575 | +0.8186 | +0.0199 | pending | reject |
| residual 0.60 | +1.3067 | +0.0101 | +2.3744 | reject |
| residual 0.75 | +2.2594 | -1.6585 | +2.8519 | reject |

Formal residual-0.55 results:

| Dataset | Seed 2026 | Seed 2027 | Seed 2028 | Mean | 95% CI lower | Decision |
|---|---:|---:|---:|---:|---:|---|
| Astyx | +2.8083 | +3.5412 | +2.6778 | +3.0091 | +1.8529 | pass |
| TruckScenes | +0.1030 | -0.4550 | +2.1489 | +0.5990 | -2.8070 | reject |
| V2X-Radar-V | +2.5932 | +4.2754 | +1.2594 | +2.7093 | -1.0454 | reject |
| K-Radar | pending | pending | +7.4416 | pending | pending | stopped after rejection |

Residual 0.55 is therefore **not M3**.

Residual 0.50 formal results also reject it:

| Dataset | Seed 2026 | Seed 2027 | Seed 2028 | Mean / proof | Decision |
|---|---:|---:|---:|---:|---|
| Astyx | +1.6428 | +4.2096 | +2.3490 | mean +2.7338, CI lower -0.5603 | reject |
| TruckScenes | +1.5674 | -1.7649 | +1.8317 | mean +0.5447, CI lower -4.4353 | reject |
| V2X-Radar-V | stopped | +2.5782 | +0.3000 | best possible CI lower over any third value: -1.3133 | reject |

The unfinished V2X seed-2026 job was stopped once mathematical impossibility
of passing the CI gate was established.

Residual 0.525 also fails the seed-2028 screen:

| Dataset | Increment over RDAR | Decision |
|---|---:|---|
| Astyx | +0.4905 | below +1 AP |
| TruckScenes | -2.1217 | regression |
| V2X-Radar-V | +3.4010 | pass on this dataset only |

This confirms that interpolation between 0.50 and 0.55 does not resolve the
cross-dataset conflict.

## M3 follow-up candidate: DTQC

DTQC separates the conflicting targets into two learned branches:

1. a residual-IoU quality branch for localization-aware ranking;
2. an unchanged binary-focal objectness branch for stable target evidence;
3. geometric probability consensus at inference.

This tests whether the TruckScenes/V2X instability is caused by forcing
objectness and localization quality into one logit. Registration/config smoke
tests pass.

DTQC is rejected. Seed-2028 results at the default global fusion
coefficient:

| Dataset | Increment over RDAR |
|---|---:|
| Astyx | -1.9050 |
| V2X-Radar-V | +2.2703 |

An inference-only sweep cannot rescue Astyx:

| Quality fusion alpha | 0.25 | 0.35 | 0.50 | 0.65 | 0.75 | 0.85 | 0.90 | 1.00 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Astyx delta | -1.9666 | -1.9323 | -1.9050 | -1.9033 | -1.8857 | -1.8191 | -1.8114 | -1.5170 |

Because every coefficient regresses Astyx, no global coefficient can pass
all datasets. Remaining DTQC-only formal jobs were stopped.

## M3 follow-up candidate: quality-aware ATSS

The next candidate couples residual-IoU classification with ATSS positive
assignment. Fixed anchor thresholds create different positive populations
under varying radar sparsity and box geometry; ATSS instead derives each
target's positive threshold from the mean and standard deviation of nearby
candidate IoUs. The same global `TOPK=9` is used on all datasets.

Seed-2028 screens run as `qflr55atss`; a DTQC+ATSS interaction screen runs in
parallel to determine whether independent objectness helps only after
adaptive assignment.

### Result

`qflr55atss` is rejected by the first completed strict screen:

| Dataset | RDAR reference | Candidate AP | Increment |
|---|---:|---:|---:|
| Astyx, seed 2028 | 34.3540 | 0.2418 | -34.1122 |

The checkpoint's default-threshold AP was 0.0000; RC-NMS recovered proposal
recall but not precision/ranking. The remaining Astyx/TruckScenes/V2X/K-Radar
jobs were terminated immediately. This agrees with the pure-ATSS control and
shows that hard adaptive replacement of the original positive assignment is
not suitable for these sparse radar splits.

The independent-objectness `dtqcatss` Astyx screen also fails:

| Dataset | RDAR reference | Candidate AP | Increment |
|---|---:|---:|---:|
| Astyx, seed 2028 | 34.3540 | 0.2428 | -34.1112 |

All remaining `dtqcatss` jobs were terminated. Hard ATSS assignment is now
closed as a rejected direction.

## M3 physics candidate: PVD

All four datasets expose calibrated radial velocity but the champion treats it
as an ordinary scalar. PVD retains the raw value and appends its line-of-sight
Cartesian components:

`vx_r = vr cos(atan2(y,x)), vy_r = vr sin(atan2(y,x))`.

This is a clean, one-change transfer screen based on RadarPillars; it does not
change anchors, augmentation, loss, assignment, optimizer, or post-processing.
Four seed-2028 screens are running on GPUs 1/2/3. If the physical bias transfers,
the final module will add a reliability gate so it is technically distinct
from fixed Doppler decomposition.

The final Doppler Reliability-Adaptive Vectorization (DRAV) implementation is
ready. Its bounded gate uses range, RCS, absolute radial speed, pillar return
count, and within-pillar Doppler dispersion. The gate is initialized exactly
to the PVD identity:

- PVD vs. initial DRAV maximum output difference: 0.0;
- output and gate gradients: finite;
- gate gradient norm on the smoke batch: 0.0031656.

## M4 context candidate: RGPC

Reliability-Gated Geometry-Aware Pillar Context has been implemented and its
CPU forward/backward smoke test passes:

- queries/keys receive normalized BEV coordinates and log pillar return count;
- values retain the original pillar features;
- a channel-wise gate initialized to 0.1 mixes context into an identity path;
- output shape and gradients are finite.

RGPC will be screened incrementally on top of PVD if PVD passes; if PVD fails,
an isolated champion+RGPC control will determine whether the context mechanism
is independently viable.

## 2026-07-26 instance restart and recovered factorial

At approximately 05:50 CST the instance restarted: SSH port 33613 temporarily
closed, all four GPU contexts disappeared, and the active PVD/RGPC jobs stopped.
Because screening checkpoints were intentionally scheduled only at epoch 160,
the interrupted 30%--74% partial runs were not recoverable.

After the endpoint recovered, the stale GPU-3 context was gone. The screening
was relaunched as a 3-way, four-dataset seed-2028 factorial:

1. `pvd`: fixed physical Doppler decomposition diagnostic;
2. `drav`: reliability-adaptive Doppler vectorization, the M3 candidate;
3. `pvd_rgpc`: PVD plus reliability-gated geometry-aware context, used to
   measure RGPC's clean incremental effect.

Twelve training jobs now run concurrently (three per GPU). Observed utilization
after warm-up was 99%, 99%, 99%, and 100%, with no OOM or traceback.

Automated evidence controls are installed:

- `evaluate_variant_gate.py` verifies completed logs and supports paired
  candidate-vs-candidate gates;
- its passing-formal, failing-screen, and incremental-reference tests pass;
- `watch_physics_context_factorial.sh` will launch DRAV formal seeds only if
  all four seed-2028 gains exceed +1 AP;
- it launches `drav_rgpc` only if both DRAV and the clean
  `pvd_rgpc - pvd` increment pass;
- `build_final_ablation_report.py` produces the sequential M1--M4 table,
  paired deltas/CIs, factorial controls, and context interaction controls.

## 2026-07-27 drav screen relaunch

The physics-context factorial was relaunched after the watcher retired:

- `launch_variant_screen.sh drav` is now running again for seed 2028.
- Active drav screen processes were observed for Astyx, TruckScenes,
  V2X-Radar-V, and K-Radar.
- A duplicate hand-started TruckScenes process was terminated so the relaunched
  full screen owns the GPU schedule.

This keeps the remaining sequential/mechanism ablation work aligned with the
current plan state rather than the retired watcher state.

Latest poll:

- `screen_drav_kradar_seed2028_gpu2.log` has closed with `Evaluation done`
  and `Epoch 160 has been evaluated`.
- `screen_drav_truckscenes_seed2028_gpu0.log` has also closed with the same
  evaluation markers.
- `screen_drav_astyx_seed2028_gpu0.log`,
  `screen_drav_truckscenes_seed2028_gpu1.log`, and
  `screen_drav_v2xradarv_seed2028_gpu2.log` are still in the wait-loop state.
- `screen_drav_kradar_seed2028_gpu3.log` is a stale GPU-mismatch failure and
  should not be treated as an active closure path.

## 2026-07-27 pvd_rgpc K-Radar launch

The `pvd_rgpc` K-Radar lane has now completed on GPU 0 after the manual
launch and full eval pass.

- `pointpillars_pvd_rgpc_kradar_car` ran with seed 2028 and finished.
- The corresponding `queue_variant_eval_lane.sh` watcher is attached.
- The previous wait-for-free-GPU autostart state is stale and should no longer
  be treated as the active status.
- Current eval output reports `Car radar AP_R40@3D IoU 0.50: 53.5853`.
- The final screen log shows `Evaluation done` and `Epoch 160 has been evaluated`.
- A separate GPU-3 log from an earlier attempt hit a CUDA illegal memory
  access; that older attempt is not the active run and should be ignored in the
  closure chain.

## 2026-07-28 drav_rgpc screen launch

The `drav_rgpc` four-dataset seed-2028 screen has now been launched from the
generic variant launcher.

- `launch_variant_screen.sh drav_rgpc` was invoked successfully.
- Active training processes are now visible for Astyx, TruckScenes, and
  V2X-Radar-V on GPUs 0, 1, and 2.
- The K-Radar lane on GPU 3 immediately failed with
  `RuntimeError: No CUDA GPUs are available`; that GPU-3 failure is the stale
  lane and should be excluded from the active screen chain.
- The active screen logs show the first training epochs advancing on the three
  healthy GPUs, so the missing `drav_rgpc` lane is no longer just a paper gap.
- Latest remote poll shows the three healthy lanes still advancing:
  - Astyx is around epoch 158/160.
  - TruckScenes is around epoch 155/160.
  - V2X-Radar-V is around epoch 148/160.
  - The stale GPU-3 K-Radar lane remains failed and unchanged.
- A later remote poll confirmed the Astyx `drav_rgpc` screen has now closed:
  - `Evaluation done` is present in `screen_drav_rgpc_astyx_seed2028_gpu0.log`.
  - `Epoch 160 has been evaluated`.
  - The final eval artifact was saved under the Astyx `eval_with_train/epoch_160/val` directory.
- Another remote poll confirmed the TruckScenes `drav_rgpc` screen has now closed:
  - `Evaluation done` is present in `screen_drav_rgpc_truckscenes_seed2028_gpu1.log`.
  - `Epoch 160 has been evaluated`.
  - The final eval artifact was saved under the TruckScenes `eval_with_train/epoch_160/val` directory.
- Latest remote poll confirmed the V2X-Radar-V `drav_rgpc` screen has now
  closed:
  - `Evaluation done` is present in `screen_drav_rgpc_v2xradarv_seed2028_gpu2.log`.
  - `Epoch 160 has been evaluated`.
  - The final eval artifact was saved under the V2X-Radar-V
    `eval_with_train/epoch_160/val` directory.

## 2026-07-28 K-Radar GPU-3 lane remap

The stale K-Radar GPU-3 branches were remapped onto live GPUs.

- `relaunch_kradar_off_gpu3.sh` was executed successfully.
- `drav` K-Radar is now running on GPU 0 with `screen_drav_kradar_seed2028_gpu0.log`.
- `pvd_rgpc` K-Radar is now running on GPU 1 with `screen_pvd_rgpc_kradar_seed2028_gpu1.log`.
- Both logs have entered the standard `Start evaluation` / `Wait 30 seconds for
  next check` loop, which means the lanes are alive and waiting on the frozen
  checkpoint rather than failing on the stale GPU-3 context.
- Latest remote poll still shows both lanes in the evaluation wait loop with no
  `Evaluation done` marker yet; the most recent wait loop progress reached
  56.5 / 0 minutes for both lanes.

## M4 candidate: SCPE

### Principle

The four datasets expose the same nominal `[x,y,z,RCS,vr]` format but have
incompatible RCS and velocity scales. SCPE:

1. standardizes RCS and radial velocity inside each frame;
2. independently encodes
   `[z_rcs, z_vr, |z_vr|, z_rcs*|z_vr|]`;
3. max/mean pools the physical evidence in each pillar;
4. adds it to the unchanged geometry PillarVFE through a bounded,
   zero-initialized residual gate.

The zero initialization makes the initial model function exactly equal to the
M3 detector; improvements must be learned from calibrated physical evidence.

### Result

- CPU forward/backward smoke test: passed.
- Direct single-level configuration inheritance: fixed and verified.
- Astyx seed-2028 AP after RC-NMS + RDAR: 34.8111.
- Residual-0.55 M3 reference: 37.0318.
- Incremental change: **-2.2207 AP**.
- SCPE is rejected and was not expanded to the other datasets. Frame
  standardization likely removed useful absolute RCS evidence.

## Required paper-strengthening experiments after acceptance

- Full sequential ablation: baseline, +M1, +M2, +M3, +M4.
- Standalone and interaction ablation for each trainable module.
- Three-seed paired confidence intervals and effect sizes.
- AP/recall by range, point count, RCS and absolute radial velocity.
- Parameter count, FLOPs, latency, peak memory and training cost.
- Robustness to radar point dropout, RCS perturbation and velocity noise.
- Threshold sensitivity for RC-NMS/RDAR and residual-quality coefficient.
- Qualitative true-positive recovery, false-positive suppression and failure
  cases.
