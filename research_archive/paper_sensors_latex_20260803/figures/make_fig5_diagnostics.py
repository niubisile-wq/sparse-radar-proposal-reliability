from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
ECE_PATH = HERE / "fig5_ece_seed2028.csv"
DROPOUT_PATH = HERE / "fig5_point_dropout.csv"
VOTING_PATH = HERE / "fig5_voting_sensitivity.csv"
OUTPUT_STEM = HERE / "fig5_diagnostics"

RDAR = "#5F6B73"
QUALITY = "#3A7CA5"
HIGH_PERF = "#D55E00"
STRICT = "#087F8C"
INK = "#263238"
GRID = "#D9E0E4"
MISSING = "#ECEFF1"
HEAT = LinearSegmentedColormap.from_list(
    "muted_blue",
    ["#EFF5F7", "#A9CAD3", "#3D8596"],
)
COUNT = LinearSegmentedColormap.from_list(
    "reliability_count",
    ["#F4E6DC", "#E5B58E", "#78B5AE", "#087F8C"],
)

mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
        "font.size": 7.1,
        "axes.labelsize": 7.8,
        "axes.titlesize": 8,
        "axes.linewidth": 0.7,
        "xtick.labelsize": 6.8,
        "ytick.labelsize": 6.8,
        "legend.fontsize": 6.6,
        "legend.frameon": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    }
)


def panel_title(
    ax: plt.Axes,
    label: str,
    title: str,
    y: float = 1.06,
) -> None:
    ax.text(
        -0.04,
        y,
        f"{label}  {title}",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=8,
        fontweight="bold",
        color=INK,
    )


def matrix_from_voting(
    voting: pd.DataFrame,
    value_column: str,
    ious: list[float],
    strengths: list[float],
) -> np.ndarray:
    matrix = np.full((len(ious), len(strengths)), np.nan)
    for row in voting.itertuples():
        i = ious.index(round(float(row.vote_iou), 2))
        j = strengths.index(round(float(row.strength), 2))
        value = getattr(row, value_column)
        if pd.notna(value):
            matrix[i, j] = float(value)
    return matrix


def draw_heatmap(
    ax: plt.Axes,
    matrix: np.ndarray,
    ious: list[float],
    strengths: list[float],
    cmap: LinearSegmentedColormap,
    vmin: float,
    vmax: float,
    value_format: str,
    selected: tuple[float, float],
) -> None:
    masked = np.ma.masked_invalid(matrix)
    cmap = cmap.copy()
    cmap.set_bad(MISSING)
    ax.imshow(masked, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = matrix[i, j]
            if np.isnan(value):
                text_value = "NA"
                text_color = "#7B858B"
            else:
                text_value = value_format.format(value)
                normalized = (value - vmin) / max(vmax - vmin, 1e-12)
                text_color = "white" if normalized > 0.67 else INK
            ax.text(
                j,
                i,
                text_value,
                ha="center",
                va="center",
                fontsize=6.5,
                fontweight="bold" if not np.isnan(value) and value >= vmax else "normal",
                color=text_color,
            )

    selected_i = ious.index(selected[0])
    selected_j = strengths.index(selected[1])
    ax.add_patch(
        Rectangle(
            (selected_j - 0.48, selected_i - 0.48),
            0.96,
            0.96,
            fill=False,
            edgecolor=HIGH_PERF,
            linewidth=1.8,
        )
    )
    ax.set_xticks(np.arange(len(strengths)), [f"{x:.2f}" for x in strengths])
    ax.set_yticks(np.arange(len(ious)), [f"{x:.2f}" for x in ious])
    ax.set_xlabel(r"Voting strength $\lambda$")
    ax.set_ylabel(r"Voting IoU $\tau_v$")
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)


