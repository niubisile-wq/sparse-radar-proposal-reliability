from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent
VARIANTS = {
    'rpa55': (0.55, 0.40),
    'rpa50': (0.50, 0.35),
    'rpa45': (0.45, 0.30),
}

for dataset in ('astyx', 'truckscenes', 'v2xradarv', 'kradar'):
    source = ROOT / f'pointpillars_bevgate_{dataset}_car.yaml'
    for name, (matched, unmatched) in VARIANTS.items():
        cfg = yaml.safe_load(source.read_text())
        cfg['MODEL']['BACKBONE_2D']['USE_BEV_ATTENTION'] = False
        for anchor_cfg in cfg['MODEL']['DENSE_HEAD']['ANCHOR_GENERATOR_CONFIG']:
            if anchor_cfg['class_name'] == 'Car':
                anchor_cfg['matched_threshold'] = matched
                anchor_cfg['unmatched_threshold'] = unmatched
        post = cfg['MODEL']['POST_PROCESSING']
        post['SCORE_THRESH'] = 0.0
        post['NMS_CONFIG']['NMS_THRESH'] = 0.50
        target = ROOT / f'pointpillars_{name}_{dataset}_car.yaml'
        target.write_text(yaml.safe_dump(cfg, sort_keys=False))
        print(target)
