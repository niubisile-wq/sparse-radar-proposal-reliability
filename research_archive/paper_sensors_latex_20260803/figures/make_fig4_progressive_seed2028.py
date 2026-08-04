from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
DATA_PATH = HERE / "fig4_progressive_seed2028.csv"
OUTPUT_STEM = HERE / "fig4_progressive_seed2028"

COLORS = {
    "Astyx": "#3A7CA5",
    "TruckScenes": "#9A6A3A",
    "V2X-Radar-V": "#4D927C",
    "K-Radar": "#C56B6B",
    "Macro": "#202A2F",
}
ACCENT = "#D55E00"
INK = "#263238"
GRID = "#D9E0E4"

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
        "legend.fontsize": 6.8,
        "legend.frameon": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    }
)


def build_figure(data: pd.DataFrame) -> plt.Figure:
    fig = plt.figure(figsize=(7.2, 3.25), facecolor="white")
    grid = fig.add_gridspec(
        1,
        2,
        width_ratios=[3.5, 1.25],
        left=0.075,
        right=0.985,
        bottom=0.18,
        top=0.84,
        wspace=0.23,
    )
    ax = fig.add_subplot(grid[0, 0])
    delta_ax = fig.add_subplot(grid[0, 1])

    x = np.arange(len(data))
    stages = data["stage_short"].tolist()
    series = ["Astyx", "TruckScenes", "V2X-Radar-V", "K-Radar", "Macro"]

    for name in series:
        is_macro = name == "Macro"
        ax.plot(
            x,
            data[name],
            color=COLORS[name],
            lw=2.25 if is_macro else 1.35,
            marker="o",
            ms=5.4 if is_macro else 4.2,
            markerfacecolor="white" if is_macro else COLORS[name],
            markeredgecolor=COLORS[name],
            markeredgewidth=1.1 if is_macro else 0.5,
            zorder=4 if is_macro else 2,
            label=name,
        )

    for xi, value in zip(x, data["Macro"]):
        ax.annotate(
            f"{value:.4f}",
            (xi, value),
            xytext=(0, 7),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=6.2,
            fontweight="bold",
            color=COLORS["Macro"],
            zorder=6,
        )

    ax.set_xticks(x, stages)
    ax.set_ylabel(r"AP$_{R40}$ at 3D IoU = 0.50")
    ax.set_xlim(-0.18, len(data) - 0.82)
    ax.set_ylim(12.5, 62.2)
    ax.set_yticks([15, 25, 35, 45, 55])
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.tick_params(axis="x", length=0, pad=6)
    ax.tick_params(axis="y", length=3, color=INK)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(INK)
    ax.spines["bottom"].set_color(INK)
    ax.text(
        -0.12,
        1.03,
        "a  Dataset and macro trajectories",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=8,
        fontweight="bold",
        color=INK,
    )
    ax.legend(
        loc="lower left",
        bbox_to_anchor=(0.0, 1.075),
        ncol=5,
        columnspacing=1.0,
        handlelength=1.7,
        handletextpad=0.4,
        borderaxespad=0,
    )

    delta = data.loc[1:, "stepwise_macro_delta"].to_numpy()
    delta_labels = data.loc[1:, "stage_short"].tolist()
    bars = delta_ax.bar(
        np.arange(len(delta)),
        delta,
        width=0.64,
        color=[COLORS["Astyx"], "#AEB9BF", ACCENT, COLORS["V2X-Radar-V"]],
        edgecolor="white",
        linewidth=0.7,
        zorder=3,
    )
    for bar, value in zip(bars, delta):
        offset = 0.09 if value < 0.1 else 0.06
        delta_ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + offset,
            f"+{value:.4f}",
            ha="center",
            va="bottom",
            fontsize=6.4,
            fontweight="bold" if value == delta.max() else "normal",
            color=INK,
        )

    delta_ax.axhline(0, color=INK, lw=0.8)
    delta_ax.set_xticks(np.arange(len(delta)), delta_labels, rotation=28, ha="right")
    delta_ax.set_ylabel(r"Stepwise $\Delta$Macro AP")
    delta_ax.set_ylim(0, 3.9)
    delta_ax.set_yticks([0, 1, 2, 3])
    delta_ax.grid(axis="y", color=GRID, lw=0.6, zorder=0)
    delta_ax.tick_params(axis="x", length=0, pad=5)
    delta_ax.tick_params(axis="y", length=3, color=INK)
    delta_ax.spines["top"].set_visible(False)
    delta_ax.spines["right"].set_visible(False)
    delta_ax.spines["left"].set_color(INK)
    delta_ax.spines["bottom"].set_color(INK)
    delta_ax.text(
        -0.05,
        1.03,
        "b  Incremental macro gain",
        transform=delta_ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=8,
        fontweight="bold",
        color=INK,
    )
    fig.text(
        0.075,
        0.965,
        "Seed 2028 construction analysis",
        ha="left",
        va="top",
        fontsize=8.5,
        fontweight="bold",
        color=INK,
    )
    fig.text(
        0.985,
        0.965,
        "Single-seed evidence; not a three-seed monotonicity test",
        ha="right",
        va="top",
        fontsize=6.8,
        color="#66747C",
    )
    return fig


def main() -> None:
    data = pd.read_csv(DATA_PATH)
    expected = {
        "stage",
        "stage_short",
        "Astyx",
        "TruckScenes",
        "V2X-Radar-V",
        "K-Radar",
        "Macro",
        "stepwise_macro_delta",
    }
    if set(data.columns) != expected:
        raise ValueError(f"Unexpected columns: {list(data.columns)}")
    if len(data) != 5:
        raise ValueError(f"Expected five progressive stages, found {len(data)}")

    recomputed = data[["Astyx", "TruckScenes", "V2X-Radar-V", "K-Radar"]].mean(
        axis=1
    )
    if not np.allclose(recomputed, data["Macro"], atol=5e-5):
        raise ValueError("Macro values do not match the four-dataset means")
    recomputed_delta = data["Macro"].diff().iloc[1:]
    if not np.allclose(
        recomputed_delta,
        data["stepwise_macro_delta"].iloc[1:],
        atol=5e-5,
    ):
        raise ValueError("Stepwise macro deltas do not match the macro trajectory")

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
