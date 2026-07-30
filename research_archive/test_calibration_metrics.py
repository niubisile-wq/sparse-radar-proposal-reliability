from __future__ import annotations

import math

import numpy as np

from build_calibration_report import brier_score, expected_calibration_error, pearson_corr


def test_brier_score_perfect_and_imperfect():
    scores = np.array([0.1, 0.9, 0.8, 0.2], dtype=np.float32)
    hits = np.array([0, 1, 1, 0], dtype=np.float32)
    assert math.isclose(brier_score(scores, hits), 0.025, rel_tol=1e-6)


def test_expected_calibration_error_simple_bin():
    scores = np.array([0.1, 0.2, 0.8, 0.9], dtype=np.float32)
    hits = np.array([0, 0, 1, 1], dtype=np.float32)
    ece, bins = expected_calibration_error(scores, hits, bins=2)
    assert math.isclose(ece, 0.15, rel_tol=1e-6)
    assert len(bins) == 2


def test_pearson_corr_monotonic():
    x = np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float32)
    y = np.array([2.0, 4.0, 6.0, 8.0], dtype=np.float32)
    assert math.isclose(pearson_corr(x, y), 1.0, rel_tol=1e-6)
