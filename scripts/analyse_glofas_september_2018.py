
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# 1. PATHS
# --------------------------------------------------

input_file = Path(
    "data/processed/glofas/"
    "glofas_september_2018_candidate_timeseries.csv"
)

output_dir = Path("data/processed/glofas")
figure_dir = Path("data/figures")

figure_dir.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

df = pd.read_csv(input_file, parse_dates=["date"])

cells = [
    "cell_4",
    "cell_11",
    "cell_14",
    "cell_18",
    "cell_19",
    "cell_25",
    "cell_32",
]

# --------------------------------------------------
# 3. CORRELATION ANALYSIS
# --------------------------------------------------

correlation = df[cells].corr(method="pearson")

print("=" * 60)
print("GloFAS SEPTEMBER 2018 CORRELATION ANALYSIS")
print("=" * 60)

print("\nCORRELATION MATRIX")
print(correlation.round(4).to_string())

correlation.to_csv(
    output_dir / "glofas_september_2018_correlation.csv"
)

# --------------------------------------------------
# 4. TIME SERIES CHART
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(13, 7))

for cell in cells:
    ax.plot(
        df["date"],
        df[cell],
        marker="o",
        markersize=3,
        linewidth=1.5,
        label=cell
    )

ax.set_title(
    "GloFAS Daily River Discharge\n"
    "Lokoja Candidate Grid Cells | September 2018"
)

ax.set_xlabel("Date")
ax.set_ylabel("Discharge (m³/s)")
ax.grid(alpha=0.3)
ax.legend(title="Grid cell")

fig.autofmt_xdate()
plt.tight_layout()

plt.savefig(
    figure_dir / "glofas_september_2018_timeseries.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# --------------------------------------------------
# 5. CORRELATION HEATMAP
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(9, 7))

image = ax.imshow(
    correlation.values,
    vmin=-1,
    vmax=1,
    cmap="coolwarm"
)

ax.set_xticks(range(len(cells)))
ax.set_yticks(range(len(cells)))

ax.set_xticklabels(cells)
ax.set_yticklabels(cells)

for i in range(len(cells)):
    for j in range(len(cells)):
        ax.text(
            j,
            i,
            f"{correlation.iloc[i, j]:.2f}",
            ha="center",
            va="center"
        )

ax.set_title(
    "Correlation Between GloFAS Candidate Cells\n"
    "September 2018"
)

fig.colorbar(image, ax=ax, label="Pearson correlation")

plt.tight_layout()

plt.savefig(
    figure_dir / "glofas_september_2018_correlation.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# --------------------------------------------------
# 6. DAILY CHANGE
# --------------------------------------------------

daily_change = df[cells].pct_change() * 100

daily_change.insert(0, "date", df["date"])

daily_change.to_csv(
    output_dir / "glofas_september_2018_daily_change.csv",
    index=False
)

# --------------------------------------------------
# 7. FINAL REPORT
# --------------------------------------------------

print("\nOUTPUTS CREATED")
print(
    figure_dir / "glofas_september_2018_timeseries.png"
)
print(
    figure_dir / "glofas_september_2018_correlation.png"
)
print(
    output_dir / "glofas_september_2018_daily_change.csv"
)

print("\nAnalysis completed successfully.")