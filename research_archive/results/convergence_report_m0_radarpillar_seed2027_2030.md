# Convergence Evidence Supplement

This note closes the current T13 gap with a reproducible event-file audit.

## Scope

- Run family: `champion_radarpillar_car/m0_radarpillar_seed2027` to `seed2030`
- Remote source tree: `/root/autodl-tmp/radar_champion/repos/RadarPillar/output/cfgs/astyx_models/champion_radarpillar_car/`
- Parsed files:
  - `tensorboard/events.out.tfevents*`
  - `eval/eval_with_train/tensorboard_val/events.out.tfevents*`
- Metrics extracted:
  - `train/loss`
  - `Car_3d/AP_R40_0.50`

## Method

The event files were decoded from TFRecord records using the `tensorboardX.proto.event_pb2`
message definitions available in the remote environment.

For the convergence audit, I use:

- `best AP`: the maximum `Car_3d/AP_R40_0.50` observed in the eval trace
- `time-to-target`: the first eval step reaching at least `99%` of the run's best AP

That threshold is an audit convenience, not a paper claim.

## Seed Summary

| Run | Train start | Train end | Train min | Eval points | AP start | AP end | Best AP | Best step | ttt99 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| seed2027 | 6.8928 | 0.6845 | 0.3486 | 11 | 16.3697 | 17.8204 | 17.8204 | 67 | 67 |
| seed2028 | 6.7762 | 1.0145 | 0.4446 | 11 | 14.8629 | 18.2645 | 18.5366 | 60 | 60 |
| seed2029 | 7.3693 | 1.3137 | 0.4308 | 11 | 18.1381 | 18.2909 | 18.6608 | 61 | 61 |
| seed2030 | 7.4915 | 1.0252 | 0.3882 | 11 | 18.6608 | 17.5408 | 18.6608 | 57 | 57 |

## Aggregate View

- Mean final train loss: `1.0095`
- Std. dev. final train loss: `0.2227`
- Mean final AP: `17.9792`
- Std. dev. final AP: `0.3146`
- Mean best AP: `18.4196`
- Std. dev. best AP: `0.3497`
- Final AP range: `17.5408` to `18.2909`
- Best AP range: `17.8204` to `18.6608`
- `3 / 4` seeds reach their best AP by step `61` or earlier

## Interpretation

The dense training loss traces all end near `~1.0` from initial values around `6.8` to `7.5`,
and the eval traces show a narrow late-epoch plateau in the `57-67` window rather than a
late divergence. One seed peaks at the first recorded eval step in the window, one at step 60,
one at step 61, and one at step 67.

This is sufficient to move T13 from "no direct evidence" to "screened with event-file support".
