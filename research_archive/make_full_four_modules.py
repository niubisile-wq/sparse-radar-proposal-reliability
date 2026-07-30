from pathlib import Path


ROOT = Path(__file__).resolve().parent

for source in sorted(ROOT.glob("pointpillars_bevgate_dapg_msbc_*_car.yaml")):
    dataset = source.name[len("pointpillars_bevgate_dapg_msbc_") : -len("_car.yaml")]
    text = source.read_text(encoding="utf-8")
    marker = "        MS_BEV_INIT_RESIDUAL_SCALE: 0.1\n"
    if marker not in text:
        raise RuntimeError(f"MSBC marker missing in {source}")
    block = (
        "        USE_RANGE_AWARE_SPATIAL_GATE: True\n"
        "        RANGE_GATE_KERNEL_SIZE: 7\n"
        "        RANGE_GATE_INIT_RESIDUAL_SCALE: 0.1\n"
    )
    target = ROOT / f"pointpillars_four_modules_{dataset}_car.yaml"
    target.write_text(text.replace(marker, marker + block, 1), encoding="utf-8")
    print(target.name)
