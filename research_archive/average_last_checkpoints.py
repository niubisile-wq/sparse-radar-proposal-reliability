#!/usr/bin/env python3
import argparse
from pathlib import Path

import torch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ckpt-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--count", type=int, default=5)
    args = parser.parse_args()

    ckpt_dir = Path(args.ckpt_dir)
    checkpoints = sorted(
        ckpt_dir.glob("checkpoint_epoch_*.pth"),
        key=lambda path: int(path.stem.rsplit("_", 1)[-1]),
    )
    selected = checkpoints[-args.count :]
    if len(selected) != args.count:
        raise RuntimeError(
            f"Expected {args.count} checkpoints in {ckpt_dir}, found {len(selected)}"
        )

    payloads = [torch.load(path, map_location="cpu") for path in selected]
    states = [payload["model_state"] for payload in payloads]
    averaged = {}
    for key, value in states[-1].items():
        if value.dtype.is_floating_point:
            total = value.to(torch.float64)
            for state in states[:-1]:
                total = total + state[key].to(torch.float64)
            averaged[key] = (total / len(states)).to(value.dtype)
        else:
            averaged[key] = value

    output_payload = dict(payloads[-1])
    output_payload["model_state"] = averaged
    output_payload["averaged_from"] = [str(path) for path in selected]
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    torch.save(output_payload, output)
    print("SWA_CHECKPOINT_OK", output, *[path.name for path in selected])


if __name__ == "__main__":
    main()
