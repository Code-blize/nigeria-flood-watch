
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# CONFIGURATION
# ============================================================

INPUT = Path(
    "data/processed/glofas/"
    "glofas_2015_2020_candidate_timeseries.csv"
)

OUTPUT = Path("data/processed/glofas")
FIGURES = Path("data/figures")

OUTPUT.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)

CELLS = [
    "cell_4", "cell_11", "cell_14",
    "cell_18", "cell_19", "cell_25", "cell_32"
]

GROUPS = {
    "Group_A": ["cell_4", "cell_11", "cell_18"],
    "Group_B": ["cell_14", "cell_19"],
    "Group_C": ["cell_25", "cell_32"]
}

# ============================================================
# LOAD AND VALIDATE
# ============================================================

df = pd.read_csv(INPUT, parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)

if df["date"].duplicated().any():
    raise ValueError("Duplicate dates found.")

if df[CELLS].isna().any().any():
    raise ValueError("Missing discharge values found.")

if len(df) != 2192:
    raise ValueError(
        f"Expected 2192 rows, found {len(df)}"
    )

df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month

# Meteorological seasons used only as calendar groupings.
# They are not a locally validated flood-season definition.
def get_season(month):
    if month in [12, 1, 2]:
        return "DJF"
    elif month in [3, 4, 5]:
        return "MAM"
    elif month in [6, 7, 8]:
        return "JJA"
    return "SON"

df["season"] = df["month"].apply(get_season)

# ============================================================
# 1. FULL-PERIOD CORRELATION
# ============================================================

full_corr = df[CELLS].corr(method="pearson")

full_corr.to_csv(
    OUTPUT / "glofas_2015_2020_correlation.csv"
)

print("\nFULL-PERIOD CORRELATION")
print("=" * 65)
print(full_corr.round(4))

# ============================================================
# 2. ANNUAL CORRELATION
# ============================================================

annual_results = []

for year, group in df.groupby("year"):
    corr = group[CELLS].corr(method="pearson")

    for cell_a in CELLS:
        for cell_b in CELLS:
            if cell_a < cell_b:
                annual_results.append({
                    "year": year,
                    "cell_a": cell_a,
                    "cell_b": cell_b,
                    "correlation": corr.loc[
                        cell_a, cell_b
                    ]
                })

annual_corr = pd.DataFrame(annual_results)

annual_corr.to_csv(
    OUTPUT / "glofas_annual_correlations.csv",
    index=False
)

# ============================================================
# 3. SEASONAL CORRELATION
# ============================================================

seasonal_results = []

for (year, season), group in df.groupby(
    ["year", "season"]
):
    if len(group) < 30:
        continue

    corr = group[CELLS].corr(method="pearson")

    for cell_a in CELLS:
        for cell_b in CELLS:
            if cell_a < cell_b:
                seasonal_results.append({
                    "year": year,
                    "season": season,
                    "cell_a": cell_a,
                    "cell_b": cell_b,
                    "correlation": corr.loc[
                        cell_a, cell_b
                    ]
                })

seasonal_corr = pd.DataFrame(seasonal_results)

seasonal_corr.to_csv(
    OUTPUT / "glofas_seasonal_correlations.csv",
    index=False
)

# ============================================================
# 4. DESCRIPTIVE STATISTICS
# ============================================================

statistics = df[CELLS].agg([
    "count", "mean", "median", "std",
    "min", "max"
]).T

statistics["coefficient_of_variation"] = (
    statistics["std"] / statistics["mean"]
)

statistics.to_csv(
    OUTPUT / "glofas_2015_2020_statistics.csv"
)

print("\nDISCHARGE STATISTICS")
print("=" * 65)
print(statistics.round(3))

# ============================================================
# 5. ANNUAL PEAK DISCHARGE
# ============================================================

annual_peaks = []

for (year, cell), group in df.melt(
    id_vars=["date", "year"],
    value_vars=CELLS,
    var_name="cell",
    value_name="discharge"
).groupby(["year", "cell"]):

    peak_index = group["discharge"].idxmax()
    peak = group.loc[peak_index]

    annual_peaks.append({
        "year": year,
        "cell": cell,
        "peak_date": peak["date"],
        "peak_discharge_m3_s": peak["discharge"]
    })

peaks = pd.DataFrame(annual_peaks)

