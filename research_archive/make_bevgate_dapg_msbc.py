from pathlib import Path


ROOT = Path(__file__).resolve().parent

for source in sorted(ROOT.glob("pointpillars_bevgate_dapg_*_car.yaml")):
    dataset = source.name[len("pointpillars_bevgate_dapg_") : -len("_car.yaml")]
    text = source.read_text(encoding="utf-8")
    marker = "        BEV_ATTENTION_RESIDUAL: True\n"
    if marker not in text:
        raise RuntimeError(f"BEV attention marker missing in {source}")
    block = (
        "        USE_MS_BEV_CONTEXT: True\n"
        "        MS_BEV_HIDDEN_CHANNELS: 32\n"
        "        MS_BEV_DILATIONS: [1, 2, 4]\n"
        "        MS_BEV_INIT_RESIDUAL_SCALE: 0.1\n"
    )
    target = ROOT / f"pointpillars_bevgate_dapg_msbc_{dataset}_car.yaml"
    target.write_text(text.replace(marker, marker + block, 1), encoding="utf-8")
    print(target.name)
