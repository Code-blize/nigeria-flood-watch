
from pathlib import Path

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# 1. PATHS
# ============================================================

base_dir = Path("data/raw/EMSR314_02_extracted")

polygon_file = (
    base_dir /
    "EMSR314_02LOKOJA_DEL_v1_hydrography_a.shp"
)

line_file = (
    base_dir /
    "EMSR314_02LOKOJA_DEL_v1_hydrography_l.shp"
)

grid_file = Path(
    "data/processed/glofas/glofas_lokoja_grid_points.geojson"
)

lga_file = Path(
    "data/processed/lokoja_lga_boundary.geojson"
)

output_dir = Path("data/processed/glofas")
figure_dir = Path("data/figures")

output_dir.mkdir(parents=True, exist_ok=True)
figure_dir.mkdir(parents=True, exist_ok=True)

# ============================================================
# 2. LOAD DATA
# ============================================================

print("=" * 65)
print("GloFAS NIGER-BENUE RIVER CELL VERIFICATION")
print("=" * 65)

rivers = gpd.read_file(polygon_file)
river_lines = gpd.read_file(line_file)
grid = gpd.read_file(grid_file)
lga = gpd.read_file(lga_file)

# Ensure consistent geographic CRS.
rivers = rivers.to_crs("EPSG:4326")
river_lines = river_lines.to_crs("EPSG:4326")
grid = grid.to_crs("EPSG:4326")
lga = lga.to_crs("EPSG:4326")

# ============================================================
# 3. SELECT EXPLICITLY NAMED RIVER POLYGONS
# ============================================================

named_rivers = rivers[
    (rivers["obj_type"] == "BH140-River")
    & (rivers["name"].isin(["Niger", "Benue"]))
].copy()

if named_rivers.empty:
    raise ValueError("No named Niger or Benue river polygons found.")

print("\n1. NAMED RIVER FEATURES")
print("-" * 45)

print(
    named_rivers[
        ["obj_type", "name"]
    ].value_counts()
)

# ============================================================
# 4. PROJECT TO METRES FOR DISTANCE CALCULATIONS
# ============================================================

metric_crs = "EPSG:32632"

rivers_metric = named_rivers.to_crs(metric_crs)
grid_metric = grid.to_crs(metric_crs)

# Dissolve polygons by river name.
river_geometries = {}

for river_name in ["Niger", "Benue"]:

    subset = rivers_metric[
        rivers_metric["name"] == river_name
    ]

    if not subset.empty:
        river_geometries[river_name] = (
            subset.geometry.union_all()
        )

# ============================================================
# 5. CALCULATE DISTANCES AND INTERSECTIONS
# ============================================================

records = []

for _, point in grid_metric.iterrows():

    result = {
        "cell_id": int(point["cell_id"]),
        "latitude": float(point.geometry.y),
        "longitude": float(point.geometry.x),
        "discharge_m3_s": float(point["discharge_m3_s"]),
    }

    distances = {}

    for river_name, river_geometry in river_geometries.items():

        distance_m = point.geometry.distance(river_geometry)

        distances[river_name] = distance_m

        result[f"{river_name.lower()}_distance_m"] = round(
            distance_m, 2
        )

        result[f"intersects_{river_name.lower()}"] = (
            point.geometry.intersects(river_geometry)
        )

    nearest_river = min(distances, key=distances.get)

    result["nearest_named_river"] = nearest_river
    result["nearest_river_distance_m"] = round(
        distances[nearest_river], 2
    )

    records.append(result)

results = pd.DataFrame(records)

# ============================================================
# 6. SORT BY DISTANCE TO NEAREST NAMED RIVER
# ============================================================

results = results.sort_values(
    "nearest_river_distance_m"
)

print("\n2. CLOSEST GloFAS GRID CELLS")
print("-" * 45)

print(
    results[
        [
            "cell_id",
            "discharge_m3_s",
            "nearest_named_river",
            "nearest_river_distance_m",
            "niger_distance_m",
            "benue_distance_m",
        ]
    ].head(20).to_string(index=False)
)

# ============================================================
# 7. EXPORT CSV
# ============================================================

csv_output = (
    output_dir /
    "glofas_niger_benue_cell_distance_analysis.csv"
)

results.to_csv(csv_output, index=False)

# Export spatial results as GeoJSON.
spatial_results = grid.merge(
    results.drop(
        columns=["latitude", "longitude", "discharge_m3_s"]
    ),
    on="cell_id"
)

spatial_results.to_file(
    output_dir / "glofas_niger_benue_cell_analysis.geojson",
    driver="GeoJSON"
)

# ============================================================
# 8. CREATE OVERLAY MAP
# ============================================================

fig, ax = plt.subplots(figsize=(12, 10))

lga.boundary.plot(
    ax=ax,
    color="black",
    linewidth=1.4,
    label="Lokoja LGA"
)

# Plot named river polygons.
for river_name, color in [
    ("Niger", "blue"),
    ("Benue", "green"),
]:

    subset = named_rivers[
        named_rivers["name"] == river_name
    ]

    if not subset.empty:
        subset.plot(
            ax=ax,
            color=color,
            alpha=0.45,
            edgecolor=color,
            label=f"{river_name} reference polygon"
        )

# Plot grid points.
grid.plot(
    ax=ax,
    color="grey",
    markersize=30,
    alpha=0.7,
    label="Other GloFAS cells"
)

# Highlight cells with high discharge.
high_flow = grid[
    grid["discharge_m3_s"] >= 1000
]

if not high_flow.empty:
    high_flow.plot(
        ax=ax,
        color="red",
        markersize=85,
        marker="*",
        label="High-discharge cells (>= 1,000 m³/s)"
    )

# Label all grid points.
for _, row in grid.iterrows():
    ax.annotate(
        str(int(row["cell_id"])),
        (row.geometry.x, row.geometry.y),
        xytext=(4, 4),
        textcoords="offset points",
        fontsize=7
    )

ax.set_title(
    "GloFAS Grid and Named River Reference Polygons\n"
    "Lokoja | 15 September 2018"
)

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.grid(alpha=0.3)
ax.legend(loc="best")

plt.tight_layout()

map_output = (
    figure_dir /
    "glofas_niger_benue_river_overlay_2018-09-15.png"
)

plt.savefig(map_output, dpi=300, bbox_inches="tight")
plt.close()

# ============================================================
# 9. FINAL SUMMARY
# ============================================================

print("\n3. SUMMARY")
print("-" * 45)

print("Total GloFAS cells:", len(results))

print(
    "Cells intersecting Niger polygons:",
    results["intersects_niger"].sum()
)

print(
    "Cells intersecting Benue polygons:",
    results["intersects_benue"].sum()
)

print("\nCSV:", csv_output)
print(
    "GeoJSON:",
    output_dir / "glofas_niger_benue_cell_analysis.geojson"
)
print("Map:", map_output)

print("\nRiver-cell verification completed.")
