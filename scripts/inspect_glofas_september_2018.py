
from pathlib import Path
import zipfile
from collections import Counter

from eccodes import (
    codes_grib_new_from_file,
    codes_get,
    codes_release,
)

archive_path = Path(
    "data/raw/glofas/glofas_lokoja_september_2018.zip"
)

extract_dir = Path("data/raw/glofas/september_2018")

extract_dir.mkdir(parents=True, exist_ok=True)

# 1. Extract archive
with zipfile.ZipFile(archive_path, "r") as archive:
    archive.extractall(extract_dir)

grib_file = extract_dir / "data.grib"

if not grib_file.exists():
    raise FileNotFoundError(grib_file)

print("=" * 60)
print("GloFAS SEPTEMBER 2018 DATA INSPECTION")
print("=" * 60)

print("GRIB file:", grib_file)
print("File size:", grib_file.stat().st_size, "bytes")

# 2. Inspect every GRIB message
messages = []
dates = []
variables = Counter()
grid_dimensions = set()

with grib_file.open("rb") as f:

    while True:

        gid = codes_grib_new_from_file(f)

        if gid is None:
            break

        try:
            record = {
                "date": codes_get(gid, "dataDate"),
                "time": codes_get(gid, "dataTime"),
                "variable": codes_get(gid, "shortName"),
                "name": codes_get(gid, "name"),
                "units": codes_get(gid, "units"),
                "Ni": codes_get(gid, "Ni"),
                "Nj": codes_get(gid, "Nj"),
                "numberOfValues": codes_get(
                    gid, "numberOfValues"
                ),
            }

            messages.append(record)
            dates.append(record["date"])
            variables[record["variable"]] += 1

            grid_dimensions.add(
                (record["Ni"], record["Nj"])
            )

        finally:
            codes_release(gid)

# 3. Report results
print("\n1. MESSAGE SUMMARY")
print("-" * 40)

print("Total GRIB messages:", len(messages))
print("Unique dates:", len(set(dates)))
print("Variables:", dict(variables))
print("Grid dimensions:", grid_dimensions)

print("\n2. DATE COVERAGE")
print("-" * 40)

for date in sorted(set(dates)):
    print(date)

print("\n3. FIRST MESSAGE")
print("-" * 40)

if messages:
    for key, value in messages[0].items():
        print(f"{key}: {value}")

# 4. Check requested date coverage
expected_dates = {
    int(f"201809{day:02d}")
    for day in range(1, 31)
}

actual_dates = set(dates)

missing_dates = sorted(expected_dates - actual_dates)
unexpected_dates = sorted(actual_dates - expected_dates)

print("\n4. COVERAGE VALIDATION")
print("-" * 40)

print("Expected dates:", len(expected_dates))
print("Available dates:", len(actual_dates))
print("Missing dates:", missing_dates)
print("Unexpected dates:", unexpected_dates)

print("\nInspection completed.")
print("=" * 60)
