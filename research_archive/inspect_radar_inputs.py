from pathlib import Path
import pickle

import numpy as np


ROOT = Path("/root/autodl-tmp/radar_champion")
DATASETS = {
    "astyx": (
        ROOT / "repos/OpenPCDet_current/data/astyx/astyx_infos_train.pkl",
        ROOT / "repos/OpenPCDet_current/data/astyx",
    ),
    "truckscenes": (
        ROOT / "data/man-truckscenes-mini/unified/truckscenes_infos_train.pkl",
        ROOT / "data/man-truckscenes-mini/unified",
    ),
    "v2xradarv": (
        ROOT / "data/v2x-radar-v-400/unified/v2xradarv_infos_train.pkl",
        ROOT / "data/v2x-radar-v-400/unified",
    ),
    "kradar": (
        ROOT / "data/kradar-400/unified/kradar_infos_train.pkl",
        ROOT / "data/kradar-400/unified",
    ),
}


def describe(name, info_path, data_root):
    with info_path.open("rb") as handle:
        infos = pickle.load(handle)
    info = infos[0]
    print(f"\n[{name}] samples={len(infos)}")
    print(f"keys={sorted(info)}")
    print(f"point_cloud={info.get('point_cloud')}")
    print(f"frame_id={info.get('frame_id')}")
    print(f"metadata={info.get('metadata')}")

    frame = info["point_cloud"]["pc_idx"]
    if name == "astyx":
        path = data_root / "training/radar_6455" / f"{frame}.txt"
        # Astyx stores [x, y, z, radial_velocity, magnitude]; benchmark order
        # is [x, y, z, magnitude/RCS, radial_velocity].
        raw = np.loadtxt(path, dtype=np.float32, skiprows=2, usecols=(0, 1, 2, 3, 4))
        points = raw[:, [0, 1, 2, 4, 3]]
    else:
        path = data_root / "training/radar_6455" / f"{frame}.bin"
        points = np.fromfile(path, dtype=np.float32).reshape(-1, 5)
    print(f"sample_file={path}")
    print(f"shape={points.shape}")
    if points.ndim == 2 and len(points):
        for column in range(points.shape[1]):
            values = points[:, column]
            print(
                f"col{column}: min={values.min():.4f} "
                f"mean={values.mean():.4f} std={values.std():.4f} "
                f"max={values.max():.4f}"
            )


for dataset_name, (dataset_info, dataset_root) in DATASETS.items():
    describe(dataset_name, dataset_info, dataset_root)
