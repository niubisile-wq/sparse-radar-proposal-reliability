from pathlib import Path


ROOT = Path(__file__).resolve().parent

for source in sorted(ROOT.glob("pointpillars_stable_bevgate_*_car.yaml")):
    if any(token in source.name for token in ("_dapg_", "_msbc_")):
        continue
    dataset = source.name[len("pointpillars_stable_bevgate_") : -len("_car.yaml")]
    stable_text = source.read_text(encoding="utf-8")

    map_marker = "    MAP_TO_BEV:\n"
    dapg_block = (
        "    BACKBONE_3D:\n"
        "        NAME: DensityAwarePillarGate\n"
        "        HIDDEN_CHANNELS: 32\n"
        "        MAX_POINTS_PER_VOXEL: 32\n"
        "        INIT_RESIDUAL_SCALE: 0.1\n"
    )
    if map_marker not in stable_text:
        raise RuntimeError(f"MAP_TO_BEV marker missing in {source}")
    dapg_text = stable_text.replace(map_marker, dapg_block + map_marker, 1)
    dapg_target = ROOT / f"pointpillars_stable_bevgate_dapg_{dataset}_car.yaml"
    dapg_target.write_text(dapg_text, encoding="utf-8")

    gate_marker = "        STABLE_BEV_GATE_INIT_SCALE: 0.1\n"
    msbc_block = (
        "        USE_MS_BEV_CONTEXT: True\n"
        "        MS_BEV_HIDDEN_CHANNELS: 32\n"
        "        MS_BEV_DILATIONS: [1, 2, 4]\n"
        "        MS_BEV_INIT_RESIDUAL_SCALE: 0.1\n"
    )
    if gate_marker not in dapg_text:
        raise RuntimeError(f"Stable gate marker missing in {source}")
    msbc_text = dapg_text.replace(gate_marker, gate_marker + msbc_block, 1)
    msbc_target = (
        ROOT / f"pointpillars_stable_bevgate_dapg_msbc_{dataset}_car.yaml"
    )
    msbc_target.write_text(msbc_text, encoding="utf-8")

    msbc_marker = "        MS_BEV_INIT_RESIDUAL_SCALE: 0.1\n"
    range_block = (
        "        USE_RANGE_AWARE_SPATIAL_GATE: True\n"
        "        RANGE_GATE_KERNEL_SIZE: 7\n"
        "        RANGE_GATE_INIT_RESIDUAL_SCALE: 0.1\n"
    )
    full_text = msbc_text.replace(msbc_marker, msbc_marker + range_block, 1)
    full_target = ROOT / f"pointpillars_stable_four_modules_{dataset}_car.yaml"
    full_target.write_text(full_text, encoding="utf-8")

    print(dapg_target.name, msbc_target.name, full_target.name)
