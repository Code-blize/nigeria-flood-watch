
from pathlib import Path
from datetime import date
import calendar
import zipfile
import cdsapi
import eccodes
import csv
import numpy as np
import json

# ============================================================
# CONFIGURATION
# ============================================================

START_YEAR = 2015
END_YEAR = 2020

OUTPUT_DIR = Path("data/raw/glofas/multiyear")
PROCESSED_DIR = Path("data/processed/glofas")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

BBOX = [7.95, 6.60, 7.65, 6.95]  # N, W, S, E

CANDIDATE_CELLS = [4, 11, 14, 18, 19, 25, 32]

# Verified coordinates from 2018-09-15
REFERENCE_COORDS = {
    4:  (7.92500, 6.77500),
    11: (7.87500, 6.77500),
    14: (7.87500, 6.92500),
    18: (7.82500, 6.77500),
    19: (7.82500, 6.82500),
    25: (7.77500, 6.77500),
    32: (7.72500, 6.77500),
}

# ============================================================
# DOWNLOAD YEARLY DATA
# ============================================================

client = cdsapi.Client()

def download_year(year):
    output_zip = OUTPUT_DIR / f"glofas_lokoja_{year}.zip"

    if output_zip.exists() and zipfile.is_zipfile(output_zip):
        print(f"{year}: Existing ZIP found. Reusing.")
        return output_zip

    request = {
        "system_version": ["version_4_0"],
        "hydrological_model": ["lisflood"],
        "product_type": ["consolidated"],
        "variable": [
            "average_river_discharge_in_the_last_24_hours"
        ],
        "timespan": ["time_mean"],
        "year": [str(year)],
        "month": [f"{m:02d}" for m in range(1, 13)],
        "day": [f"{d:02d}" for d in range(1, 32)],
        "area": BBOX,
        "data_format": "grib",
        "download_format": "zip",
    }

    print(f"\nSubmitting GloFAS request for {year}...")

    client.retrieve(
        "cems-glofas-historical",
        request
    ).download(str(output_zip))

    if not zipfile.is_zipfile(output_zip):
        raise RuntimeError(f"{year}: Download is not a valid ZIP.")

    print(
        f"{year}: Download complete "
        f"({output_zip.stat().st_size:,} bytes)"
    )

    return output_zip


# ============================================================
# EXTRACT GRIB FROM ZIP
# ============================================================

def extract_grib(zip_path, year):
    year_dir = OUTPUT_DIR / str(year)
    year_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path) as archive:
        grib_names = [
            name for name in archive.namelist()
            if name.lower().endswith(
                (".grib", ".grb", ".grib2")
            )
        ]

        if not grib_names:
            raise RuntimeError(
                f"{year}: No GRIB file found in archive."
            )

        extracted = archive.extract(
            grib_names[0],
            year_dir
        )

    return Path(extracted)


# ============================================================
# READ GRIB USING DIRECT ECCODES
# ============================================================

def read_year(grib_path, year):
    records = []
    message_count = 0

    with open(grib_path, "rb") as f:
        while True:
            gid = eccodes.codes_grib_new_from_file(f)

            if gid is None:
                break

            try:
                message_count += 1

                short_name = eccodes.codes_get(
                    gid, "shortName"
                )

                if short_name != "avg_dis":
                    raise RuntimeError(
                        f"{year}: Unexpected variable "
                        f"{short_name}"
                    )

                data_date = eccodes.codes_get(
                    gid, "dataDate"
                )

                date_text = str(data_date)
                record_date = date(
                    int(date_text[:4]),
                    int(date_text[4:6]),
                    int(date_text[6:8])
                )

                if record_date.year != year:
                    raise RuntimeError(
                        f"Unexpected date {record_date}"
                    )

                values = np.asarray(
                    eccodes.codes_get_values(gid)
                )

                latitudes = np.asarray(
                    eccodes.codes_get_array(
                        gid, "latitudes"
                    )
                )

                longitudes = np.asarray(
                    eccodes.codes_get_array(
                        gid, "longitudes"
                    )
                )

                if not (
                    len(values)
                    == len(latitudes)
                    == len(longitudes)
                ):
                    raise RuntimeError(
                        f"{record_date}: Grid array lengths differ."
                    )

                record = {"date": record_date.isoformat()}

                for cell in CANDIDATE_CELLS:
                    index = cell - 1

                    if index >= len(values):
                        raise RuntimeError(
                            f"Cell {cell} outside returned grid."
                        )

                    lat = float(latitudes[index])
                    lon = float(longitudes[index])

                    expected_lat, expected_lon = (
                        REFERENCE_COORDS[cell]
                    )

                    if (
                        abs(lat - expected_lat) > 0.00001
                        or abs(lon - expected_lon) > 0.00001
                    ):
                        raise RuntimeError(
                            f"Cell {cell} coordinate mismatch "
                            f"on {record_date}: "
                            f"({lat}, {lon})"
                        )

                    value = float(values[index])

                    if not np.isfinite(value):
                        value = None

                    record[f"cell_{cell}"] = value

                records.append(record)

            finally:
                eccodes.codes_release(gid)

    print(
        f"{year}: Read {message_count} GRIB messages."
    )

    return records, message_count


