
from pathlib import Path
import json
import csv
import numpy as np

from eccodes import (
    codes_grib_new_from_file,
    codes_get,
    codes_get_values,
    codes_grib_get_data,
    codes_release,
)

# ============================================================
# 1. PATHS
# ============================================================

input_file = Path("data/raw/glofas/extracted/data.grib")
output_dir = Path("data/processed/glofas")

output_dir.mkdir(parents=True, exist_ok=True)

csv_file = output_dir / "glofas_lokoja_2018-09-15_grid.csv"
metadata_file = output_dir / "glofas_lokoja_2018-09-15_metadata.json"

if not input_file.exists():
    raise FileNotFoundError(input_file)

# ============================================================
# 2. READ GRIB
# ============================================================

print("=" * 60)
print("NIGERIAFLOODWATCH - GloFAS DATA INSPECTION")
print("=" * 60)

with input_file.open("rb") as f:
    gid = codes_grib_new_from_file(f)

if gid is None:
    raise ValueError("No valid GRIB message found.")

try:
    # ========================================================
    # 3. METADATA
    # ========================================================

    metadata_keys = [
        "edition", "discipline", "shortName", "name", "units",
        "dataDate", "dataTime", "Ni", "Nj",
        "numberOfValues", "gridType",
        "latitudeOfFirstGridPointInDegrees",
        "longitudeOfFirstGridPointInDegrees",
        "latitudeOfLastGridPointInDegrees",
        "longitudeOfLastGridPointInDegrees",
    ]

    metadata = {}

    for key in metadata_keys:
        try:
            metadata[key] = codes_get(gid, key)
        except Exception:
            metadata[key] = None

    print("\n1. GRIB METADATA")
    for key, value in metadata.items():
        print(f"{key}: {value}")

    # ========================================================
    # 4. DISCHARGE VALUES
    # ========================================================

    values = np.asarray(codes_get_values(gid), dtype=float)
    missing_value = codes_get(gid, "missingValue")

    valid_mask = np.isfinite(values) & (values != missing_value)
    valid_values = values[valid_mask]

    if len(valid_values) == 0:
        raise ValueError("No valid discharge values.")

    statistics = {
        "minimum": float(valid_values.min()),
        "maximum": float(valid_values.max()),
        "mean": float(valid_values.mean()),
        "median": float(np.median(valid_values)),
        "standard_deviation": float(valid_values.std()),
        "valid_cells": int(valid_mask.sum()),
        "missing_cells": int((~valid_mask).sum()),
    }

    print("\n2. DISCHARGE STATISTICS")
    for key, value in statistics.items():
        print(f"{key}: {value}")

    # ========================================================
    # 5. GRID COORDINATES
    # ========================================================

    grid_points = codes_grib_get_data(gid)

    print("\n3. COORDINATE RETURN FORMAT")
    print("Returned object type:", type(grid_points))
    print("Number of returned points:", len(grid_points))

    # Support dictionary and tuple coordinate formats.
    latitudes = []
    longitudes = []
    grid_values = []

    for point in grid_points:

        if isinstance(point, dict):
            lat = point.get("lat", point.get("latitude"))
            lon = point.get("lon", point.get("longitude"))
            val = point.get("value")

        elif isinstance(point, (tuple, list)):
            lat, lon, val = point[:3]

        else:
            raise TypeError(
                f"Unexpected coordinate point type: {type(point)}"
            )

        latitudes.append(float(lat))
        longitudes.append(float(lon))
        grid_values.append(float(val))

    latitudes = np.asarray(latitudes)
    longitudes = np.asarray(longitudes)
    grid_values = np.asarray(grid_values)

    if not (
        len(latitudes) == len(longitudes) == len(grid_values) == len(values)
    ):
        raise ValueError("Grid coordinate and value counts do not match.")

    print("\n4. COORDINATE EXTENT")
    print("Latitude:", latitudes.min(), "to", latitudes.max())
    print("Longitude:", longitudes.min(), "to", longitudes.max())

    # ========================================================
    # 6. GRID CELL RECORDS
    # ========================================================

    records = []

    for i, (lat, lon, discharge) in enumerate(
        zip(latitudes, longitudes, grid_values), start=1
    ):
        is_valid = np.isfinite(discharge) and discharge != missing_value

        records.append({
            "cell_id": i,
            "latitude": float(lat),
            "longitude": float(lon),
            "discharge_m3_s": float(discharge) if is_valid else None,
            "valid": bool(is_valid),
        })

    print("\n5. FIRST 10 GRID CELLS")
    for record in records[:10]:
        print(record)

    # ========================================================
    # 7. EXPORT CSV
    # ========================================================

    with csv_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "cell_id",
                "latitude",
                "longitude",
                "discharge_m3_s",
                "valid",
            ],
        )
        writer.writeheader()
        writer.writerows(records)

    # ========================================================
    # 8. EXPORT METADATA
    # ========================================================

    output_metadata = {
        "project": "NigeriaFloodWatch",
        "dataset": "GloFAS Historical",
        "date": "2018-09-15",
        "source_file": str(input_file),
        "grib_metadata": metadata,
        "statistics": statistics,
        "coordinate_extent": {
            "minimum_latitude": float(latitudes.min()),
            "maximum_latitude": float(latitudes.max()),
            "minimum_longitude": float(longitudes.min()),
            "maximum_longitude": float(longitudes.max()),
        },
    }

    with metadata_file.open("w", encoding="utf-8") as f:
        json.dump(output_metadata, f, indent=4)

    print("\n6. EXPORT COMPLETE")
    print("Grid CSV:", csv_file)
    print("Metadata:", metadata_file)

finally:
    codes_release(gid)

print("\nGloFAS inspection finished.")
print("=" * 60)
