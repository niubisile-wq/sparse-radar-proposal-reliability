# Fair ablation report

- Seeds discovered: 2026, 2027, 2028, 2029, 2034, 2035, 2036, 2037, 3407, 4519, 5623, 6001
- Practical-gain threshold: 1.0 AP
- Statistical gate: paired 95% CI lower bound > 0

## AP summary

| Module | Astyx | TruckScenes | V2X-Radar-V | K-Radar | Macro mean |
|---|---:|---:|---:|---:|---:|
| pointpillars | 28.5987 ± 1.6869 (n=3) | 15.7163 ± 1.7772 (n=3) | 40.1987 ± 0.9695 (n=3) | 48.9068 ± 1.6606 (n=3) | 33.3551 |
| bevgate | 26.9583 ± 0.5484 (n=3) | 14.8548 ± 3.4672 (n=3) | 42.3446 ± 1.2145 (n=3) | 51.3838 ± 2.2243 (n=2) | 33.8854 |
| stable_bevgate | 27.5859 ± 0.8082 (n=5) | 14.3281 ± 1.4939 (n=6) | 41.2906 ± 1.6521 (n=5) | 50.0312 ± 2.1817 (n=4) | 33.3089 |
| rccg | 27.1980 ± 0.0000 (n=1) | 14.2030 ± 0.0000 (n=1) | 38.2742 ± 0.0000 (n=1) | — | — |
| dapg2 | 26.7032 ± 1.2843 (n=3) | 13.4754 ± 3.1603 (n=2) | 40.7141 ± 2.9449 (n=2) | 50.6456 ± 0.9019 (n=2) | 32.8845 |
| msbc2 | 28.4206 ± 0.0000 (n=1) | 14.0324 ± 5.4310 (n=2) | 41.2925 ± 1.7700 (n=2) | — | — |
| range2 | 26.0519 ± 0.2188 (n=2) | 17.4485 ± 3.9146 (n=2) | 37.1043 ± 5.1113 (n=2) | 50.4802 ± 0.0000 (n=1) | 32.7712 |
| dapg3 | 26.8505 ± 1.3938 (n=2) | 12.4669 ± 1.1702 (n=3) | 40.7812 ± 2.8499 (n=2) | 49.0292 ± 3.1878 (n=2) | 32.2820 |
| msbc3 | 27.7645 ± 0.9181 (n=3) | 16.1016 ± 2.5046 (n=2) | 41.4768 ± 1.4336 (n=3) | 53.9329 ± 0.0000 (n=1) | 34.8189 |
| range3 | 27.0292 ± 1.6010 (n=2) | 18.0074 ± 3.1241 (n=2) | 40.6651 ± 0.0755 (n=2) | 48.9803 ± 0.0000 (n=1) | 33.6705 |
| sbd05 | 27.6053 ± 0.0209 (n=2) | 14.4917 ± 0.0000 (n=1) | 38.1893 ± 0.0000 (n=1) | 46.2794 ± 3.8703 (n=2) | 31.6414 |
| sbd10 | 26.2870 ± 1.1976 (n=2) | 15.9806 ± 0.0000 (n=1) | 40.5302 ± 0.2883 (n=2) | 48.7488 ± 0.0000 (n=1) | 32.8867 |
| sbd20 | 26.6260 ± 0.3982 (n=2) | 11.0915 ± 0.0000 (n=1) | 38.1667 ± 1.8822 (n=2) | 45.5965 ± 0.0000 (n=1) | 30.3702 |
| swa5 | — | — | — | 46.3701 ± 0.0000 (n=1) | — |
| rcnms | 32.8152 ± 1.4692 (n=3) | 16.3498 ± 1.7514 (n=3) | 41.6866 ± 1.1545 (n=3) | 50.5059 ± 2.0589 (n=3) | 35.3394 |
| taac_rcnms | 33.1874 ± 0.2209 (n=3) | 16.3295 ± 0.5433 (n=3) | 42.8078 ± 3.3466 (n=3) | 55.1917 ± 3.1736 (n=3) | 36.8791 |
| rdar | 32.8347 ± 1.4689 (n=3) | 16.3671 ± 1.7480 (n=3) | 41.7029 ± 1.1490 (n=3) | 50.5163 ± 2.0546 (n=3) | 35.3552 |
| stable_bevgate_dapg | 25.4683 ± 0.0000 (n=1) | 15.2049 ± 2.9519 (n=2) | 40.1694 ± 0.0000 (n=1) | 51.7622 ± 1.9950 (n=2) | 33.1512 |
| stable_bevgate_dapg_msbc | 27.6501 ± 0.7019 (n=2) | 17.0262 ± 1.5036 (n=4) | 41.5751 ± 1.9508 (n=3) | 53.6578 ± 1.1699 (n=2) | 34.9773 |
| stable_four_modules | 29.1110 ± 0.0000 (n=1) | 0.0000 ± 0.0000 (n=1) | 0.0000 ± 0.0000 (n=1) | — | — |
| atss | 0.0000 ± 0.0000 (n=1) | — | — | — | — |
| atss15 | — | — | — | — | — |
| atss5 | — | — | — | — | — |
| bevgate_dapg | 27.2249 ± 1.4067 (n=3) | 15.7510 ± 1.6320 (n=3) | 41.8574 ± 2.4020 (n=3) | 51.7123 ± 1.8559 (n=3) | 34.1364 |
| bevgate_dapg_msbc | 28.0965 ± 0.1611 (n=3) | 21.1790 ± 2.7525 (n=3) | 41.4425 ± 1.1149 (n=3) | 54.4423 ± 0.0000 (n=1) | 36.2901 |
| bevgate_replay10 | 23.2143 ± 0.0000 (n=1) | 13.8910 ± 0.0000 (n=1) | 38.6544 ± 0.0000 (n=1) | — | — |
| bevgate_replay5 | 25.6215 ± 0.0000 (n=1) | 16.8717 ± 0.0000 (n=1) | 37.8685 ± 0.0000 (n=1) | 50.4758 ± 0.0000 (n=1) | 32.7094 |
| corner | 31.1560 ± 0.0000 (n=1) | — | 42.3051 ± 0.0000 (n=1) | — | — |
| corner02 | 31.1266 ± 0.0000 (n=1) | — | — | — | — |
| four_modules | 26.8552 ± 1.4847 (n=6) | 17.5568 ± 2.2065 (n=6) | 40.4580 ± 3.1135 (n=6) | 0.0000 ± 0.0000 (n=2) | 21.2175 |
| iouaware | 31.5161 ± 0.0000 (n=1) | 16.5672 ± 0.0000 (n=1) | 41.0898 ± 1.3672 (n=2) | 46.4958 ± 3.9424 (n=2) | 33.9172 |
| iouaware_radarreplay | 27.3125 ± 0.0000 (n=1) | 13.8836 ± 0.0000 (n=1) | — | — | — |
| rpa45 | — | — | — | — | — |
| rpa50 | 34.4625 ± 0.0000 (n=1) | — | — | — | — |
| rpa55 | 34.7538 ± 0.0000 (n=1) | — | — | — | — |
| swa5_nms050 | — | — | — | 48.2534 ± 0.0000 (n=1) | — |
| taac | 28.5787 ± 0.4688 (n=4) | 16.1570 ± 1.7406 (n=4) | 39.9524 ± 4.2241 (n=4) | 55.1238 ± 3.3266 (n=4) | 34.9530 |