peaks.to_csv(
    OUTPUT / "glofas_annual_peak_discharge.csv",
    index=False
)

# ============================================================
# 6. GROUP-LEVEL TIME SERIES
# ============================================================

for group_name, cells in GROUPS.items():
    df[group_name] = df[cells].mean(axis=1)

group_columns = list(GROUPS.keys())

df[
    ["date", "year", "season"] + group_columns
].to_csv(
    OUTPUT / "glofas_group_mean_timeseries.csv",
    index=False
)

# ============================================================
# 7. FULL-PERIOD TIME SERIES FIGURE
# ============================================================

fig, ax = plt.subplots(figsize=(15, 6))

for cell in CELLS:
    ax.plot(
        df["date"],
        df[cell],
        label=cell,
        linewidth=0.8,
        alpha=0.8
    )

ax.set_title(
    "GloFAS Daily Discharge: Candidate Cells (2015–2020)"
)
ax.set_xlabel("Date")
ax.set_ylabel("Discharge (m³/s)")
ax.legend(ncol=4)
ax.grid(alpha=0.25)

fig.tight_layout()
fig.savefig(
    FIGURES / "glofas_2015_2020_timeseries.png",
    dpi=200
)
plt.close(fig)

# ============================================================
# 8. CORRELATION HEATMAP
# ============================================================

fig, ax = plt.subplots(figsize=(9, 7))

im = ax.imshow(
    full_corr.values,
    vmin=-1,
    vmax=1,
    cmap="coolwarm"
)

ax.set_xticks(range(len(CELLS)))
ax.set_yticks(range(len(CELLS)))
ax.set_xticklabels(CELLS, rotation=45)
ax.set_yticklabels(CELLS)

for i in range(len(CELLS)):
    for j in range(len(CELLS)):
        ax.text(
            j, i,
            f"{full_corr.iloc[i, j]:.2f}",
            ha="center",
            va="center",
            fontsize=8
        )

ax.set_title(
    "GloFAS Candidate Cell Correlation (2015–2020)"
)

fig.colorbar(im, ax=ax, label="Pearson correlation")
fig.tight_layout()

fig.savefig(
    FIGURES / "glofas_2015_2020_correlation.png",
    dpi=200
)
plt.close(fig)

# ============================================================
# 9. GROUP MEAN TIME SERIES
# ============================================================

fig, ax = plt.subplots(figsize=(15, 6))

for group in group_columns:
    ax.plot(
        df["date"],
        df[group],
        label=group,
        linewidth=1
    )

ax.set_title(
    "GloFAS Candidate Group Mean Discharge (2015–2020)"
)
ax.set_xlabel("Date")
ax.set_ylabel("Mean grid-cell discharge (m³/s)")
ax.legend()
ax.grid(alpha=0.25)

fig.tight_layout()
fig.savefig(
    FIGURES / "glofas_2015_2020_group_timeseries.png",
    dpi=200
)
plt.close(fig)

# ============================================================
# 10. GROUP CORRELATION STABILITY SUMMARY
# ============================================================

pairs = [
    ("cell_4", "cell_11"),
    ("cell_4", "cell_18"),
    ("cell_11", "cell_18"),
    ("cell_14", "cell_19"),
    ("cell_25", "cell_32")
]

stability = []

for cell_a, cell_b in pairs:
    values = []

    for year, group in df.groupby("year"):
        correlation = group[cell_a].corr(group[cell_b])

        values.append({
            "year": year,
            "correlation": correlation
        })

    correlations = [item["correlation"] for item in values]

    stability.append({
        "cell_a": cell_a,
        "cell_b": cell_b,
        "mean_annual_correlation": np.mean(correlations),
        "minimum_annual_correlation": np.min(correlations),
        "maximum_annual_correlation": np.max(correlations),
        "std_annual_correlation": np.std(correlations)
    })

stability_df = pd.DataFrame(stability)

stability_df.to_csv(
    OUTPUT / "glofas_group_correlation_stability.csv",
    index=False
)

print("\nGROUP CORRELATION STABILITY")
print("=" * 65)
print(stability_df.round(4).to_string(index=False))

print("\nANALYSIS COMPLETED SUCCESSFULLY.")
print("Processed records:", len(df))
print("Output directory:", OUTPUT)
print("Figure directory:", FIGURES)
