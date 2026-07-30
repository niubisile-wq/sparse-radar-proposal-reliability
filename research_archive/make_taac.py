from __future__ import annotations

import pickle
import re
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
REPO_CONFIG_ROOT = (
    ROOT / "repos" / "OpenPCDet_current" / "tools" / "cfgs" / "astyx_models"
)
INFO_PATHS = {
    "astyx": Path(
        "/root/autodl-tmp/radar_champion/repos/OpenPCDet_current/data/astyx/"
        "astyx_infos_train.pkl"
    ),
    "truckscenes": Path(
        "/root/autodl-tmp/radar_champion/data/man-truckscenes-mini/unified/"
        "truckscenes_infos_train.pkl"
    ),
    "v2xradarv": Path(
        "/root/autodl-tmp/radar_champion/data/v2x-radar-v-400/unified/"
        "v2xradarv_infos_train.pkl"
    ),
    "kradar": Path(
        "/root/autodl-tmp/radar_champion/data/kradar-400/unified/"
        "kradar_infos_train.pkl"
    ),
}


def estimate_car_anchor(info_path: Path) -> tuple[list[float], float, int]:
    with info_path.open("rb") as stream:
        infos = pickle.load(stream)

    dimensions: list[np.ndarray] = []
    bottom_heights: list[np.ndarray] = []
    for info in infos:
        annos = info.get("annos", {})
        boxes = np.asarray(annos.get("gt_boxes", []), dtype=np.float64).reshape(-1, 7)
        names = np.asarray(annos.get("name", ["Car"] * len(boxes)))
        boxes = boxes[names == "Car"]
        if not len(boxes):
            continue

        # Some source converters encode the horizontal dimensions as (w, l)
        # and others as (l, w).  Canonicalize to (long, short, height).
        horizontal = np.sort(boxes[:, 3:5], axis=1)[:, ::-1]
        dimensions.append(np.column_stack((horizontal, boxes[:, 5])))
        bottom_heights.append(boxes[:, 2] - boxes[:, 5] / 2.0)

    dims = np.concatenate(dimensions, axis=0)
    bottoms = np.concatenate(bottom_heights, axis=0)
    anchor_size = np.median(dims, axis=0).round(4).tolist()
    bottom_height = round(float(np.median(bottoms)), 4)
    return anchor_size, bottom_height, len(dims)


def replace_car_anchor(text: str, size: list[float], bottom: float) -> str:
    pattern = re.compile(
        r"(\{'class_name': 'Car', 'anchor_sizes': )"
        r"(\[\[[^\]]+\]\])"
        r"(, 'anchor_rotations': \[[^\]]+\], 'anchor_bottom_heights': )"
        r"(\[[^\]]+\])"
    )
    replacement = (
        rf"\g<1>[[{', '.join(f'{value:.4f}' for value in size)}]]"
        rf"\g<3>[{bottom:.4f}]"
    )
    updated, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError("Could not uniquely replace the Car anchor config")
    if "USE_BEV_ATTENTION: True" not in updated:
        raise RuntimeError("Expected baseline BEV attention marker was not found")
    return updated.replace("USE_BEV_ATTENTION: True", "USE_BEV_ATTENTION: False", 1)


def main() -> None:
    for dataset, info_path in INFO_PATHS.items():
        size, bottom, count = estimate_car_anchor(info_path)
        source = ROOT / f"pointpillars_bevgate_{dataset}_car.yaml"
        if not source.exists():
            source = REPO_CONFIG_ROOT / source.name
        target = ROOT / f"pointpillars_taac_{dataset}_car.yaml"
        target.write_text(
            replace_car_anchor(source.read_text(encoding="utf-8"), size, bottom),
            encoding="utf-8",
        )
        print(
            f"{dataset}: n={count} anchor_size={size} "
            f"bottom_height={bottom} -> {target.name}"
        )


if __name__ == "__main__":
    main()