## Sequential paired deltas

| Step | Dataset | Mean ΔAP | SD | 95% CI lower | n | All seeds > 0 | ≥1 AP | Pass |
|---|---|---:|---:|---:|---:|:---:|:---:|:---:|
| pointpillars → bevgate | astyx | -1.6404 | 1.4268 | -5.1852 | 3 | no | no | fail/pending |
| pointpillars → bevgate | truckscenes | -0.8615 | 2.6568 | -7.4619 | 3 | no | no | fail/pending |
| pointpillars → bevgate | v2xradarv | +2.1459 | 0.9288 | -0.1615 | 3 | yes | yes | fail/pending |
| pointpillars → bevgate | kradar | +2.1817 | 0.0098 | — | 2 | yes | yes | fail/pending |
| pointpillars → stable_bevgate | astyx | -0.5690 | 1.5009 | -4.2979 | 3 | no | no | fail/pending |
| pointpillars → stable_bevgate | truckscenes | -1.1186 | 3.8946 | -10.7942 | 3 | no | no | fail/pending |
| pointpillars → stable_bevgate | v2xradarv | +1.2870 | 2.8673 | -5.8363 | 3 | no | yes | fail/pending |
| pointpillars → stable_bevgate | kradar | +1.0787 | 1.2265 | -1.9683 | 3 | no | yes | fail/pending |
| pointpillars → rccg | astyx | -3.3029 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → rccg | truckscenes | -0.9261 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → rccg | v2xradarv | -1.7928 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → rccg | kradar | — | — | — | 0 | — | — | pending |
| pointpillars → dapg2 | astyx | -4.4381 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → dapg2 | truckscenes | +0.5809 | 0.0000 | — | 1 | yes | no | fail/pending |
| pointpillars → dapg2 | v2xradarv | -1.4353 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → dapg2 | kradar | +2.3854 | 0.0000 | — | 1 | yes | yes | fail/pending |
| pointpillars → msbc2 | astyx | -2.0803 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → msbc2 | truckscenes | -4.9370 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → msbc2 | v2xradarv | -0.0261 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → msbc2 | kradar | — | — | — | 0 | — | — | pending |
| pointpillars → range2 | astyx | -4.2943 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → range2 | truckscenes | -0.4487 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → range2 | v2xradarv | -6.5769 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → range2 | kradar | — | — | — | 0 | — | — | pending |
| pointpillars → dapg3 | astyx | -2.6648 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → dapg3 | truckscenes | -1.5576 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → dapg3 | v2xradarv | -1.3009 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → dapg3 | kradar | -0.8474 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → msbc3 | astyx | -3.4688 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → msbc3 | truckscenes | -0.7985 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → msbc3 | v2xradarv | -0.2197 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → msbc3 | kradar | — | — | — | 0 | — | — | pending |
| pointpillars → range3 | astyx | -2.3396 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → range3 | truckscenes | +0.6692 | 0.0000 | — | 1 | yes | no | fail/pending |
| pointpillars → range3 | v2xradarv | +0.5447 | 0.0000 | — | 1 | yes | no | fail/pending |
| pointpillars → range3 | kradar | — | — | — | 0 | — | — | pending |
| pointpillars → sbd05 | astyx | -2.9104 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → sbd05 | truckscenes | -0.6374 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → sbd05 | v2xradarv | -1.8777 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → sbd05 | kradar | -4.0797 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → sbd10 | astyx | -3.3671 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → sbd10 | truckscenes | +0.8515 | 0.0000 | — | 1 | yes | no | fail/pending |
| pointpillars → sbd10 | v2xradarv | +0.6671 | 0.0000 | — | 1 | yes | no | fail/pending |
| pointpillars → sbd10 | kradar | — | — | — | 0 | — | — | pending |
| pointpillars → sbd20 | astyx | -4.1564 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → sbd20 | truckscenes | -4.0376 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → sbd20 | v2xradarv | -3.2312 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → sbd20 | kradar | — | — | — | 0 | — | — | pending |
| pointpillars → swa5 | astyx | — | — | — | 0 | — | — | pending |
| pointpillars → swa5 | truckscenes | — | — | — | 0 | — | — | pending |
| pointpillars → swa5 | v2xradarv | — | — | — | 0 | — | — | pending |
| pointpillars → swa5 | kradar | -4.4119 | 0.0000 | — | 1 | no | no | fail/pending |
| pointpillars → rcnms | astyx | +4.2165 | 0.4324 | 3.1422 | 3 | yes | yes | pass |
| pointpillars → rcnms | truckscenes | +0.6335 | 0.4723 | -0.5399 | 3 | yes | no | fail/pending |
| pointpillars → rcnms | v2xradarv | +1.4879 | 0.2516 | 0.8629 | 3 | yes | yes | pass |
| pointpillars → rcnms | kradar | +1.5991 | 2.4488 | -4.4846 | 3 | no | yes | fail/pending |
| rcnms → taac_rcnms | astyx | +0.3723 | 1.2493 | -2.7314 | 3 | no | no | fail/pending |
| rcnms → taac_rcnms | truckscenes | -0.0202 | 2.0217 | -5.0427 | 3 | no | no | fail/pending |
| rcnms → taac_rcnms | v2xradarv | +1.1212 | 2.5917 | -5.3175 | 3 | no | yes | fail/pending |
| rcnms → taac_rcnms | kradar | +4.6858 | 4.0212 | -5.3042 | 3 | yes | yes | fail/pending |
| rcnms → rdar | astyx | +0.0195 | 0.0086 | -0.0019 | 3 | yes | no | fail/pending |
| rcnms → rdar | truckscenes | +0.0173 | 0.0073 | -0.0007 | 3 | yes | no | fail/pending |
| rcnms → rdar | v2xradarv | +0.0163 | 0.0056 | 0.0024 | 3 | yes | no | fail/pending |
| rcnms → rdar | kradar | +0.0103 | 0.0043 | -0.0004 | 3 | yes | no | fail/pending |
| stable_bevgate → stable_bevgate_dapg | astyx | -0.9163 | 0.0000 | — | 1 | no | no | fail/pending |
| stable_bevgate → stable_bevgate_dapg | truckscenes | +1.5297 | 3.6616 | — | 2 | no | yes | fail/pending |
| stable_bevgate → stable_bevgate_dapg | v2xradarv | +0.4470 | 0.0000 | — | 1 | yes | no | fail/pending |
| stable_bevgate → stable_bevgate_dapg | kradar | — | — | — | 0 | — | — | pending |
| stable_bevgate_dapg → stable_bevgate_dapg_msbc | astyx | +1.6854 | 0.0000 | — | 1 | yes | yes | fail/pending |
| stable_bevgate_dapg → stable_bevgate_dapg_msbc | truckscenes | +2.3564 | 3.7687 | — | 2 | no | yes | fail/pending |
| stable_bevgate_dapg → stable_bevgate_dapg_msbc | v2xradarv | +0.8458 | 0.0000 | — | 1 | yes | no | fail/pending |
| stable_bevgate_dapg → stable_bevgate_dapg_msbc | kradar | +2.4789 | 0.0000 | — | 1 | yes | yes | fail/pending |
| stable_bevgate_dapg_msbc → stable_four_modules | astyx | — | — | — | 0 | — | — | pending |
| stable_bevgate_dapg_msbc → stable_four_modules | truckscenes | -18.1389 | 0.0000 | — | 1 | no | no | fail/pending |
| stable_bevgate_dapg_msbc → stable_four_modules | v2xradarv | — | — | — | 0 | — | — | pending |
| stable_bevgate_dapg_msbc → stable_four_modules | kradar | — | — | — | 0 | — | — | pending |
| bevgate → bevgate_dapg | astyx | +0.2666 | 1.9229 | -4.5104 | 3 | no | no | fail/pending |
| bevgate → bevgate_dapg | truckscenes | +0.8962 | 2.7298 | -5.8855 | 3 | no | no | fail/pending |
| bevgate → bevgate_dapg | v2xradarv | -0.4873 | 1.3072 | -3.7347 | 3 | no | no | fail/pending |
| bevgate → bevgate_dapg | kradar | +1.2610 | 0.9316 | — | 2 | yes | yes | fail/pending |
| bevgate_dapg → bevgate_dapg_msbc | astyx | +0.8716 | 1.2488 | -2.2308 | 3 | no | no | fail/pending |
| bevgate_dapg → bevgate_dapg_msbc | truckscenes | +5.4280 | 1.2695 | 2.2741 | 3 | yes | yes | pass |
| bevgate_dapg → bevgate_dapg_msbc | v2xradarv | -0.4149 | 2.0030 | -5.3911 | 3 | no | no | fail/pending |
| bevgate_dapg → bevgate_dapg_msbc | kradar | +0.8834 | 0.0000 | — | 1 | yes | no | fail/pending |
| bevgate_dapg_msbc → four_modules | astyx | -0.7513 | 1.8321 | -5.3028 | 3 | no | no | fail/pending |
| bevgate_dapg_msbc → four_modules | truckscenes | -2.1077 | 4.4172 | -13.0814 | 3 | no | no | fail/pending |
| bevgate_dapg_msbc → four_modules | v2xradarv | +0.3108 | 3.0933 | -7.3739 | 3 | no | no | fail/pending |
| bevgate_dapg_msbc → four_modules | kradar | — | — | — | 0 | — | — | pending |
