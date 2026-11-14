
from pathlib import Path
import cdsapi
import zipfile

# Output directory
output_dir = Path("data/raw/glofas")
output_dir.mkdir(parents=True, exist_ok=True)

target = output_dir / "glofas_lokoja_september_2018.zip"

# September 2018: 30 days
days = [f"{day:02d}" for day in range(1, 31)]

dataset = "cems-glofas-historical"

request = {
    "system_version": ["version_4_0"],
    "hydrological_model": ["lisflood"],
    "product_type": ["consolidated"],
    "timespan": ["time_mean"],
    "variable": [
        "average_river_discharge_in_the_last_24_hours"
    ],
    "year": ["2018"],
    "month": ["09"],
    "day": days,

    # North, West, South, East
    "area": [7.95, 6.60, 7.65, 6.95],

    "data_format": "grib",
    "download_format": "zip",
}

print("Requesting GloFAS daily discharge")
print("Period: 1–30 September 2018")
print("Grid area: Lokoja vicinity")

client = cdsapi.Client()
client.retrieve(dataset, request, str(target))

print("\nDownload completed.")
print("File:", target)
print("Size:", round(target.stat().st_size / (1024 * 1024), 2), "MB")

# Check archive integrity
with zipfile.ZipFile(target, "r") as archive:
    bad_file = archive.testzip()

    if bad_file:
        raise RuntimeError(f"Corrupt archive member: {bad_file}")

    print("\nArchive contents:")
    for item in archive.infolist():
        print(item.filename, item.file_size, "bytes")

print("\nArchive integrity check passed.")
