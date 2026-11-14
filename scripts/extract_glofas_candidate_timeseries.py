
from pathlib import Path
import csv

import numpy as np
import pandas as pd

from eccodes import (
    codes_grib_new_from_file,
    codes_grib_get_data,
    codes_get,
    codes_release,
)

# ============================================================
# 1. PATHS AND SETTINGS
# ============================================================

grib_file = Path(
    "data/raw/glofas/september_2018/data.grib"
)

reference_file = Path(
    "data/processed/glofas/glofas_lokoja_2018-09-15_grid.csv"
)

output_dir = Path("data/processed/glofas")
output_dir.mkdir(parents=True, exist_ok=True)

candidate_ids = [4, 11, 14, 18, 19, 25, 32]

wide_output = (
    output_dir / "glofas_september_2018_candidate_timeseries.csv"
)

long_output = (
    output_dir / "glofas_september_2018_candidate_long.csv"
)

summary_output = (
    output_dir / "glofas_september_2018_candidate_summary.csv"
)

# ============================================================
# 2. LOAD REFERENCE GRID
# ============================================================

reference = pd.read_csv(reference_file)

reference = reference[
    reference["cell_id"].isin(candidate_ids)
].copy()

if len(reference) != len(candidate_ids):
    raise ValueError("Some candidate cell IDs are missing.")

# Coordinates are used to identify cells in each GRIB message.
candidate_coordinates = {
    int(row.cell_id): (float(row.latitude), float(row.longitude))
    for row in reference.itertuples()
}

# ============================================================
# 3. EXTRACT DAILY VALUES
# ============================================================

records = []
reference_grid = None
message_count = 0

with grib_file.open("rb") as f:

    while True:

        gid = codes_grib_new_from_file(f)

        if gid is None:
            break

        try:
            date = int(codes_get(gid, "dataDate"))
            variable = codes_get(gid, "shortName")
            units = codes_get(gid, "units")

            if variable != "avg_dis":
                raise ValueError(
                    f"Unexpected variable {variable} on {date}"
                )

            if units != "m**3 s**-1":
                raise ValueError(
                    f"Unexpected units {units} on {date}"
                )

            points = codes_grib_get_data(gid)

            # ecCodes returns a tuple containing point dictionaries.
            current_grid = {}

            for point in points:

                if isinstance(point, dict):
                    lat = float(point["lat"])
                    lon = float(point["lon"])
                    value = float(point["value"])
                else:
                    lat, lon, value = map(float, point[:3])

                key = (round(lat, 5), round(lon, 5))
                current_grid[key] = value

            # Verify that the spatial grid is unchanged.
            if reference_grid is None:
                reference_grid = set(current_grid.keys())
            elif set(current_grid.keys()) != reference_grid:
                raise ValueError(
                    f"Grid coordinates changed on {date}"
                )

            row = {"date": pd.to_datetime(str(date), format="%Y%m%d")}

            for cell_id, (lat, lon) in candidate_coordinates.items():

                key = (round(lat, 5), round(lon, 5))

                if key not in current_grid:
                    raise ValueError(
                        f"Cell {cell_id} not found on {date}"
                    )

                row[f"cell_{cell_id}"] = current_grid[key]

            records.append(row)
            message_count += 1

        finally:
            codes_release(gid)

# ============================================================
# 4. VALIDATE TIME SERIES
# ============================================================

daily = pd.DataFrame(records).sort_values("date")

expected_dates = pd.date_range(
    "2018-09-01",
    "2018-09-30",
    freq="D"
)

if message_count != 30:
    raise ValueError(
        f"Expected 30 messages, found {message_count}"
    )

if daily["date"].tolist() != list(expected_dates):
    raise ValueError("Daily date coverage is incomplete.")

value_columns = [f"cell_{i}" for i in candidate_ids]

if daily[value_columns].isna().any().any():
    raise ValueError("Missing candidate-cell values detected.")

# ============================================================
# 5. EXPORT WIDE TABLE
# ============================================================

daily.to_csv(wide_output, index=False)

# ============================================================
# 6. EXPORT LONG TABLE
# ============================================================

long_data = daily.melt(
    id_vars="date",
    value_vars=value_columns,
    var_name="cell_id",
    value_name="discharge_m3_s"
)

long_data["cell_id"] = (
    long_data["cell_id"].str.replace("cell_", "", regex=False)
    .astype(int)
)

long_data.to_csv(long_output, index=False)

# ============================================================
# 7. CALCULATE SUMMARY STATISTICS
# ============================================================

summary = daily[value_columns].agg(
    ["count", "min", "max", "mean", "median", "std"]
).T

summary.index.name = "cell_id"
summary = summary.reset_index()

summary["cell_id"] = (
    summary["cell_id"].str.replace("cell_", "", regex=False)
    .astype(int)
)

summary.to_csv(summary_output, index=False)

# ============================================================
# 8. REPORT
# ============================================================

print("=" * 60)
print("GloFAS SEPTEMBER 2018 CANDIDATE CELL EXTRACTION")
print("=" * 60)

print("GRIB messages processed:", message_count)
print("Dates:", daily["date"].min(), "to", daily["date"].max())
print("Candidate cells:", candidate_ids)

print("\nDAILY DISCHARGE PREVIEW")
print(daily.head(10).to_string(index=False))

print("\nCELL SUMMARY")
print(summary.to_string(index=False))

print("\nEXPORTED FILES")
print(wide_output)
print(long_output)
print(summary_output)

print("\nExtraction and validation completed.")
