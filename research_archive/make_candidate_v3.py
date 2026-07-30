from pathlib import Path


root = Path(__file__).resolve().parent
for module in ("dapg", "msbc", "range"):
    for source in sorted(root.glob(f"pointpillars_{module}2_*_car.yaml")):
        dataset = source.name[len(f"pointpillars_{module}2_") : -len("_car.yaml")]
        target = root / f"pointpillars_{module}3_{dataset}_car.yaml"
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        print(target.name)
