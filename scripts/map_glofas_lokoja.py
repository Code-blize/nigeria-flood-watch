
from pathlib import Path

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --------------------------------------------------
# 1. INPUT AND OUTPUT PATHS
# --------------------------------------------------

grid_file = Path(
    "data/processed/glofas/glofas_lokoja_2018-09-15_grid.csv"
)

boundary_file = Path(
    "data/processed/lokoja_lga_boundary.geojson"
)

output_dir = Path("data/processed/glofas")
figure_dir = Path("data/figures")

output_dir.mkdir(parents=True, exist_ok=True)
figure_dir.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

grid = pd.read_csv(grid_file)

boundary = gpd.read_file(boundary_file)

if boundary.crs is None:
    raise ValueError("Lokoja boundary has no CRS.")

boundary = boundary.to_crs("EPSG:4326")

# --------------------------------------------------
# 3. CREATE GRID POINTS
# --------------------------------------------------

points = gpd.GeoDataFrame(
    grid,
    geometry=gpd.points_from_xy(
        grid["longitude"],
        grid["latitude"]
    ),
    crs="EPSG:4326"
)

# --------------------------------------------------
# 4. IDENTIFY POINTS INSIDE LOKOJA LGA
# --------------------------------------------------

lga_geometry = boundary.geometry.union_all()

points["inside_lokoja_lga"] = (
    points.geometry.apply(lga_geometry.covers)
)

inside = points[
    points["inside_lokoja_lga"]
].copy()

outside = points[
    ~points["inside_lokoja_lga"]
].copy()

print("=" * 55)
print("GloFAS GRID SPATIAL ANALYSIS")
print("=" * 55)

print("Total grid points:", len(points))
print("Inside Lokoja LGA:", len(inside))
print("Outside Lokoja LGA:", len(outside))

print("\nGrid points inside Lokoja:")
print(
    inside[
        ["cell_id", "latitude", "longitude", "discharge_m3_s"]
    ].to_string(index=False)
)

# --------------------------------------------------
# 5. EXPORT SPATIAL DATA
# --------------------------------------------------

points.to_file(
    output_dir / "glofas_lokoja_grid_points.geojson",
    driver="GeoJSON"
)

inside.to_file(
    output_dir / "glofas_grid_points_inside_lokoja.geojson",
    driver="GeoJSON"
)

# --------------------------------------------------
# 6. CREATE MAP
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 9))

boundary.boundary.plot(
    ax=ax,
    linewidth=1.5,
    color="black",
    label="Lokoja LGA boundary"
)

# Plot grid points using a logarithmic colour scale.
positive = points[
    points["discharge_m3_s"] > 0
]

zero = points[
    points["discharge_m3_s"] == 0
]

if not zero.empty:
    zero.plot(
        ax=ax,
        color="lightgrey",
        markersize=35,
        label="Zero discharge"
    )

if not positive.empty:
    positive.plot(
        ax=ax,
        column="discharge_m3_s",
        cmap="YlOrRd",
        markersize=65,
        legend=True,
        norm=plt.matplotlib.colors.LogNorm(
            vmin=positive["discharge_m3_s"].min(),
            vmax=positive["discharge_m3_s"].max()
        ),
        legend_kwds={
            "label": "Discharge (m³/s, logarithmic scale)"
        }
    )

# Label each grid point.
for _, row in points.iterrows():
    ax.annotate(
        str(int(row["cell_id"])),
        xy=(row.geometry.x, row.geometry.y),
        xytext=(3, 3),
        textcoords="offset points",
        fontsize=7
    )

ax.set_title(
    "GloFAS Historical Discharge Grid\n"
    "Lokoja Vicinity | 15 September 2018"
)

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.grid(True, alpha=0.3)
ax.legend(loc="best")

plt.tight_layout()

map_file = (
    figure_dir / "glofas_lokoja_discharge_grid_2018-09-15.png"
)

plt.savefig(map_file, dpi=300, bbox_inches="tight")
plt.close()

print("\nExport completed:")
print(output_dir / "glofas_lokoja_grid_points.geojson")
print(output_dir / "glofas_grid_points_inside_lokoja.geojson")
print(map_file)

print("\nSpatial analysis completed.")
