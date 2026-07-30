#!/usr/bin/env python3
import csv
import math
import statistics
import sys
from pathlib import Path

from collect_fair_ablation import (
    DATASETS,
    LOG_PATTERN,
    MIN_PRACTICAL_AP_GAIN,
    PREDECESSOR,
    T_CRITICAL_975,
    parse_log,
)


def fmt(value):
    return "—" if value is None else f"{value:.4f}"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    log_dir = root / "logs" / "fair_ablation"
    result_dir = root / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    values = {}
    for path in sorted(log_dir.glob("fair_*_seed*_gpu*.log")):
        match = LOG_PATTERN.match(path.name)
        if not match:
            continue
        parsed = parse_log(path)
        row = {**match.groupdict(), **parsed, "log": str(path)}
        row["seed"] = int(row["seed"])
        rows.append(row)
        values[(row["module"], row["dataset"], row["seed"])] = row["ap"]

    detail_path = result_dir / "fair_ablation_seed_results.csv"
    with detail_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=(
                "module",
                "dataset",
                "seed",
                "ap",
                "complete",
                "error",
                "log",
            ),
        )
        writer.writeheader()
        writer.writerows(rows)

    seeds = sorted({row["seed"] for row in rows})
    discovered = {row["module"] for row in rows}
    preferred_order = [
        "pointpillars",
        "bevgate",
        "stable_bevgate",
        "rccg",
        "dapg2",
        "msbc2",
        "range2",
        "dapg3",
        "msbc3",
        "range3",
        "sbd05",
        "sbd10",
        "sbd20",
        "swa5",
        "rcnms",
        "taac_rcnms",
        "rdar",
        "stable_bevgate_dapg",
        "stable_bevgate_dapg_msbc",
        "stable_four_modules",
    ]
    modules = [module for module in preferred_order if module in discovered]
    modules += sorted(discovered.difference(modules))

    report = [
        "# Fair ablation report",
        "",
        f"- Seeds discovered: {', '.join(map(str, seeds)) or 'none'}",
        f"- Practical-gain threshold: {MIN_PRACTICAL_AP_GAIN:.1f} AP",
        "- Statistical gate: paired 95% CI lower bound > 0",
        "",
        "## AP summary",
        "",
        "| Module | Astyx | TruckScenes | V2X-Radar-V | K-Radar | Macro mean |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for module in modules:
        dataset_means = []
        cells = []
        for dataset in DATASETS:
            samples = [
                values[(module, dataset, seed)]
                for seed in seeds
                if values.get((module, dataset, seed)) is not None
            ]
            if samples:
                mean = statistics.mean(samples)
                std = statistics.stdev(samples) if len(samples) > 1 else 0.0
                dataset_means.append(mean)
                cells.append(f"{mean:.4f} ± {std:.4f} (n={len(samples)})")
            else:
                cells.append("—")
        macro = statistics.mean(dataset_means) if len(dataset_means) == 4 else None
        report.append(
            f"| {module} | {' | '.join(cells)} | {fmt(macro)} |"
        )

    report.extend(
        [
            "",
            "## Sequential paired deltas",
            "",
            "| Step | Dataset | Mean ΔAP | SD | 95% CI lower | n | "
            "All seeds > 0 | ≥1 AP | Pass |",
            "|---|---|---:|---:|---:|---:|:---:|:---:|:---:|",
        ]
    )
    for module in modules:
        if module == "pointpillars":
            continue
        predecessor = PREDECESSOR.get(module)
        if predecessor is None:
            continue
        for dataset in DATASETS:
            deltas = []
            for seed in seeds:
                current = values.get((module, dataset, seed))
                previous = values.get((predecessor, dataset, seed))
                if current is not None and previous is not None:
                    deltas.append(current - previous)
            if not deltas:
                report.append(
                    f"| {predecessor} → {module} | {dataset} | — | — | — | "
                    "0 | — | — | pending |"
                )
                continue
            mean_delta = statistics.mean(deltas)
            std = statistics.stdev(deltas) if len(deltas) > 1 else 0.0
            all_positive = all(delta > 0 for delta in deltas)
            practical = mean_delta >= MIN_PRACTICAL_AP_GAIN
            if len(deltas) >= 3:
                t_critical = T_CRITICAL_975.get(len(deltas) - 1, 1.96)
                ci_lower = mean_delta - t_critical * std / math.sqrt(len(deltas))
                significant = ci_lower > 0
            else:
                ci_lower = None
                significant = False
            passed = all_positive and practical and significant
            report.append(
                f"| {predecessor} → {module} | {dataset} | {mean_delta:+.4f} | "
                f"{std:.4f} | {fmt(ci_lower)} | {len(deltas)} | "
                f"{'yes' if all_positive else 'no'} | "
                f"{'yes' if practical else 'no'} | "
                f"{'pass' if passed else 'fail/pending'} |"
            )

    report_path = result_dir / "fair_ablation_report.md"
    report_path.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(detail_path)
    print(report_path)


if __name__ == "__main__":
    main()
