import pickle

p = pickle.load(open('/root/autodl-tmp/radar_champion/results/rdar_astyx_seed2026.pkl', 'rb'))
print('pred keys', p[0].keys())
print('pred shapes', {k: (type(v).__name__, getattr(v, 'shape', None)) for k, v in p[0].items()})
i = pickle.load(open('data/astyx/astyx_infos_val.pkl', 'rb'))
print('info keys', i[0].keys())
print('anno keys', i[0].get('annos', {}).keys())
gt = i[0]['annos'].get('gt_boxes_lidar')
print('gt shape', None if gt is None else gt.shape)
