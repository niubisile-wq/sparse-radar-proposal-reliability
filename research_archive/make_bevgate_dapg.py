from pathlib import Path


ROOT = Path(__file__).resolve().parent

for source in sorted(ROOT.glob("pointpillars_bevgate_*_car.yaml")):
    dataset = source.name[len("pointpillars_bevgate_") : -len("_car.yaml")]
    text = source.read_text(encoding="utf-8")
    marker = "    MAP_TO_BEV:\n"
    if marker not in text:
        raise RuntimeError(f"MAP_TO_BEV marker missing in {source}")
    block = (
        "    BACKBONE_3D:\n"
        "        NAME: DensityAwarePillarGate\n"
        "        HIDDEN_CHANNELS: 32\n"
        "        MAX_POINTS_PER_VOXEL: 32\n"
        "        INIT_RESIDUAL_SCALE: 0.1\n"
    )
    target = ROOT / f"pointpillars_bevgate_dapg_{dataset}_car.yaml"
    target.write_text(text.replace(marker, block + marker, 1), encoding="utf-8")
    print(target.name)
