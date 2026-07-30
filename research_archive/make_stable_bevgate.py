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
        "        USE_STABLE_BEV_GATE: True\n"
        "        STABLE_BEV_GATE_REDUCTION: 8\n"
        "        STABLE_BEV_GATE_INIT_SCALE: 0.1\n"
    )
    if marker not in text:
        raise RuntimeError(f"BEV gate marker missing in {source}")
    target = ROOT / f"pointpillars_stable_bevgate_{dataset}_car.yaml"
    target.write_text(text.replace(marker, replacement, 1), encoding="utf-8")
    print(target.name)
