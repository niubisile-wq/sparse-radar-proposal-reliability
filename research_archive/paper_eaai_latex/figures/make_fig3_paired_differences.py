from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
DATA_PATH = HERE / "fig3_paired_differences.csv"
OUTPUT_STEM = HERE / "fig3_paired_differences"

STRICT = "#087F8C"
HIGH_PERF = "#D55E00"
INK = "#263238"
GRID = "#D8DEE3"
GROUP_SHADE = "#F4F7F8"

mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
        "font.size": 7.2,
        "axes.labelsize": 8,
        "axes.titlesize": 8,
        "axes.linewidth": 0.7,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "legend.fontsize": 7,
        "legend.frameon": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    }
)


def build_figure(data: pd.DataFrame) -> plt.Figure:
    fig = plt.figure(figsize=(7.2, 4.05), facecolor="white")
    grid = fig.add_gridspec(
        1,
        2,
        width_ratios=[4.7, 1.35],
        left=0.145,
        right=0.985,
        bottom=0.14,
        top=0.94,
        wspace=0.08,
    )
    ax = fig.add_subplot(grid[0, 0])
    summary = fig.add_subplot(grid[0, 1])

    n = len(data)
    y = np.arange(n)[::-1]
    strict = data["strict_delta"].to_numpy()
    high = data["high_performance_delta"].to_numpy()

    for group_start in (0, 6):
        top_index = n - 1 - group_start
        ax.axhspan(
            top_index - 2.5,
            top_index + 0.5,
            color=GROUP_SHADE,
            zorder=0,
        )

    for boundary in (2.5, 5.5, 8.5):
        ax.axhline(boundary, color=GRID, lw=0.65, zorder=0)

    ax.axvline(0, color=INK, lw=1.05, zorder=1)
    ax.text(
        0.16,
        n - 0.58,
        "RDAR reference",
        ha="left",
        va="bottom",
        color=INK,
        fontsize=6.4,
        zorder=5,
        bbox={
            "boxstyle": "square,pad=0.16",
            "facecolor": "white",
            "edgecolor": "none",
        },
    )

    ax.hlines(y, strict, high, color="#BCC5CB", lw=0.75, zorder=1)
    strict_scatter = ax.scatter(
        strict,
        y,
        s=28,
        marker="o",
        facecolor=STRICT,
        edgecolor="white",
        linewidth=0.55,
        zorder=3,
        label="Strict route",
    )
    high_scatter = ax.scatter(
        high,
        y,
        s=34,
        marker="D",
        facecolor=HIGH_PERF,
        edgecolor="white",
        linewidth=0.55,
        zorder=3,
        label="High-performance route",
    )

    negative_row = data.index[
        (data["dataset"] == "TruckScenes") & (data["seed"] == 2027)
    ][0]
    negative_y = y[negative_row]
    negative_x = high[negative_row]
    ax.text(
        negative_x,
        negative_y - 0.30,
        "−1.2770 · only negative",
        ha="center",
        va="top",
        fontsize=6.1,
        color=HIGH_PERF,
    )

    labels = [f"{row.dataset}  {row.seed}" for row in data.itertuples()]
    ax.set_yticks(y, labels)
    ax.set_ylim(-0.7, n - 0.05)
    ax.set_xlim(-1.75, 8.75)
    ax.set_xticks([-1, 0, 1, 2, 4, 6, 8])
    ax.set_xlabel(r"$\Delta$AP$_{R40}$ relative to RDAR (3D IoU = 0.50)")
    ax.grid(axis="x", color=GRID, lw=0.55, linestyle="-", zorder=0)
    ax.tick_params(axis="y", length=0, pad=5)
    ax.tick_params(axis="x", length=3, color=INK)
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_color(INK)
    ax.legend(
        handles=[high_scatter, strict_scatter],
        loc="lower left",
        bbox_to_anchor=(0, 1.005),
        ncol=2,
        columnspacing=1.4,
        handletextpad=0.45,
        borderaxespad=0,
    )

    summary.set_xlim(0, 1)
    summary.set_ylim(0, 1)
    summary.axis("off")
    summary.axvline(0.02, color=GRID, lw=0.8, ymin=0.02, ymax=0.98)

    summary.text(
        0.12,
        0.94,
        "Paired summary",
        ha="left",
        va="top",
        fontsize=8,
        fontweight="bold",
        color=INK,
    )
    summary.text(
        0.12,
        0.84,
        "STRICT ROUTE",
        ha="left",
        va="top",
        fontsize=6.7,
        fontweight="bold",
        color=STRICT,
    )
    summary.text(
        0.12,
        0.78,
        "12/12 positive",
        ha="left",
        va="top",
        fontsize=9.2,
        fontweight="bold",
        color=STRICT,
    )
    summary.text(
        0.12,
        0.69,
        "Mean  +0.9726\n"
        "Median  +0.8493\n"
        "95% bootstrap CI\n"
        "[+0.6468, +1.3536]\n"
        "Range\n"
        "[+0.1718, +2.6060]",
        ha="left",
        va="top",
        fontsize=6.9,
        linespacing=1.42,
        color=INK,
    )

    summary.plot([0.12, 0.90], [0.39, 0.39], color=GRID, lw=0.8)
    summary.text(
        0.12,
        0.33,
        "HIGH-PERFORMANCE",
        ha="left",
        va="top",
        fontsize=6.7,
        fontweight="bold",
        color=HIGH_PERF,
    )
    summary.text(
        0.12,
        0.27,
        "11/12 positive",
        ha="left",
        va="top",
        fontsize=8.6,
        fontweight="bold",
        color=HIGH_PERF,
    )
    summary.text(
        0.12,
        0.18,
        "Mean  +3.7662\n"
        "One negative cell\n"
        "(TruckScenes, 2027)",
        ha="left",
        va="top",
        fontsize=6.9,
        linespacing=1.42,
        color=INK,
    )

    return fig


def main() -> None:
    data = pd.read_csv(DATA_PATH)
    required = {
        "dataset",
        "seed",
        "strict_delta",
        "high_performance_delta",
    }
    if set(data.columns) != required:
        raise ValueError(f"Unexpected columns: {list(data.columns)}")
    if len(data) != 12:
        raise ValueError(f"Expected 12 paired rows, found {len(data)}")
    if int((data["strict_delta"] > 0).sum()) != 12:
        raise ValueError("Strict route must contain 12 positive differences")
    if int((data["high_performance_delta"] > 0).sum()) != 11:
        raise ValueError("High-performance route must contain 11 positive differences")

    fig = build_figure(data)
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
