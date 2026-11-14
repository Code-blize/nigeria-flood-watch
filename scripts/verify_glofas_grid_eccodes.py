
from pathlib import Path
import numpy as np
import eccodes

grib_path = Path(
    "data/raw/glofas/api_validation/data.grib"
)

candidate_cells = [4, 11, 14, 18, 19, 25, 32]

with open(grib_path, "rb") as f:
    gid = eccodes.codes_grib_new_from_file(f)

    if gid is None:
        raise RuntimeError("Unable to read GRIB message")

    values = np.asarray(
        eccodes.codes_get_values(gid)
    )

    latitudes = np.asarray(
        eccodes.codes_get_array(gid, "latitudes")
    )

    longitudes = np.asarray(
        eccodes.codes_get_array(gid, "longitudes")
    )

    date = eccodes.codes_get(gid, "dataDate")

    eccodes.codes_release(gid)

print("GloFAS GRID VERIFICATION")
print("=" * 60)
print("Date:", date)
print("Number of grid points:", len(values))

print("\nCANDIDATE GRID CELLS")
print("-" * 60)

for cell in candidate_cells:
    index = cell - 1

    print(
        f"Cell {cell:>2}: "
        f"Latitude={latitudes[index]:.5f}, "
        f"Longitude={longitudes[index]:.5f}, "
        f"Discharge={values[index]:.3f} m3/s"
    )

print("\nVerification completed.")