def build_figure(
    ece: pd.DataFrame,
    dropout: pd.DataFrame,
    voting: pd.DataFrame,
) -> plt.Figure:
    fig, axes = plt.subplots(
        2,
        2,
        figsize=(7.2, 5.05),
        facecolor="white",
        gridspec_kw={
            "left": 0.09,
            "right": 0.985,
            "bottom": 0.09,
            "top": 0.92,
            "hspace": 0.48,
            "wspace": 0.28,
        },
    )
    ax_a, ax_b, ax_c, ax_d = axes.flat

    methods = ["RDAR", "Quality-aligned", "High-performance"]
    colors = [RDAR, QUALITY, HIGH_PERF]
    x = np.arange(len(ece))
    width = 0.23
    for idx, (method, color) in enumerate(zip(methods, colors)):
        offset = (idx - 1) * width
        ax_a.bar(
            x + offset,
            ece[method],
            width=width,
            color=color,
            edgecolor="white",
            linewidth=0.5,
            label=method,
            zorder=3,
        )
    ax_a.set_xticks(x, ["Astyx", "TruckScenes", "V2X-Radar-V", "K-Radar"])
    ax_a.set_ylabel("Expected calibration error")
    ax_a.set_ylim(0, 0.72)
    ax_a.set_yticks([0, 0.2, 0.4, 0.6])
    ax_a.grid(axis="y", color=GRID, lw=0.6, zorder=0)
    ax_a.spines["top"].set_visible(False)
    ax_a.spines["right"].set_visible(False)
    ax_a.legend(
        loc="lower left",
        bbox_to_anchor=(0, 1.01),
        ncol=3,
        columnspacing=0.9,
        handlelength=1.1,
        handletextpad=0.35,
        borderaxespad=0,
    )
    panel_title(ax_a, "a", "Confidence calibration (seed 2028)", y=1.14)

    for method, color, marker in (
        ("RDAR", RDAR, "o"),
        ("High-performance", HIGH_PERF, "D"),
    ):
        ax_b.plot(
            dropout["drop_rate"],
            dropout[method],
            color=color,
            lw=1.7,
            marker=marker,
            ms=4.8,
            markeredgecolor="white",
            markeredgewidth=0.5,
            label=method,
            zorder=3,
        )
    ax_b.fill_between(
        dropout["drop_rate"],
        dropout["RDAR"],
        dropout["High-performance"],
        color="#F2D8C7",
        alpha=0.55,
        zorder=1,
    )
    ax_b.set_xticks([0, 10, 20, 30], ["Clean", "10%", "20%", "30%"])
    ax_b.set_ylabel("Macro AP")
    ax_b.set_ylim(30.5, 40.6)
    ax_b.grid(axis="y", color=GRID, lw=0.6, zorder=0)
    ax_b.spines["top"].set_visible(False)
    ax_b.spines["right"].set_visible(False)
    ax_b.legend(
        loc="lower left",
        bbox_to_anchor=(0, 1.01),
        ncol=2,
        columnspacing=1.1,
        handlelength=1.4,
        handletextpad=0.4,
        borderaxespad=0,
    )
    panel_title(ax_b, "b", "Deterministic point dropout", y=1.14)

    ious = [0.22, 0.24, 0.25, 0.26, 0.28]
    strengths = [0.35, 0.40, 0.45, 0.50]
    macro_matrix = matrix_from_voting(voting, "macro_ap", ious, strengths)
    count_matrix = matrix_from_voting(voting, "positive_count", ious, strengths)
    selected = (0.24, 0.40)

    draw_heatmap(
        ax_c,
        macro_matrix,
        ious,
        strengths,
        HEAT,
        35.75,
        36.34,
        "{:.2f}",
        selected,
    )
    panel_title(ax_c, "c", "Voting sensitivity: Macro AP")
    ax_c.text(
        0.98,
        1.04,
        "Orange border: selected",
        transform=ax_c.transAxes,
        ha="right",
        va="bottom",
        fontsize=6.3,
        color=HIGH_PERF,
    )

    draw_heatmap(
        ax_d,
        count_matrix,
        ious,
        strengths,
        COUNT,
        7,
        12,
        "{:.0f}/12",
        selected,
    )
    panel_title(ax_d, "d", "Positive dataset–seed pairs")
    ax_d.text(
        0.98,
        1.04,
        "Complete grid: 20 settings",
        transform=ax_d.transAxes,
        ha="right",
        va="bottom",
        fontsize=6.3,
        color="#66747C",
    )
    return fig


def main() -> None:
    ece = pd.read_csv(ECE_PATH)
    dropout = pd.read_csv(DROPOUT_PATH)
    voting = pd.read_csv(VOTING_PATH)

    if len(ece) != 4 or len(dropout) != 4 or len(voting) != 20:
        raise ValueError("Unexpected diagnostic source-data dimensions")
    if int(voting["macro_ap"].notna().sum()) != 20:
        raise ValueError("Expected 20 traceable voting settings")
    selected = voting[
        (voting["vote_iou"] == 0.24) & (voting["strength"] == 0.40)
    ].iloc[0]
    if (
        abs(selected["macro_ap"] - 36.3278) > 5e-5
        or int(selected["positive_count"]) != 12
    ):
        raise ValueError("Selected voting setting does not match the frozen result")
    if not (
        np.all(ece["Quality-aligned"] < ece["RDAR"])
        and np.all(ece["High-performance"] < ece["RDAR"])
    ):
        raise ValueError("ECE direction does not match the frozen diagnostic claim")

    fig = build_figure(ece, dropout, voting)
    fig.savefig(OUTPUT_STEM.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(OUTPUT_STEM.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(
        OUTPUT_STEM.with_suffix(".png"),
        dpi=600,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
