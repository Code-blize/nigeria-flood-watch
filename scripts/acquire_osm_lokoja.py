
"""
NigeriaFloodWatch
OSM acquisition for Lokoja LGA.

Outputs:
- Roads
- Building footprints
- Waterways and water bodies
- Acquisition metadata

Input:
data/processed/lokoja_lga_boundary.geojson
"""

from pathlib import Path
from datetime import datetime, timezone
import json

import geopandas as gpd
import osmnx as ox
import pandas as pd
from shapely.geometry import shape


# --------------------------------------------------
# 1. PATHS AND SETTINGS
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

BOUNDARY_FILE = ROOT / "data/processed/lokoja_lga_boundary.geojson"
OUTPUT_DIR = ROOT / "data/raw/osm"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ox.settings.use_cache = True
ox.settings.log_console = True
ox.settings.timeout = 300
ox.settings.overpass_url = "https://overpass.kumi.systems/api"

# --------------------------------------------------
# 2. LOAD LOKOJA LGA BOUNDARY
# --------------------------------------------------

if not BOUNDARY_FILE.exists():
    raise FileNotFoundError(f"Boundary not found: {BOUNDARY_FILE}")

boundary = gpd.read_file(BOUNDARY_FILE)

if boundary.empty:
    raise ValueError("Lokoja boundary file contains no features.")

if boundary.crs is None:
    raise ValueError("Boundary CRS is missing. Define it before proceeding.")

boundary = boundary.to_crs("EPSG:4326")

aoi = boundary.geometry.union_all()

if aoi.is_empty or not aoi.is_valid:
    raise ValueError("AOI geometry is empty or invalid.")

print("AOI CRS:", boundary.crs)
print("AOI area in features:", len(boundary))
print("AOI bounds:", aoi.bounds)

# --------------------------------------------------
# 3. DEFINE OSM FEATURE TAGS
# --------------------------------------------------

feature_groups = {
    "roads": {
        "highway": True
    }
}

# --------------------------------------------------
# 4. DOWNLOAD AND SAVE FEATURES
# --------------------------------------------------

results = []

for name, tags in feature_groups.items():

    print(f"\nDownloading {name}...")

    try:
        gdf = ox.features_from_polygon(aoi, tags=tags)

        if gdf.empty:
            print(f"WARNING: No {name} features returned.")
            results.append({
                "dataset": name,
                "feature_count": 0,
                "status": "No features returned"
            })
            continue

        # Preserve all original OSM tags.
        gdf = gdf.reset_index()

        # Retain features intersecting the Lokoja LGA.
        gdf = gpd.GeoDataFrame(
            gdf,
            geometry="geometry",
            crs="EPSG:4326"
        )

        gdf = gdf[gdf.geometry.notna()]
        gdf = gdf[gdf.geometry.intersects(aoi)]

        output_file = OUTPUT_DIR / f"lokoja_osm_{name}.geojson"

        gdf.to_file(output_file, driver="GeoJSON")

        print(f"Saved: {output_file}")
        print(f"Features: {len(gdf)}")
        print("Geometry types:", gdf.geom_type.value_counts().to_dict())

        results.append({
            "dataset": name,
            "feature_count": len(gdf),
            "geometry_types": json.dumps(
                gdf.geom_type.value_counts().to_dict()
            ),
            "output_file": str(output_file.relative_to(ROOT)),
            "status": "Downloaded"
        })

    except Exception as exc:
        print(f"ERROR downloading {name}: {exc}")

        results.append({
            "dataset": name,
            "feature_count": None,
            "status": f"Failed: {str(exc)}"
        })

# --------------------------------------------------
# 5. SAVE ACQUISITION METADATA
# --------------------------------------------------

metadata = pd.DataFrame(results)

metadata["source"] = "OpenStreetMap via OSMnx/Overpass"
metadata["aoi"] = "Lokoja LGA"
metadata["crs"] = "EPSG:4326"
metadata["access_date_utc"] = datetime.now(
    timezone.utc
).isoformat()

metadata_file = OUTPUT_DIR / "lokoja_osm_acquisition_metadata.csv"

metadata.to_csv(metadata_file, index=False)

print("\nACQUISITION SUMMARY")
print(metadata.to_string(index=False))

print("\nMetadata saved:", metadata_file)
print("\nOSM acquisition process finished.")
