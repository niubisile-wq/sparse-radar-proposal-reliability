from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent
DATASETS = ('astyx', 'truckscenes', 'v2xradarv', 'kradar')


def main():
    for dataset in DATASETS:
        source = ROOT / f'pointpillars_bevgate_{dataset}_car.yaml'
        target = ROOT / f'pointpillars_corner_{dataset}_car.yaml'
        cfg = yaml.safe_load(source.read_text())
        cfg['MODEL']['BACKBONE_2D']['USE_BEV_ATTENTION'] = False
        head = cfg['MODEL']['DENSE_HEAD']
        head['NAME'] = 'AnchorHeadCornerAware'
        head['CORNER_LOSS_WEIGHT'] = 1.0
        post = cfg['MODEL']['POST_PROCESSING']
        post['SCORE_THRESH'] = 0.0
        post['NMS_CONFIG']['NMS_THRESH'] = 0.50
        target.write_text(yaml.safe_dump(cfg, sort_keys=False))
        print(target)


if __name__ == '__main__':
    main()
