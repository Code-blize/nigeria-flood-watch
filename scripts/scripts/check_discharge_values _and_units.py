from pathlib import Path
import numpy as np
from eccodes import (
    codes_grib_new_from_file,
    codes_get_array,
    codes_release,
)

path = Path("data/raw/glofas/extracted/data.grib")

with path.open("rb") as f:
    grib = codes_grib_new_from_file(f)

if grib is None:
    raise RuntimeError(f"No GRIB message found in {path}")

values = np.asarray(codes_get_array(grib, "values"), dtype=float)
lats = np.asarray(codes_get_array(grib, "latitudes"), dtype=float)
lons = np.asarray(codes_get_array(grib, "longitudes"), dtype=float)

print("Cell count:", len(values))
print("Zero values:", int(np.sum(values == 0)))
print("Negative values:", int(np.sum(values < 0)))
print("Minimum:", float(np.min(values)))
print("Median:", float(np.median(values)))
print("Maximum:", float(np.max(values)))
print("Mean:", float(np.mean(values)))

print("\nHighest 10 grid-cell values:")
for i in np.argsort(values)[-10:][::-1]:
    print(
        f"value={values[i]:.5f} m3/s, "
        f"latitude={lats[i]:.5f}, longitude={lons[i]:.5f}"
    )

codes_release(grib)