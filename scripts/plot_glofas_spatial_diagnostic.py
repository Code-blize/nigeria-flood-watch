
from pathlib import Path

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# FILE PATHS
# ============================================================

LGA_FILE = Path(
    "data/processed/lokoja_lga_boundary.geojson"
)

FLOOD_FILE = Path(
    "data/processed/lokoja_2018_flood_extent.geojson"
)

HYDROGRAPHY_FILE = Path(
    "data/raw/EMSR314_02_extracted/"
    "EMSR314_02LOKOJA_DEL_v1_hydrography_a.shp"
)

OUTPUT_DIR = Path("data/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_MAP = (
    OUTPUT_DIR /
    "glofas_seven_candidate_cells_spatial_diagnostic.png"
)

OUTPUT_CSV = (
    Path("data/processed/glofas") /
    "glofas_candidate_cell_spatial_inventory.csv"
)

# ============================================================
# VERIFIED CANDIDATE CELL COORDINATES
# ============================================================

cell_data = [
    {"cell": "cell_4", "latitude": 7.92500,
     "longitude": 6.77500, "group": "Group A"},

    {"cell": "cell_11", "latitude": 7.87500,
     "longitude": 6.77500, "group": "Group A"},

    {"cell": "cell_18", "latitude": 7.82500,
     "longitude": 6.77500, "group": "Group A"},

    {"cell": "cell_14", "latitude": 7.87500,
     "longitude": 6.92500, "group": "Group B"},

    {"cell": "cell_19", "latitude": 7.82500,
     "longitude": 6.82500, "group": "Group B"},

    {"cell": "cell_25", "latitude": 7.77500,
     "longitude": 6.77500, "group": "Group C"},

    {"cell": "cell_32", "latitude": 7.72500,
     "longitude": 6.77500, "group": "Group C"},
]

cells_df = pd.DataFrame(cell_data)

cells = gpd.GeoDataFrame(
    cells_df,
    geometry=gpd.points_from_xy(
        cells_df["longitude"],
        cells_df["latitude"]
    ),
    crs="EPSG:4326"
)

# ============================================================
# LOAD SPATIAL DATA
# ============================================================

print("Loading spatial datasets...")

lga = gpd.read_file(LGA_FILE)
flood = gpd.read_file(FLOOD_FILE)
hydro = gpd.read_file(HYDROGRAPHY_FILE)

for name, layer in [
    ("LGA", lga),
    ("Flood extent", flood),
    ("Hydrography", hydro),
    ("Candidate cells", cells)
]:
    if layer.crs is None:
        raise ValueError(f"{name} has no CRS.")

    if layer.crs != "EPSG:4326":
        layer = layer.to_crs("EPSG:4326")

    if name == "LGA":
        lga = layer
    elif name == "Flood extent":
        flood = layer
    elif name == "Hydrography":
        hydro = layer
    else:
        cells = layer

# ============================================================
# FILTER NAMED NIGER AND BENUE HYDROGRAPHY
# ============================================================

if "name" not in hydro.columns:
    raise ValueError(
        "Expected a 'name' field in the hydrography layer."
    )

