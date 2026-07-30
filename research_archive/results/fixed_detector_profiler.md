# Fixed detector profiler

Hardware: NVIDIA GeForce RTX 3090

Protocol: batch_size=4, workers=2, warmup_batches=3, max_measure_batches=20. Measures model forward including OpenPCDet post_processing; excludes AP evaluation and result serialization.

| Method | Dataset | Ckpt seed | Frames | ms/frame | Status |
|---|---|---:|---:|---:|---|
| rdar_taac | astyx | 2028 | 80 | 4.740 ± 0.297 | ok |
| rdar_taac | truckscenes | 2028 | 68 | 3.851 ± 0.311 | ok |
| rdar_taac | v2xradarv | 2028 | 68 | 4.834 ± 1.092 | ok |
| rdar_taac | kradar | 2028 | 68 | 5.887 ± 2.409 | ok |
| q55rpa50_kprior | astyx | 2027 | 80 | 8.263 ± 1.163 | ok |
| q55rpa50_kprior | truckscenes | 2027 | 68 | 7.880 ± 1.257 | ok |
| q55rpa50_kprior | v2xradarv | 2027 | 68 | 8.124 ± 1.334 | ok |
| q55rpa50_kprior | kradar | 2028 | 68 | 8.601 ± 1.471 | ok |