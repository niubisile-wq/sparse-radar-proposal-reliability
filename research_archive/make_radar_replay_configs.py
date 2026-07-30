from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent
DATASETS = ('astyx', 'truckscenes', 'v2xradarv', 'kradar')
DB_INFO = {
    'astyx': 'astyx_dbinfos_train.pkl',
    'truckscenes': 'astyx_dbinfos_train.pkl',
    'v2xradarv': 'astyx_dbinfos_train.pkl',
    'kradar': 'astyx_dbinfos_train.pkl',
}


def main():
    for dataset in DATASETS:
        source = ROOT / f'pointpillars_iouaware_{dataset}_car.yaml'
        target = ROOT / f'pointpillars_iouaware_radarreplay_{dataset}_car.yaml'
        cfg = yaml.safe_load(source.read_text())
        # DatasetTemplate consumes DATA_CONFIG.DATA_AUGMENTOR.  Some legacy
        # experiment YAMLs also contain a top-level copy, which is only logged
        # and otherwise ignored; explicitly override the nested configuration.
        augmentor = cfg['DATA_AUGMENTOR']
        augmentor['DISABLE_AUG_LIST'] = [
            name for name in augmentor.get('DISABLE_AUG_LIST', [])
            if name != 'gt_sampling'
        ]
        sampler = next(
            item for item in augmentor['AUG_CONFIG_LIST']
            if item['NAME'] == 'gt_sampling'
        )
        sampler['USE_ROAD_PLANE'] = False
        sampler['DB_INFO_PATH'] = [DB_INFO[dataset]]
        sampler['PREPARE'] = {
            'filter_by_min_points': ['Car:1'],
            'filter_by_difficulty': [-1],
        }
        sampler['SAMPLE_GROUPS'] = ['Car:15']
        sampler['NUM_POINT_FEATURES'] = 5
        sampler['DATABASE_WITH_FAKELIDAR'] = False
        sampler['REMOVE_EXTRA_WIDTH'] = [0.0, 0.0, 0.0]
        sampler['LIMIT_WHOLE_SCENE'] = False
        cfg['DATA_CONFIG']['DATA_AUGMENTOR'] = augmentor
        cfg.pop('DATA_AUGMENTOR', None)
        target.write_text(yaml.safe_dump(cfg, sort_keys=False))
        print(target)


if __name__ == '__main__':
    main()
