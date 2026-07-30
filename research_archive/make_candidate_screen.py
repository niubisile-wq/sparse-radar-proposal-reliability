from pathlib import Path


ROOT = Path(__file__).resolve().parent
for source in sorted(ROOT.glob("pointpillars_bevgate_*_car.yaml")):
    if any(token in source.name for token in ("_dapg_", "_msbc_")):
        continue
    dataset = source.name[len("pointpillars_bevgate_") : -len("_car.yaml")]
    text = source.read_text(encoding="utf-8")
    attention_marker = "        USE_BEV_ATTENTION: True\n"
    vfe_marker = "        NUM_FILTERS: [64]\n    MAP_TO_BEV:\n"
    if attention_marker not in text or vfe_marker not in text:
        raise RuntimeError(f"Expected marker missing in {source}")

    common = text.replace(attention_marker, "        USE_BEV_ATTENTION: False\n", 1)

    dapg = common.replace(
        vfe_marker,
        (
            "        NUM_FILTERS: [64]\n"
            "    BACKBONE_3D:\n"
            "        NAME: DensityAwarePillarGate\n"
            "        HIDDEN_CHANNELS: 32\n"
            "        MAX_POINTS_PER_VOXEL: 32\n"
            "        INIT_RESIDUAL_SCALE: 0.0\n"
            "    MAP_TO_BEV:\n"
        ),
        1,
    )
    (ROOT / f"pointpillars_dapg2_{dataset}_car.yaml").write_text(
        dapg, encoding="utf-8"
    )

    msbc = common.replace(
        "        USE_BEV_ATTENTION: False\n",
        (
            "        USE_BEV_ATTENTION: False\n"
            "        USE_MS_BEV_CONTEXT: True\n"
            "        MS_BEV_HIDDEN_CHANNELS: 32\n"
            "        MS_BEV_DILATIONS: [1, 2, 4]\n"
            "        MS_BEV_INIT_RESIDUAL_SCALE: 0.0\n"
        ),
        1,
    )
    (ROOT / f"pointpillars_msbc2_{dataset}_car.yaml").write_text(
        msbc, encoding="utf-8"
    )

    range_gate = common.replace(
        "        USE_BEV_ATTENTION: False\n",
        (
            "        USE_BEV_ATTENTION: False\n"
            "        USE_RANGE_AWARE_SPATIAL_GATE: True\n"
            "        RANGE_GATE_KERNEL_SIZE: 7\n"
            "        RANGE_GATE_INIT_RESIDUAL_SCALE: 0.0\n"
        ),
        1,
    )
    (ROOT / f"pointpillars_range2_{dataset}_car.yaml").write_text(
        range_gate, encoding="utf-8"
    )

    print(dataset)
