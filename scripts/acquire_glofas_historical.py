
from pathlib import Path
import cdsapi

# Output directory
output_dir = Path("data/raw/glofas")
output_dir.mkdir(parents=True, exist_ok=True)

# Copernicus Early Warning Data Store
client = cdsapi.Client()

dataset = "cems-glofas-historical"

request = {
    "system_version": ["version_4_0"],
    "hydrological_model": ["lisflood"],
    "product_type": ["consolidated"],
    "timespan": ["time_mean"],
    "variable": ["average_river_discharge_in_the_last_24_hours"],
    "year": ["2018"],
    "month": ["09"],
    "day": ["15"],

    # North, West, South, East
    "area": [7.95, 6.60, 7.65, 6.95],

    "data_format": "grib",
    "download_format": "zip",
}

target = output_dir / "glofas_lokoja_2018-09-15.zip"

print("Submitting GloFAS historical data request...")
print("Date: 15 September 2018")
print("Region: Lokoja vicinity")

client.retrieve(dataset, request, str(target))

print(f"Download completed: {target}")
print(f"File size: {target.stat().st_size / (1024 * 1024):.2f} MB")