# ============================================================
# MAIN EXTRACTION
# ============================================================

all_records = []
yearly_report = []

for year in range(START_YEAR, END_YEAR + 1):
    print("\n" + "=" * 60)
    print(f"PROCESSING {year}")
    print("=" * 60)

    zip_path = download_year(year)
    grib_path = extract_grib(zip_path, year)

    records, message_count = read_year(
        grib_path, year
    )

    unique_dates = {
        row["date"] for row in records
    }

    expected_days = (
        366 if calendar.isleap(year) else 365
    )

    if len(unique_dates) != len(records):
        raise RuntimeError(
            f"{year}: Duplicate daily records found."
        )

    if len(unique_dates) != expected_days:
        raise RuntimeError(
            f"{year}: Expected {expected_days} dates, "
            f"found {len(unique_dates)}. "
            "Inspect this year's archive before proceeding."
        )

    all_records.extend(records)

    yearly_report.append({
        "year": year,
        "grib_messages": message_count,
        "unique_dates": len(unique_dates),
        "expected_dates": expected_days,
        "status": "PASS"
    })

    print(
        f"{year}: PASS — {len(unique_dates)} unique dates."
    )


# ============================================================
# FINAL VALIDATION AND OUTPUT
# ============================================================

all_records.sort(key=lambda row: row["date"])

all_dates = [row["date"] for row in all_records]

if len(all_dates) != len(set(all_dates)):
    raise RuntimeError("Duplicate dates across years.")

expected_total = sum(
    366 if calendar.isleap(y) else 365
    for y in range(START_YEAR, END_YEAR + 1)
)

if len(all_records) != expected_total:
    raise RuntimeError(
        f"Expected {expected_total} records, "
        f"found {len(all_records)}."
    )

csv_path = (
    PROCESSED_DIR /
    "glofas_2015_2020_candidate_timeseries.csv"
)

fieldnames = [
    "date"
] + [
    f"cell_{cell}" for cell in CANDIDATE_CELLS
]

with open(csv_path, "w", newline="") as f:
    writer = csv.DictWriter(
        f, fieldnames=fieldnames
    )
    writer.writeheader()
    writer.writerows(all_records)

report_path = (
    PROCESSED_DIR /
    "glofas_2015_2020_quality_report.json"
)

report = {
    "dataset": "GloFAS historical v4.0",
    "variable": "avg_dis",
    "units": "m3/s",
    "period": f"{START_YEAR}-01-01 to {END_YEAR}-12-31",
    "candidate_cells": CANDIDATE_CELLS,
    "total_records": len(all_records),
    "expected_records": expected_total,
    "yearly_checks": yearly_report,
    "missing_values": {
        field: sum(
            row[field] is None for row in all_records
        )
        for field in fieldnames[1:]
    },
    "status": "PASS"
}

with open(report_path, "w") as f:
    json.dump(report, f, indent=4)

print("\n" + "=" * 60)
print("MULTI-YEAR EXTRACTION COMPLETED")
print("=" * 60)
print("Total daily records:", len(all_records))
print("Expected daily records:", expected_total)
print("CSV:", csv_path)
print("Quality report:", report_path)
print("\nMissing values:")
for cell, count in report["missing_values"].items():
    print(f"{cell}: {count}")
