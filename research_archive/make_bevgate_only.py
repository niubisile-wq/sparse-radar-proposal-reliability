from pathlib import Path


ROOT = Path(__file__).resolve().parent
PREFIX = "radardg_m2_pgdr_dropout_bevgate_pillarattn_"


def remove_named_list_item(lines, item_name):
    output = []
    index = 0
    marker = f"- NAME: {item_name}"
    while index < len(lines):
        line = lines[index]
        if line.strip() != marker:
            output.append(line)
            index += 1
            continue

        indent = len(line) - len(line.lstrip())
        index += 1
        while index < len(lines):
            candidate = lines[index]
            if candidate.strip():
                candidate_indent = len(candidate) - len(candidate.lstrip())
                if candidate_indent <= indent:
                    break
            index += 1
    return output


def remove_mapping_block(lines, key):
    output = []
    index = 0
    marker = f"{key}:"
    while index < len(lines):
        line = lines[index]
        if line.strip() != marker:
            output.append(line)
            index += 1
            continue

        indent = len(line) - len(line.lstrip())
        index += 1
        while index < len(lines):
            candidate = lines[index]
            if candidate.strip():
                candidate_indent = len(candidate) - len(candidate.lstrip())
                if candidate_indent <= indent:
                    break
            index += 1
    return output


for source in sorted(ROOT.glob(f"{PREFIX}*_car.yaml")):
    dataset = source.name[len(PREFIX) : -len("_car.yaml")]
    lines = source.read_text(encoding="utf-8").splitlines(keepends=True)
    lines = remove_named_list_item(lines, "radar_statistical_canonicalization")
    lines = remove_named_list_item(lines, "physics_guided_radar_augmentation")
    lines = remove_mapping_block(lines, "BACKBONE_3D")
    lines = [
        line
        for line in lines
        if line.strip()
        not in {
            "USE_VELOCITY_DECOMPOSITION: True",
            "EXTRA_INPUT_FEATURES: 2",
        }
    ]
    target = ROOT / f"pointpillars_bevgate_{dataset}_car.yaml"
    target.write_text("".join(lines), encoding="utf-8")
    print(target.name)
