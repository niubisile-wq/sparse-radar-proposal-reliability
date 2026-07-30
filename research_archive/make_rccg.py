from pathlib import Path


ROOT = Path(__file__).resolve().parent
for source in sorted(ROOT.glob("pointpillars_bevgate_*_car.yaml")):
    if any(token in source.name for token in ("_dapg_", "_msbc_")):
        continue
    dataset = source.name[len("pointpillars_bevgate_") : -len("_car.yaml")]
    text = source.read_text(encoding="utf-8")
    marker = "        USE_BEV_ATTENTION: True\n"
    replacement = (
        "        USE_BEV_ATTENTION: False\n"
        "        USE_RADAR_CHANNEL_CONTRAST_GATE: True\n"
        "        RADAR_CHANNEL_GATE_REDUCTION: 8\n"
        "        RADAR_CHANNEL_GATE_INIT_SCALE: 0.0\n"
    )
    if marker not in text:
        raise RuntimeError(f"BEV gate marker missing in {source}")
    target = ROOT / f"pointpillars_rccg_{dataset}_car.yaml"
    target.write_text(text.replace(marker, replacement, 1), encoding="utf-8")
    print(target.name)
