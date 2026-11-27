from pathlib import Path
import math
from eccodes import (
    codes_grib_new_from_file,
    codes_get,
    codes_get_array,
    codes_release,
)

path = Path("data/raw/glofas/extracted/data.grib")

with path.open("rb") as f:
    grib = codes_grib_new_from_file(f)

if grib is None:
    raise RuntimeError(f"No GRIB message found in {path}")

def get(key):
    try:
        return codes_get(grib, key)
    except Exception:
        return "unavailable"

values = codes_get_array(grib, "values")
latitudes = codes_get_array(grib, "latitudes")
longitudes = codes_get_array(grib, "longitudes")

missing_marker = get("missingValue")
valid_values = [
    float(v) for v in values
    if missing_marker == "unavailable"
    or not math.isclose(
        float(v), float(missing_marker),
        rel_tol=0.0, abs_tol=1e-12
    )
]

print("Grid type:", get("gridType"))
print("First latitude/longitude pairs:")
for lat, lon in list(zip(latitudes, longitudes))[:10]:
    print(f"({lat:.5f}, {lon:.5f})")

print("Discharge values (first 10):", values[:10])
print("Valid value count:", len(valid_values))
print("Minimum discharge:", min(valid_values) if valid_values else "none")
print("Maximum discharge:", max(valid_values) if valid_values else "none")
print("Bitmap present:", get("bitmapPresent"))
print("Number of missing points:", len(values) - len(valid_values))

codes_release(grib)