from pathlib import Path

import geopandas as gpd
import pandas as pd

CANDIDATES_PATH = Path(
    "data/processed/glofas/glofas_candidate_cells_documented.csv"
)

# Replace these with the exact paths returned by find.
AOI_PATH = Path("data/raw/lokoja_lga_extracted/lokoja_lga_utm32n.shp")
HYDRO_PATH = Path(
    "data/raw/EMSR314_02_extracted/EMSR314_02LOKOJA_DEL_v1_hydrography_l.shp"
)

METRIC_CRS = "EPSG:32632"
OUTPUT_PATH = Path(
    "data/processed/glofas/glofas_spatial_alignment.csv"
)

# Read candidate cell centers. The GRIB coordinates are longitude, latitude.
cells = pd.read_csv(CANDIDATES_PATH)
points = gpd.GeoDataFrame(
    cells,
    geometry=gpd.points_from_xy(cells["longitude"], cells["latitude"]),
    crs="EPSG:4326",
)

# Read and reproject AOI and hydrography to the same metric CRS.
aoi = gpd.read_file(AOI_PATH).to_crs(METRIC_CRS)
hydro = gpd.read_file(HYDRO_PATH).to_crs(METRIC_CRS)
points_m = points.to_crs(METRIC_CRS)

aoi_geom = aoi.geometry.union_all()

# Clip raw hydrography to the AOI before measuring proximity.
hydro_clipped = gpd.clip(hydro, aoi)

points_m["inside_aoi_check"] = points_m.geometry.apply(aoi_geom.covers)

# Distance to the nearest hydrography line within the AOI.
hydro_geom = hydro_clipped.geometry.union_all()
points_m["distance_to_hydro_m"] = points_m.geometry.distance(hydro_geom)

# This is a distance measurement, not a declaration that a cell is on a river.
points_m["river_alignment_status"] = "Review distance and hydrography geometry"

result = points_m.drop(columns="geometry").copy()
result["grid_crs"] = "EPSG:4326"
result["comparison_crs"] = METRIC_CRS
result["distance_to_hydro_km"] = result["distance_to_hydro_m"] / 1000

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(OUTPUT_PATH, index=False)

print("Candidate points:", len(result))
print("Point centers inside AOI:", int(result["inside_aoi_check"].sum()))
print("\nDistance to nearest clipped hydrography feature:")
print(
    result[
        [
            "cell_id",
            "longitude",
            "latitude",
            "inside_aoi_check",
            "distance_to_hydro_m",
            "distance_to_hydro_km",
        ]
    ].to_string(index=False)
)
print(f"\nSaved: {OUTPUT_PATH}")