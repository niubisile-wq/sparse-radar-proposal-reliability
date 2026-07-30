#!/usr/bin/env python3
"""Reproducible screen/formal gate for sequential radar module candidates."""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
from pathlib import Path


DATASETS = ("astyx", "truckscenes", "v2xradarv", "kradar")
SEEDS = (2026, 2027, 2028)
REFERENCE = {
    "astyx": {2026: 32.7281, 2027: 31.4220, 2028: 34.3540},
    "truckscenes": {2026: 15.4127, 2027: 18.3845, 2028: 15.3041},
    "v2xradarv": {2026: 40.7802, 2027: 42.9899, 2028: 41.3385},
    "kradar": {2026: 51.3450, 2027: 48.1767, 2028: 52.0271},
}
AP_RE = re.compile(r"AP_R40@3D IoU 0\.50:\s*([0-9.]+)")
T_CRIT_975_DF2 = 4.303


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("variant")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("/root/autodl-tmp/radar_champion"),
    )
    parser.add_argument("--mode", choices=("screen", "formal"), default="formal")
    parser.add_argument("--min-gain", type=float, default=1.0)
    parser.add_argument(
        "--reference-variant",
        help=(
            "Compare against another evaluated variant instead of the fixed "
            "RDAR reference. Seeds and datasets are paired."
        ),
    )
    return parser.parse_args()


def read_completed_ap(log_dir: Path, variant: str, dataset: str, seed: int):
    paths = sorted(
        log_dir.glob(f"eval_rdar_{variant}_{dataset}_seed{seed}_gpu*.log"),
        key=lambda path: (path.stat().st_mtime_ns, path.name),
    )
    if not paths:
        return None, None
    path = paths[-1]
    text = path.read_text(encoding="utf-8", errors="ignore")
    values = AP_RE.findall(text)
    complete = "Evaluation done." in text
    if not complete or not values:
        return None, str(path)
    return float(values[-1]), str(path)


def main() -> int:
    args = parse_args()
    log_dir = args.root / "logs" / "fair_ablation"
    result_dir = args.root / "results"
    result_dir.mkdir(parents=True, exist_ok=True)
    required_seeds = (2028,) if args.mode == "screen" else SEEDS

    reference_name = args.reference_variant or "rdar"
    report = {
        "variant": args.variant,
        "mode": args.mode,
        "reference": reference_name,
        "minimum_gain_ap": args.min_gain,
        "datasets": {},
        "complete": True,
        "passed": True,
    }
    for dataset in DATASETS:
        aps = {}
        reference_aps = {}
        deltas = {}
        logs = {}
        reference_logs = {}
        for seed in required_seeds:
            ap, log = read_completed_ap(
                log_dir, args.variant, dataset, seed
            )
            logs[str(seed)] = log
            aps[str(seed)] = ap
            if args.reference_variant:
                reference_ap, reference_log = read_completed_ap(
                    log_dir, args.reference_variant, dataset, seed
                )
            else:
                reference_ap = REFERENCE[dataset][seed]
                reference_log = "fixed RDAR reference"
            reference_aps[str(seed)] = reference_ap
            reference_logs[str(seed)] = reference_log
            deltas[str(seed)] = (
                None
                if ap is None or reference_ap is None
                else ap - reference_ap
            )

        complete = all(value is not None for value in deltas.values())
        dataset_result = {
            "ap": aps,
            "reference_ap": reference_aps,
            "delta_ap": deltas,
            "logs": logs,
            "reference_logs": reference_logs,
            "complete": complete,
            "passed": False,
        }
        if complete and args.mode == "screen":
            delta = deltas["2028"]
            dataset_result["passed"] = delta >= args.min_gain
        elif complete:
            values = [deltas[str(seed)] for seed in SEEDS]
            mean = statistics.mean(values)
            std = statistics.stdev(values)
            ci_lower = mean - T_CRIT_975_DF2 * std / math.sqrt(3)
            dataset_result.update(
                {
                    "mean_delta_ap": mean,
                    "std_delta_ap": std,
                    "paired_ci95_lower": ci_lower,
                    "all_seeds_positive": all(value > 0 for value in values),
                }
            )
            dataset_result["passed"] = (
                dataset_result["all_seeds_positive"]
                and mean >= args.min_gain
                and ci_lower > 0
            )

        report["datasets"][dataset] = dataset_result
        report["complete"] &= complete
        report["passed"] &= dataset_result["passed"]

    stem = f"{args.variant}_vs_{reference_name}_{args.mode}_gate"
    json_path = result_dir / f"{stem}.json"
    json_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    markdown = [
        f"# {args.variant}: {args.mode} gate",
        "",
        f"- Reference: {reference_name}",
        f"- Minimum gain: {args.min_gain:.1f} AP",
        f"- Complete: {report['complete']}",
        f"- Passed: {report['passed']}",
        "",
        "| Dataset | AP / delta by seed | Mean delta | CI95 lower | Pass |",
        "|---|---|---:|---:|:---:|",
    ]
    for dataset, item in report["datasets"].items():
        cells = ", ".join(
            (
                f"{seed}: pending"
                if item["ap"][str(seed)] is None
                else f"{seed}: {item['ap'][str(seed)]:.4f} "
                f"({item['delta_ap'][str(seed)]:+.4f})"
            )
            for seed in required_seeds
        )
        mean = item.get("mean_delta_ap")
        ci_lower = item.get("paired_ci95_lower")
        markdown.append(
            f"| {dataset} | {cells} | "
            f"{'—' if mean is None else f'{mean:+.4f}'} | "
            f"{'—' if ci_lower is None else f'{ci_lower:+.4f}'} | "
            f"{'yes' if item['passed'] else 'no/pending'} |"
        )
    markdown_path = result_dir / f"{stem}.md"
    markdown_path.write_text("\n".join(markdown) + "\n", encoding="utf-8")
    print(json_path)
    print(markdown_path)

    if not report["complete"]:
        return 2
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
