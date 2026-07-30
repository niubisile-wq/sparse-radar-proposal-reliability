from pathlib import Path


root = Path(__file__).resolve().parent
variants = {"sbd05": 0.05, "sbd10": 0.10, "sbd20": 0.20}
for source in sorted(root.glob("pointpillars_bevgate_*_car.yaml")):
    if any(token in source.name for token in ("_dapg_", "_msbc_")):
        continue
    dataset = source.name[len("pointpillars_bevgate_") : -len("_car.yaml")]
    text = source.read_text(encoding="utf-8")
    marker = "        USE_BEV_ATTENTION: True\n"
    if marker not in text:
        raise RuntimeError(f"BEV attention marker missing in {source}")
    for module, probability in variants.items():
        replacement = (
            "        USE_BEV_ATTENTION: False\n"
            f"        BEV_FEATURE_DROPOUT_P: {probability:.2f}\n"
        )
        target = root / f"pointpillars_{module}_{dataset}_car.yaml"
        target.write_text(text.replace(marker, replacement, 1), encoding="utf-8")
        print(target.name)
