import pickle
import sys
from pathlib import Path

for raw in sys.argv[1:]:
    path = Path(raw)
    data = pickle.loads(path.read_bytes())
    print(path, "frames=", len(data))
    if data:
        print(" keys=", sorted(data[0].keys()))
        for key in ("scene", "scene_id", "sequence", "seq_id", "frame_id", "point_cloud"):
            vals = [str(item.get(key)) for item in data if key in item]
            if vals:
                print("", key, "unique=", len(set(vals)))
