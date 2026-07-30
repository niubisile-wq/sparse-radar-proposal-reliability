#!/usr/bin/env python3
import csv
import math
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path


LOG_PATTERN = re.compile(
    r"fair_(?P<module>[a-z0-9_]+)_(?P<dataset>astyx|truckscenes|v2xradarv|kradar)"
    r"_seed(?P<seed>\d+)_gpu\d+\.log$"
)
AP_PATTERN = re.compile(r"AP_R40@3D IoU 0\.50:\s*([0-9.]+)")
ERROR_PATTERN = re.compile(
    r"Traceback|CUDA out of memory|Killed|RuntimeError|FATAL", re.IGNORECASE
)
COMPLETE_PATTERN = re.compile(r"Evaluation done")
DATASETS = ("astyx", "truckscenes", "v2xradarv", "kradar")
PREDECESSOR = {
    "bevgate": "pointpillars",
    "stable_bevgate": "pointpillars",
    "rccg": "pointpillars",
    "dapg2": "pointpillars",
    "msbc2": "pointpillars",
    "range2": "pointpillars",
    "dapg3": "pointpillars",
    "msbc3": "pointpillars",
    "range3": "pointpillars",
    "sbd05": "pointpillars",
    "sbd10": "pointpillars",
    "sbd20": "pointpillars",
    "swa5": "pointpillars",
    "rcnms": "pointpillars",
    "taac_rcnms": "rcnms",
    "rdar": "rcnms",
    "stable_bevgate_dapg": "stable_bevgate",
    "stable_bevgate_dapg_msbc": "stable_bevgate_dapg",
    "stable_four_modules": "stable_bevgate_dapg_msbc",
    "bevgate_dapg": "bevgate",
    "bevgate_dapg_msbc": "bevgate_dapg",
    "four_modules": "bevgate_dapg_msbc",
}
T_CRITICAL_975 = {
    1: 12.706,
    2: 4.303,
    3: 3.182,
    4: 2.776,
    5: 2.571,
    6: 2.447,
    7: 2.365,
    8: 2.306,
    9: 2.262,
}
MIN_PRACTICAL_AP_GAIN = 1.0


def parse_log(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    ap_values = AP_PATTERN.findall(text)
    return {
        "ap": float(ap_values[-1]) if ap_values else None,
        "complete": bool(COMPLETE_PATTERN.search(text)),
        "error": bool(ERROR_PATTERN.search(text)),
    }


def main():
    log_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "logs/fair_ablation")
    rows = []
    by_key = {}
    for path in sorted(log_dir.glob("fair_*_seed*_gpu*.log")):
        match = LOG_PATTERN.match(path.name)
        if not match:
            continue
        parsed = parse_log(path)
        row = {
            **match.groupdict(),
            **parsed,
            "log": str(path),
        }
        row["seed"] = int(row["seed"])
        rows.append(row)
        by_key[(row["module"], row["dataset"], row["seed"])] = row

    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=("module", "dataset", "seed", "ap", "complete", "error", "log"),
    )
    writer.writeheader()
    writer.writerows(rows)

    print("\n# paired sequential module deltas")
    module_deltas = defaultdict(list)
    modules = sorted({row["module"] for row in rows if row["module"] != "pointpillars"})
    seeds = sorted({row["seed"] for row in rows})
    for module in modules:
        predecessor = PREDECESSOR.get(module, "pointpillars")
        print(f"\n[{predecessor} -> {module}]")
        all_positive = True
        all_significant = True
        complete_pairs = 0
        for dataset in DATASETS:
            deltas = []
            for seed in seeds:
                baseline = by_key.get((predecessor, dataset, seed))
                candidate = by_key.get((module, dataset, seed))
                if not baseline or not candidate:
                    continue
                if (
                    baseline["ap"] is None
                    or candidate["ap"] is None
                    or baseline["error"]
                    or candidate["error"]
                ):
                    continue
                delta = candidate["ap"] - baseline["ap"]
                deltas.append(delta)
                module_deltas[module].append(delta)
                complete_pairs += 1
            if not deltas:
                all_positive = False
                all_significant = False
                print(f"{dataset}: pending")
                continue
            mean_delta = statistics.mean(deltas)
            seedwise_positive = all(delta > 0 for delta in deltas)
            all_positive = all_positive and seedwise_positive
            std = statistics.stdev(deltas) if len(deltas) > 1 else 0.0
            if len(deltas) >= 3:
                degrees_freedom = len(deltas) - 1
                t_critical = T_CRITICAL_975.get(degrees_freedom, 1.96)
                ci_lower = mean_delta - t_critical * std / math.sqrt(len(deltas))
                statistically_significant = ci_lower > 0.0
            else:
                ci_lower = float("-inf")
                statistically_significant = False
            practically_significant = mean_delta >= MIN_PRACTICAL_AP_GAIN
            dataset_pass = (
                seedwise_positive
                and statistically_significant
                and practically_significant
            )
            all_significant = all_significant and dataset_pass
            print(
                f"{dataset}: mean_delta={mean_delta:+.4f}, "
                f"std={std:.4f}, n={len(deltas)}, "
                f"ci95_lower={ci_lower:+.4f}, "
                f"all_positive={seedwise_positive}, "
                f"practical_gain={practically_significant}, "
                f"pass={dataset_pass}"
            )
        print(
            f"gate_all_dataset_seed_pairs_positive={all_positive} "
            f"gate_all_datasets_significant={all_significant} "
            f"complete_pairs={complete_pairs}"
        )


if __name__ == "__main__":
    main()
