#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import torch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--a", required=True)
    parser.add_argument("--b", required=True)
    parser.add_argument("--weight_b", type=float, required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    checkpoint_a = torch.load(args.a, map_location="cpu")
    checkpoint_b = torch.load(args.b, map_location="cpu")
    state_a = checkpoint_a["model_state"]
    state_b = checkpoint_b["model_state"]
    if state_a.keys() != state_b.keys():
        raise ValueError("Model state keys differ")

    weight_b = args.weight_b
    output_state = {}
    for key, value_a in state_a.items():
        value_b = state_b[key]
        if value_a.shape != value_b.shape:
            raise ValueError(f"Shape mismatch for {key}")
        if torch.is_floating_point(value_a):
            output_state[key] = value_a.mul(1.0 - weight_b).add(
                value_b, alpha=weight_b
            )
        else:
            output_state[key] = value_a

    output_checkpoint = dict(checkpoint_a)
    output_checkpoint["model_state"] = output_state
    output_checkpoint["optimizer_state"] = None
    output_checkpoint["it"] = 0.0
    output_checkpoint["epoch"] = -1
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    torch.save(output_checkpoint, output)


if __name__ == "__main__":
    main()
