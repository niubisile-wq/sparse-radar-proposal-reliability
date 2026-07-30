# Gate/vote four-cell component-attribution diagnostic

This diagnostic uses the same primary prediction lane within each row and
compares neither operation, the expert gate only, the restricted vote only,
and gate followed by vote. Expert checkpoints are epoch 160; Astyx,
TruckScenes, and V2X-Radar-V use seed 2027, while K-Radar uses the available
seed-2028 expert checkpoint.

| Dataset | Neither | Gate only | Vote only | Gate + vote |
|---|---:|---:|---:|---:|
| Astyx | 31.4220 | 31.9674 | 31.7927 | 32.9596 |
| TruckScenes | 18.3845 | 21.1631 | 18.0119 | 20.6590 |
| V2X-Radar-V | 42.9899 | 44.6020 | 42.1110 | 45.0582 |
| K-Radar | 52.0271 | 54.2513 | 51.8515 | 54.1391 |

This is a component-attribution diagnostic, not the formal 12-cell result.
Generic three-seed post-processing controls remain reported separately.
