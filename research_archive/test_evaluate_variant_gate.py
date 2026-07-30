import json
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).with_name("evaluate_variant_gate.py")
REFERENCE = {
    "astyx": {2026: 32.7281, 2027: 31.4220, 2028: 34.3540},
    "truckscenes": {2026: 15.4127, 2027: 18.3845, 2028: 15.3041},
    "v2xradarv": {2026: 40.7802, 2027: 42.9899, 2028: 41.3385},
    "kradar": {2026: 51.3450, 2027: 48.1767, 2028: 52.0271},
}


def write_log(root, variant, dataset, seed, delta):
    log_dir = root / "logs" / "fair_ablation"
    log_dir.mkdir(parents=True, exist_ok=True)
    ap = REFERENCE[dataset][seed] + delta
    (log_dir / f"eval_rdar_{variant}_{dataset}_seed{seed}_gpu0.log").write_text(
        f"Car radar AP_R40@3D IoU 0.50: {ap:.4f}\nEvaluation done.\n",
        encoding="utf-8",
    )


with tempfile.TemporaryDirectory() as temporary_directory:
    root = Path(temporary_directory)
    for dataset in REFERENCE:
        write_log(root, "passing", dataset, 2026, 1.2)
        write_log(root, "passing", dataset, 2027, 1.3)
        write_log(root, "passing", dataset, 2028, 1.1)
    passing = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "passing",
            "--root",
            str(root),
            "--mode",
            "formal",
        ],
        check=False,
    )
    assert passing.returncode == 0
    report = json.loads(
        (root / "results" / "passing_vs_rdar_formal_gate.json").read_text(
            encoding="utf-8"
        )
    )
    assert report["complete"] is True
    assert report["passed"] is True

    for dataset in REFERENCE:
        write_log(root, "failing", dataset, 2028, 1.2)
    write_log(root, "failing", "truckscenes", 2028, -0.1)
    failing = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "failing",
            "--root",
            str(root),
            "--mode",
            "screen",
        ],
        check=False,
    )
    assert failing.returncode == 1
    report = json.loads(
        (root / "results" / "failing_vs_rdar_screen_gate.json").read_text(
            encoding="utf-8"
        )
    )
    assert report["complete"] is True
    assert report["passed"] is False

    for dataset in REFERENCE:
        write_log(root, "incremental", dataset, 2028, 2.3)
    incremental = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "incremental",
            "--reference-variant",
            "passing",
            "--root",
            str(root),
            "--mode",
            "screen",
        ],
        check=False,
    )
    assert incremental.returncode == 0
    report = json.loads(
        (
            root
            / "results"
            / "incremental_vs_passing_screen_gate.json"
        ).read_text(encoding="utf-8")
    )
    assert report["complete"] is True
    assert report["passed"] is True

print("variant gate tests passed")