hydro["name_clean"] = (
    hydro["name"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
)

named_rivers = hydro[
    hydro["name_clean"].isin(["niger", "benue"])
].copy()

named_rivers["river_label"] = (
    named_rivers["name_clean"].str.title()
)

print("\nNamed hydrography features:")
print(
    named_rivers[
        ["name", "geometry"]
    ].groupby("name").size()
)

# ============================================================
# SPATIAL INVENTORY
# ============================================================

print("\nCandidate cell locations:")
print(
    cells[
        ["cell", "group", "latitude", "longitude"]
    ].to_string(index=False)
)

# Spatial intersection with LGA
lga_union = lga.geometry.union_all()

cells["inside_lokoja_lga"] = (
    cells.geometry.within(lga_union)
    | cells.geometry.intersects(lga_union)
)

# Distance to named hydrography, measured in metres.
# Use a projected CRS for distance calculations.
cells_projected = cells.to_crs("EPSG:32632")
rivers_projected = named_rivers.to_crs("EPSG:32632")

nearest_river = []
nearest_distance = []

for _, cell in cells_projected.iterrows():

    if rivers_projected.empty:
        nearest_river.append(None)
        nearest_distance.append(None)
        continue

    distances = rivers_projected.geometry.distance(
        cell.geometry
    )

    nearest_index = distances.idxmin()

    nearest_river.append(
        rivers_projected.loc[
            nearest_index, "river_label"
        ]
    )

    nearest_distance.append(
        float(distances.loc[nearest_index])
    )

cells["nearest_named_hydrography"] = nearest_river
cells["nearest_hydrography_distance_m"] = nearest_distance

cells.drop(columns="geometry").to_csv(
    OUTPUT_CSV,
    index=False
)

# ============================================================
# MAP
# ============================================================

fig, ax = plt.subplots(figsize=(13, 11))

# Flood extent
flood.plot(
    ax=ax,
    color="lightskyblue",
    edgecolor="steelblue",
    linewidth=0.4,
    alpha=0.55,
    label="September 2018 flood extent"
)

# Lokoja LGA boundary
lga.boundary.plot(
    ax=ax,
    color="black",
    linewidth=1.5,
    label="Lokoja LGA"
)

# Named river hydrography
for river_name, color in [
    ("Niger", "darkorange"),
    ("Benue", "purple")
]:
    subset = named_rivers[
        named_rivers["river_label"] == river_name
    ]

    if not subset.empty:
        subset.plot(
            ax=ax,
            color=color,
            edgecolor=color,
            linewidth=1.8,
            alpha=0.9,
            label=f"{river_name} named hydrography"
        )

# Candidate grid cells
group_styles = {
    "Group A": {
        "color": "red",
        "marker": "o"
    },
    "Group B": {
        "color": "green",
        "marker": "s"
    },
    "Group C": {
        "color": "magenta",
        "marker": "^"
    }
}

for group_name, style in group_styles.items():

    subset = cells[cells["group"] == group_name]

    subset.plot(
        ax=ax,
        color=style["color"],
        marker=style["marker"],
        markersize=85,
        edgecolor="black",
        linewidth=0.7,
        label=f"{group_name} candidate cells",
        zorder=5
    )

    for _, row in subset.iterrows():
        ax.annotate(
            row["cell"].replace("cell_", ""),
            xy=(row.geometry.x, row.geometry.y),
            xytext=(5, 6),
            textcoords="offset points",
            fontsize=9,
            fontweight="bold"
        )

# ============================================================
# MAP FORMATTING
# ============================================================

ax.set_title(
    "GloFAS Candidate Grid Cells and Lokoja Hydrography\n"
    "September 2018 Flood Context",
    fontsize=15,
    fontweight="bold",
    pad=15
)

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

ax.grid(
    True,
    linestyle="--",
    alpha=0.35
)

ax.legend(
    loc="best",
    fontsize=8,
    frameon=True
)

ax.set_aspect("equal", adjustable="datalim")

fig.tight_layout()

fig.savefig(
    OUTPUT_MAP,
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)

# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 65)
print("SPATIAL DIAGNOSTIC COMPLETED")
print("=" * 65)

print("Candidate cells:", len(cells))
print(
    "Cells intersecting Lokoja LGA:",
    int(cells["inside_lokoja_lga"].sum())
)

print("\nSpatial inventory:")
print(
    cells[
        [
            "cell",
            "group",
            "inside_lokoja_lga",
            "nearest_named_hydrography",
            "nearest_hydrography_distance_m"
        ]
    ].to_string(index=False)
)

print("\nMap:", OUTPUT_MAP)
print("Inventory:", OUTPUT_CSV)
