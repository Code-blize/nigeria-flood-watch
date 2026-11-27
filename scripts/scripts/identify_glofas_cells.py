from pathlib import Path

import geopandas as gpd
import pandas as pd
from eccodes import (
    codes_grib_new_from_file,
    codes_get,
    codes_get_array,
    codes_release,
)

GRIB_PATH = Path("data/raw/glofas/extracted/data.grib")

# Change this to the actual path of your AOI shapefile in Codespaces.
AOI_PATH = Path("data/processed/vector/lokoja_lga_utm32n.shp")

OUTPUT_PATH = Path("data/processed/glofas/glofas_candidate_cells.csv")


# Read the single GRIB message
with GRIB_PATH.open("rb") as f:
    grib = codes_grib_new_from_file(f)

if grib is None:
    raise RuntimeError(f"No GRIB message found in {GRIB_PATH}")

latitudes = codes_get_array(grib, "latitudes")
longitudes = codes_get_array(grib, "longitudes")
values = codes_get_array(grib, "values")

metadata = {
    "shortName": codes_get(grib, "shortName"),
    "units": codes_get(grib, "units"),
    "validityDate": codes_get(grib, "validityDate"),
    "validityTime": codes_get(grib, "validityTime"),
}

codes_release(grib)


# Create one row per grid point
df = pd.DataFrame({
    "cell_id": [f"GLOFAS_{i:02d}" for i in range(1, len(values) + 1)],
    "longitude": longitudes,
    "latitude": latitudes,
    "discharge_m3_s": values,
})

print("GRIB metadata:", metadata)
print("Grid points:", len(df))


# Read the authoritative study-area boundary
if not AOI_PATH.exists():
    raise FileNotFoundError(
        f"AOI shapefile not found: {AOI_PATH.resolve()}\n"
        "Update AOI_PATH to the location of lokoja_lga_utm32n.shp."
    )

aoi = gpd.read_file(AOI_PATH).to_crs("EPSG:4326")
aoi_geometry = aoi.geometry.union_all()

points = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
    crs="EPSG:4326",
)

# Point-center test: a cell is included when its grid point is within the AOI.
points["inside_aoi"] = points.geometry.apply(aoi_geometry.covers)

candidates = points[points["inside_aoi"]].copy()

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
points.drop(columns="geometry").to_csv(OUTPUT_PATH, index=False)

print("\nGrid points inside AOI:", len(candidates))
print(candidates[[
    "cell_id", "longitude", "latitude", "discharge_m3_s"
]].to_string(index=False))

print(f"\nAll grid points saved to: {OUTPUT_PATH}")