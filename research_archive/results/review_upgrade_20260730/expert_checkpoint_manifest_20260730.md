# Fixed-expert checkpoint manifest

This manifest records the expert checkpoints used by the fixed-expert
cross-seed diagnostic. The choice was fixed by checkpoint availability before
the factorial AP values were read; no checkpoint was selected by optimizing the
diagnostic results. All checkpoints are epoch 160.

| Conversion | Expert seed | Checkpoint filename | SHA256 |
|---|---:|---|---|
| Astyx | 2027 | `checkpoint_epoch_160.pth` under `pointpillars_bevgate_dapg_msbc_astyx_car/fair_bevgate_dapg_msbc_astyx_seed2027/ckpt/` | `99a4a890bda04bf695d3d865568655155f1c8c86da7fe071c0bad6802af8c4f2` |
| TruckScenes | 2027 | `checkpoint_epoch_160.pth` under `pointpillars_bevgate_dapg_msbc_truckscenes_car/fair_bevgate_dapg_msbc_truckscenes_seed2027/ckpt/` | `4795889a050f0d145a4bcc3c6e6014781a50e3cbb5e162da2977a7e2bea48d2e` |
| V2X-Radar-V | 2027 | `checkpoint_epoch_160.pth` under `pointpillars_bevgate_dapg_msbc_v2xradarv_car/fair_bevgate_dapg_msbc_v2xradarv_seed2027/ckpt/` | `f566573f17d42f5fbb3518725bf23267e8b4d92799bb3b88e20974e29ac1c829` |
| K-Radar | 2028 | `checkpoint_epoch_160.pth` under `pointpillars_bevgate_dapg_msbc_kradar_car/fair_bevgate_dapg_msbc_kradar_seed2028_retry/ckpt/` | `c83cd4f999181534cdc814579f9a1427571e8e614dcbdc3fa6beb12e936197b7` |

The corresponding prediction-file paths and factorial logs are included in
`strict_fixed_expert_factorial_12cell/`. The full model checkpoints remain on
the instance because of archive-size constraints; this manifest provides the
filename, epoch, provenance path, and integrity hash needed to audit the
frozen run.
