
from pathlib import Path
import pandas as pd
import numpy as np

INPUT = Path(
    "data/processed/glofas/"
    "glofas_2015_2020_candidate_timeseries.csv"
)

OUTPUT = Path("data/processed/glofas")
OUTPUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT)

groups = {
    "Group_A": ["cell_4", "cell_11", "cell_18"],
    "Group_B": ["cell_14", "cell_19"],
    "Group_C": ["cell_25", "cell_32"]
}

results = []

print("=" * 75)
print("GloFAS CELL REDUNDANCY DIAGNOSTICS")
print("=" * 75)

for group_name, cells in groups.items():
    print(f"\n{group_name}")
    print("-" * 75)

    for i in range(len(cells)):
        for j in range(i + 1, len(cells)):
            a = cells[i]
            b = cells[j]

            x = df[a].to_numpy(dtype=float)
            y = df[b].to_numpy(dtype=float)

            slope, intercept = np.polyfit(x, y, 1)
            predicted = slope * x + intercept
            residuals = y - predicted

            corr = np.corrcoef(x, y)[0, 1]

            result = {
                "group": group_name,
                "cell_a": a,
                "cell_b": b,
                "pearson_r": corr,
                "slope": slope,
                "intercept": intercept,
                "r_squared": corr ** 2,
                "max_absolute_residual": np.max(
                    np.abs(residuals)
                ),
                "mean_absolute_residual": np.mean(
                    np.abs(residuals)
                ),
                "exactly_identical": np.array_equal(x, y),
                "max_absolute_difference": np.max(
                    np.abs(x - y)
                )
            }

            results.append(result)

            print(f"\n{a} vs {b}")
            for key, value in result.items():
                if key not in ["group", "cell_a", "cell_b"]:
                    print(f"{key}: {value}")

results_df = pd.DataFrame(results)

output_file = (
    OUTPUT / "glofas_cell_redundancy_diagnostics.csv"
)

results_df.to_csv(output_file, index=False)

print("\n" + "=" * 75)
print("Diagnostics saved:", output_file)
print("Completed.")
