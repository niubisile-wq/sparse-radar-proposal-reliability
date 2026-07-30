from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent
for dataset in ('astyx', 'truckscenes', 'v2xradarv', 'kradar'):
    source = ROOT / f'pointpillars_corner_{dataset}_car.yaml'
    target = ROOT / f'pointpillars_corner02_{dataset}_car.yaml'
    cfg = yaml.safe_load(source.read_text())
    cfg['MODEL']['DENSE_HEAD']['CORNER_LOSS_WEIGHT'] = 0.2
    target.write_text(yaml.safe_dump(cfg, sort_keys=False))
    print(target)
