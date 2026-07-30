# Gate/vote component-attribution diagnostic

This diagnostic uses the stable BEV-gated expert checkpoint at epoch 160 and
seed 2027. It compares the same primary RDAR stream after the expert gate and
after the gate followed by the restricted `xy`/heading vote.

| Dataset | RDAR | Gate only | Gate + vote | Vote increment |
|---|---:|---:|---:|---:|
| Astyx | 31.4220 | 32.6512 | 32.4638 | -0.1874 |
| TruckScenes | 18.3845 | 19.4072 | 19.1881 | -0.2191 |
| V2X-Radar-V | 42.9899 | 44.0130 | 43.2741 | -0.7389 |
| K-Radar | 48.1767 | 49.3558 | 49.0496 | -0.3062 |

This is a component-attribution diagnostic, not the formal 12-cell result and
not a complete four-cell factorial table. Generic ungated box-voting controls
are reported separately in the manuscript.
