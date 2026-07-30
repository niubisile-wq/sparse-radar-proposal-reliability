import pickle
import sys
from pathlib import Path

for train_path, val_path in zip(sys.argv[1::2], sys.argv[2::2]):
    train = pickle.loads(Path(train_path).read_bytes())
    val = pickle.loads(Path(val_path).read_bytes())
    def ids(rows):
        return {str(row.get("point_cloud", {}).get("pc_idx")) for row in rows}
    def car_count(rows):
        total = 0
        for row in rows:
            names = row.get("annos", {}).get("name", [])
            total += sum(str(name).lower() == "car" for name in names)
        return total
    train_ids, val_ids = ids(train), ids(val)
    overlap = train_ids & val_ids
    train_int = {int(x) for x in train_ids if x.isdigit()}
    val_int = {int(x) for x in val_ids if x.isdigit()}
    adjacent = sum((x - 1 in train_int or x + 1 in train_int) for x in val_int)
    print(Path(train_path).name, "train=", len(train_ids), "val=", len(val_ids),
          "car_instances=", car_count(train), "/", car_count(val),
          "pc_idx_overlap=", len(overlap), "train_minmax=", (min(train_ids), max(train_ids)),
          "val_minmax=", (min(val_ids), max(val_ids)))
    print(" validation_frames_adjacent_to_train=", adjacent, "/", len(val_int))
    print(" first_train=", sorted(train_ids)[:8], "first_val=", sorted(val_ids)[:8])
