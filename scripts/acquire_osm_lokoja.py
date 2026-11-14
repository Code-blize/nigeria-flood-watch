
from pathlib import Path
import geopandas as gpd
import osmnx as ox

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data/raw/osm"
OUTPUT.mkdir(parents=True, exist_ok=True)

# Central Lokoja: temporary 3 km test area
point = gpd.GeoSeries(
    gpd.points_from_xy([6.74], [7.80]),
    crs="EPSG:4326"
).iloc[0]

aoi = point.buffer(0.027)  # approximately 3 km

ox.settings.overpass_url = "https://overpass.kumi.systems/api"
ox.settings.timeout = 180
ox.settings.use_cache = True
ox.settings.log_console = True

print("Testing OSM extraction around central Lokoja...")
print("AOI bounds:", aoi.bounds)

# Request only primary, secondary, tertiary and residential roads
tags = {
    "highway": [
        "primary",
        "secondary",
        "tertiary",
        "residential",
        "unclassified"
    ]
}

roads = ox.features_from_polygon(aoi, tags=tags)

if roads.empty:
    raise RuntimeError("No road features returned.")

roads = roads.reset_index()
roads = gpd.GeoDataFrame(
    roads, geometry="geometry", crs="EPSG:4326"
)

roads = roads[
    roads.geometry.notna()
    & roads.geometry.intersects(aoi)
]

output_file = OUTPUT / "lokoja_urban_roads_test.geojson"
roads.to_file(output_file, driver="GeoJSON")

print("\nSUCCESS")
print("Road features:", len(roads))
print("Geometry types:", roads.geom_type.value_counts().to_dict())
print("Saved:", output_file)
