
from pathlib import Path
import cdsapi
import zipfile
import pygrib

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

OUTPUT_DIR = Path("data/raw/glofas/api_validation")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_ZIP = OUTPUT_DIR / "glofas_v4_2018-09-15_updated_api.zip"

BBOX = [
    7.95,  # North
    6.60,  # West
    7.65,  # South
    6.95   # East
]

# --------------------------------------------------
# UPDATED EWDS REQUEST
# --------------------------------------------------

request = {
    "system_version": ["version_4_0"],
    "hydrological_model": ["lisflood"],
    "product_type": ["consolidated"],
    "variable": [
        "average_river_discharge_in_the_last_24_hours"
    ],
    "timespan": ["time_mean"],
    "year": ["2018"],
    "month": ["09"],
    "day": ["15"],
    "area": BBOX,
    "data_format": "grib",
    "download_format": "zip"
}

print("=" * 55)
print("GloFAS UPDATED API VALIDATION")
print("=" * 55)
print("Date: 2018-09-15")
print("Version: 4.0")
print("Product: Consolidated")
print("Variable: Average river discharge")
print()

# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------

client = cdsapi.Client()

if not OUTPUT_ZIP.exists():
    print("Submitting updated API request...")
    client.retrieve(
        "cems-glofas-historical",
        request
    ).download(str(OUTPUT_ZIP))
else:
    print("Existing validation ZIP found. Reusing it.")

print(f"\nDownloaded file: {OUTPUT_ZIP}")
print(f"File size: {OUTPUT_ZIP.stat().st_size:,} bytes")

# --------------------------------------------------
# VERIFY ZIP AND GRIB
# --------------------------------------------------

if not zipfile.is_zipfile(OUTPUT_ZIP):
    raise RuntimeError("Downloaded file is not a valid ZIP archive.")

with zipfile.ZipFile(OUTPUT_ZIP) as archive:
    grib_files = [
        name for name in archive.namelist()
        if name.lower().endswith((".grib", ".grb", ".grib2"))
    ]

    if not grib_files:
        raise RuntimeError("No GRIB file found inside ZIP.")

    extracted = archive.extract(
        grib_files[0],
        OUTPUT_DIR
    )

print(f"Extracted GRIB: {extracted}")

# --------------------------------------------------
# INSPECT GRIB MESSAGES
# --------------------------------------------------

grbs = pygrib.open(str(extracted))
messages = list(grbs)
grbs.close()

if not messages:
    raise RuntimeError("GRIB contains no messages.")

print(f"\nGRIB messages: {len(messages)}")

for i, msg in enumerate(messages, start=1):
    print(f"\nMessage {i}")
    print("Date:", msg.dataDate)
    print("Short name:", msg.shortName)
    print("Variable:", msg.name)
    print("Units:", msg.units)
    print("Grid dimensions:", msg.Ni, "x", msg.Nj)

    values = msg.values
    print("Minimum:", float(values.min()))
    print("Maximum:", float(values.max()))
    print("Mean:", float(values.mean()))

print("\nValidation completed.")