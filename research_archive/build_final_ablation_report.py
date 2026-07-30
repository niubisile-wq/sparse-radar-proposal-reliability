#!/usr/bin/env python3
"""Build sequential and factorial ablation tables from authoritative logs."""

from __future__ import annotations

import csv
import math
import re
import statistics
from pathlib import Path


ROOT = Path("/root/autodl-tmp/radar_champion")
LOGS = ROOT / "logs" / "fair_ablation"
RESULTS = ROOT / "results"
DATASETS = ("astyx", "truckscenes", "v2xradarv", "kradar")
SEEDS = (2026, 2027, 2028)
T_CRIT = 4.303
AP_RE = re.compile(r"AP_R40@3D IoU 0\.50:\s*([0-9.]+)")

SEQUENTIAL = (
    ("baseline", "PointPillars"),
    ("rcnms", "+ M1 RC-NMS"),
    ("rdar", "+ M2 RDAR"),
    ("drav", "+ M3 DRAV"),
    ("drav_rgpc", "+ M4 RGPC"),
)
PREDECESSOR = {
    "rcnms": "baseline",
    "rdar": "rcnms",
    "drav": "rdar",
    "drav_rgpc": "drav",
}
FACTORIAL = ("pvd", "drav", "rgpc", "pvd_rgpc", "drav_rgpc")


def latest_completed_ap(paths):
    paths = sorted(
        paths,
        key=lambda path: (path.stat().st_mtime_ns, path.name),
    )
    for path in reversed(paths):
        text = path.read_text(encoding="utf-8", errors="ignore")
        values = AP_RE.findall(text)
        if values and (
            "Evaluation done." in text
            or "End evaluation" in text
            or "****************Evaluation done.*****************" in text
        ):
            return float(values[-1]), str(path)
    return None, None


def read_ap(module, dataset, seed):
    if module == "baseline":
        pattern = f"fair_pointpillars_{dataset}_seed{seed}_gpu*.log"
    elif module == "rcnms":
        pattern = f"fair_rcnms_{dataset}_seed{seed}_gpu*.log"
    elif module == "rdar":
        pattern = f"fair_rdar_{dataset}_seed{seed}_gpu*.log"
    else:
        pattern = f"eval_rdar_{module}_{dataset}_seed{seed}_gpu*.log"
    return latest_completed_ap(LOGS.glob(pattern))


def summary(values):
    valid = [value for value in values if value is not None]
    if not valid:
        return None, None
    return (
        statistics.mean(valid),
        statistics.stdev(valid) if len(valid) > 1 else 0.0,
    )


def paired_gate(current, previous):
    deltas = [
        current[index] - previous[index]
        for index in range(len(SEEDS))
        if current[index] is not None and previous[index] is not None
    ]
    result = {"n": len(deltas), "deltas": deltas, "passed": False}
    if not deltas:
        return result
    result["mean"] = statistics.mean(deltas)
    result["std"] = statistics.stdev(deltas) if len(deltas) > 1 else 0.0
    result["all_positive"] = all(delta > 0 for delta in deltas)
    if len(deltas) == 3:
        result["ci_lower"] = (
            result["mean"] - T_CRIT * result["std"] / math.sqrt(3)
        )
        result["passed"] = (
            result["all_positive"]
            and result["mean"] >= 1.0
            and result["ci_lower"] > 0
        )
    return result


def fmt(value, signed=False):
    if value is None:
        return "—"
    return f"{value:+.4f}" if signed else f"{value:.4f}"


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    modules = [name for name, _ in SEQUENTIAL]
    modules.extend(name for name in FACTORIAL if name not in modules)
    values = {}
    rows = []
    for module in modules:
        for dataset in DATASETS:
            for seed in SEEDS:
                ap, log = read_ap(module, dataset, seed)
                values[(module, dataset, seed)] = ap
                rows.append(
                    {
                        "module": module,
                        "dataset": dataset,
                        "seed": seed,
                        "ap": ap,
                        "log": log,
                    }
                )

    csv_path = RESULTS / "final_ablation_seed_results.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=("module", "dataset", "seed", "ap", "log")
        )
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# Final four-module ablation",
        "",
        "Acceptance gate: all paired seeds positive, mean incremental gain "
        "≥ +1.0 AP, paired 95% CI lower bound > 0.",
        "",
        "## Sequential AP",
        "",
        "| System | Astyx | TruckScenes | V2X-Radar-V | K-Radar | Macro |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    label_by_module = dict(SEQUENTIAL)
    for module, label in SEQUENTIAL:
        means = []
        cells = []
        for dataset in DATASETS:
            samples = [values[(module, dataset, seed)] for seed in SEEDS]
            mean, std = summary(samples)
            cells.append(
                "—"
                if mean is None
                else f"{mean:.4f} ± {std:.4f} "
                f"(n={sum(value is not None for value in samples)})"
            )
            if mean is not None:
                means.append(mean)
        macro = statistics.mean(means) if len(means) == 4 else None
        lines.append(f"| {label} | {' | '.join(cells)} | {fmt(macro)} |")

    lines.extend(
        [
            "",
            "## Sequential paired increments",
            "",
            "| Step | Dataset | Seed deltas | Mean | CI95 lower | n | Pass |",
            "|---|---|---|---:|---:|---:|:---:|",
        ]
    )
    for module, label in SEQUENTIAL[1:]:
        previous = PREDECESSOR[module]
        for dataset in DATASETS:
            current_values = [
                values[(module, dataset, seed)] for seed in SEEDS
            ]
            previous_values = [
                values[(previous, dataset, seed)] for seed in SEEDS
            ]
            gate = paired_gate(current_values, previous_values)
            delta_cells = ", ".join(
                fmt(delta, signed=True) for delta in gate["deltas"]
            ) or "—"
            lines.append(
                f"| {label_by_module[previous]} → {label} | {dataset} | "
                f"{delta_cells} | {fmt(gate.get('mean'), signed=True)} | "
                f"{fmt(gate.get('ci_lower'), signed=True)} | {gate['n']} | "
                f"{'yes' if gate['passed'] else 'no/pending'} |"
            )

    lines.extend(
        [
            "",
            "## Training-module factorial controls",
            "",
            "| Variant | Astyx | TruckScenes | V2X-Radar-V | K-Radar |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for module in FACTORIAL:
        cells = []
        for dataset in DATASETS:
            samples = [values[(module, dataset, seed)] for seed in SEEDS]
            mean, std = summary(samples)
            cells.append(
                "—" if mean is None else f"{mean:.4f} ± {std:.4f}"
            )
        lines.append(f"| {module} | {' | '.join(cells)} |")

    lines.extend(
        [
            "",
            "## Context-module incremental controls",
            "",
            "| Comparison | Dataset | Mean ΔAP | CI95 lower | n | Pass |",
            "|---|---|---:|---:|---:|:---:|",
        ]
    )
    for current, previous in (
        ("pvd_rgpc", "pvd"),
        ("drav_rgpc", "drav"),
    ):
        for dataset in DATASETS:
            gate = paired_gate(
                [values[(current, dataset, seed)] for seed in SEEDS],
                [values[(previous, dataset, seed)] for seed in SEEDS],
            )
            lines.append(
                f"| {previous} → {current} | {dataset} | "
                f"{fmt(gate.get('mean'), signed=True)} | "
                f"{fmt(gate.get('ci_lower'), signed=True)} | {gate['n']} | "
                f"{'yes' if gate['passed'] else 'no/pending'} |"
            )

    report_path = RESULTS / "final_ablation_report.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(csv_path)
    print(report_path)


if __name__ == "__main__":
    main()
