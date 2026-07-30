from pathlib import Path
import sys

from pcdet.config import cfg, cfg_from_yaml_file
from pcdet.datasets.astyx import astyx_dataset as astyx_dataset_module
from pcdet.datasets.unified_radar.unified_radar_dataset import UnifiedRadarDataset


ROOT = Path('/root/autodl-tmp/radar_champion')
REPO = ROOT / 'repos/OpenPCDet_current'
SPECS = {
    'truckscenes': (
        ROOT / 'data/man-truckscenes-mini/unified',
        'truckscenes_infos_train.pkl',
    ),
    'v2xradarv': (
        ROOT / 'data/v2x-radar-v-400/unified',
        'v2xradarv_infos_train.pkl',
    ),
    'kradar': (
        ROOT / 'data/kradar-400/unified',
        'kradar_infos_train.pkl',
    ),
}


def main(dataset_name):
    # The upstream Astyx database helper references Path without importing it.
    astyx_dataset_module.Path = Path
    data_path, info_name = SPECS[dataset_name]
    cfg_file = (
        REPO / 'tools/cfgs/astyx_models'
        / f'pointpillars_iouaware_{dataset_name}_car.yaml'
    )
    local_cfg = cfg_from_yaml_file(str(cfg_file), cfg)
    local_cfg.DATA_CONFIG.DATASET = 'UnifiedRadarDataset'
    local_cfg.DATA_CONFIG.DATA_PATH = str(data_path)
    local_cfg.DATA_CONFIG.INFO_PATH.train = [info_name]
    dataset = UnifiedRadarDataset(
        dataset_cfg=local_cfg.DATA_CONFIG,
        class_names=['Car'],
        training=True,
        root_path=data_path,
        logger=None,
    )
    dataset.create_groundtruth_database(
        info_path=data_path / info_name,
        used_classes=['Car'],
        split='train',
    )


if __name__ == '__main__':
    main(sys.argv[1])
