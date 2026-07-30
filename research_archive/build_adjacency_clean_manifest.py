"""Build a reproducible validation manifest after a numeric +/-1 ID audit.

This is a sensitivity-manifest generator, not an AP evaluator.  It deliberately
does not assume that pc_idx is temporal; it only applies the documented audit
rule and records the retained IDs so that predictions can be re-evaluated when
the corresponding per-frame prediction archive is available.
"""

import argparse
import json
import pickle
from pathlib import Path


def load_rows(path: Path):
    with path.open("rb") as handle:
        obj = pickle.load(handle)
    if isinstance(obj, dict):
        for key in ("infos", "data", "annos"):
            if key in obj and isinstance(obj[key], list):
                obj = obj[key]
                break
    if not isinstance(obj, list):
        raise TypeError(f"Expected a list-like info file: {path}")
    return obj


def pc_id(row):
    value = row.get("point_cloud", {}).get("pc_idx")
    if value is None:
        raise KeyError("Missing point_cloud.pc_idx")
    return int(value)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("train_info", type=Path)
    parser.add_argument("val_info", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    train_rows = load_rows(args.train_info)
    val_rows = load_rows(args.val_info)
    train_ids = {pc_id(row) for row in train_rows}
    val_ids = [pc_id(row) for row in val_rows]
    keep = [idx for idx, frame_id in enumerate(val_ids)
            if frame_id - 1 not in train_ids and frame_id + 1 not in train_ids]
    payload = {
        "rule": "retain validation rows whose numeric pc_idx is not within +/-1 of any train pc_idx",
        "train_info": str(args.train_info),
        "val_info": str(args.val_info),
        "train_frames": len(train_rows),
        "validation_frames": len(val_rows),
        "retained_frames": len(keep),
        "excluded_frames": len(val_rows) - len(keep),
        "retained_validation_row_indices": keep,
        "retained_pc_idx": [val_ids[idx] for idx in keep],
        "note": "pc_idx adjacency is an audit signal, not proof of temporal order or scene identity.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: payload[k] for k in
                      ("train_frames", "validation_frames", "retained_frames", "excluded_frames")},
                     sort_keys=True))


if __name__ == "__main__":
    main()
