
from pathlib import Path

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# FILE PATHS
# ============================================================

BASE = Path("data")

LGA_FILE = BASE / "processed/lokoja_lga_boundary.geojson"

FLOOD_FILE = BASE / "processed/lokoja_2018_flood_extent.geojson"

HYDRO_POLYGON_FILE = (
    BASE / "raw/EMSR314_02_extracted/"
    "EMSR314_02LOKOJA_DEL_v1_hydrography_a.shp"
)

HYDRO_LINE_FILE = (
    BASE / "raw/EMSR314_02_extracted/"
    "EMSR314_02LOKOJA_DEL_v1_hydrography_l.shp"
)

HYDROBASINS_FILE = (
    BASE / "processed/"
    "hydrobasins_combined_upstream_network_lokoja.geojson"
)

OUTPUT_DIR = BASE / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_MAP = (
    OUTPUT_DIR /
    "glofas_hydrological_network_diagnostic.png"
)

OUTPUT_INVENTORY = (
    BASE / "processed/glofas/"
    "glofas_hydrological_network_inventory.csv"
)

# ============================================================
# GLOFAS CANDIDATE CELLS
# ============================================================

cell_data = [
    ("cell_4", 7.92500, 6.77500, "Group A"),
    ("cell_11", 7.87500, 6.77500, "Group A"),
    ("cell_18", 7.82500, 6.77500, "Group A"),
    ("cell_14", 7.87500, 6.92500, "Group B"),
    ("cell_19", 7.82500, 6.82500, "Group B"),
    ("cell_25", 7.77500, 6.77500, "Group C"),
    ("cell_32", 7.72500, 6.77500, "Group C"),
]

cells_df = pd.DataFrame(
    cell_data,
    columns=["cell", "latitude", "longitude", "group"]
)

cells = gpd.GeoDataFrame(
    cells_df,
    geometry=gpd.points_from_xy(
        cells_df["longitude"],
        cells_df["latitude"]
    ),
    crs="EPSG:4326"
)

# ============================================================
# LOAD DATASETS
# ============================================================

def load_layer(path, label):
    if not path.exists():
        raise FileNotFoundError(
            f"{label} not found: {path}"
        )

    layer = gpd.read_file(path)

    if layer.empty:
        raise ValueError(f"{label} contains no features.")

    if layer.crs is None:
        raise ValueError(
            f"{label} has no CRS. Check the source data."
        )

    return layer.to_crs("EPSG:4326")

print("Loading spatial datasets...")

lga = load_layer(LGA_FILE, "Lokoja LGA")
flood = load_layer(FLOOD_FILE, "2018 flood extent")

hydro_polygons = load_layer(
    HYDRO_POLYGON_FILE,
    "Hydrography polygons"
)

hydro_lines = load_layer(
    HYDRO_LINE_FILE,
    "Hydrography lines"
)

hydrobasins = load_layer(
    HYDROBASINS_FILE,
    "HydroBASINS network"
)

print("\nDATASET INVENTORY")
print("-" * 60)

for name, layer in [
    ("Lokoja LGA", lga),
    ("2018 flood extent", flood),
    ("Hydrography polygons", hydro_polygons),
    ("Hydrography lines", hydro_lines),
    ("HydroBASINS", hydrobasins),
]:
    print(f"{name}: {len(layer)} features")

# ============================================================
# IDENTIFY NAMED HYDROGRAPHY
# ============================================================

if "name" not in hydro_polygons.columns:
    raise ValueError(
        "Hydrography polygon layer has no 'name' field."
    )

hydro_polygons["name_clean"] = (
    hydro_polygons["name"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
)

named_rivers = hydro_polygons[
    hydro_polygons["name_clean"].isin(
        ["niger", "benue"]
    )
].copy()

named_rivers["river_label"] = (
    named_rivers["name_clean"].str.title()
)

print("\nNAMED RIVER POLYGONS")
print(named_rivers["river_label"].value_counts())

# ============================================================
# INSPECT HYDROGRAPHY LINE ATTRIBUTES
# ============================================================

print("\nHYDROGRAPHY LINE ATTRIBUTES")

for column in hydro_lines.columns:
    if column != "geometry":
        print(
            f"\n{column}:",
            hydro_lines[column].nunique(),
            "unique values"
        )

if "name" in hydro_lines.columns:
    print("\nLine names:")
    print(
        hydro_lines["name"]
        .fillna("Unknown")
        .value_counts()
        .head(10)
    )

# ============================================================
# CATCHMENT INVENTORY
# ============================================================

print("\nHYDROBASINS ATTRIBUTE FIELDS")
print(list(hydrobasins.columns))

# Do not assign Niger or Benue identities based only on
# the geometry or proximity of individual catchments.

# ============================================================
# SPATIAL INVENTORY
# ============================================================

lga_union = lga.geometry.union_all()

cells["inside_lokoja_lga"] = (
    cells.geometry.intersects(lga_union)
)

cells_projected = cells.to_crs("EPSG:32632")
rivers_projected = named_rivers.to_crs("EPSG:32632")

nearest_rivers = []
nearest_distances = []

for _, cell in cells_projected.iterrows():

    distances = rivers_projected.geometry.distance(
        cell.geometry
    )

    nearest_index = distances.idxmin()

    nearest_rivers.append(
        rivers_projected.loc[
            nearest_index, "river_label"
        ]
    )

    nearest_distances.append(
        float(distances.loc[nearest_index])
    )

cells["nearest_named_hydrography"] = nearest_rivers
cells["nearest_named_hydrography_distance_m"] = (
    nearest_distances
)

OUTPUT_INVENTORY.parent.mkdir(
    parents=True,
    exist_ok=True
)

cells.drop(columns="geometry").to_csv(
    OUTPUT_INVENTORY,
    index=False
)

# ============================================================
# MAP
# ============================================================

fig, ax = plt.subplots(figsize=(15, 12))

# 1. HydroBASINS catchment boundaries
hydrobasins.boundary.plot(
    ax=ax,
    color="dimgray",
    linewidth=0.45,
    alpha=0.45,
    label="HydroBASINS catchment boundaries",
    zorder=1
)

# 2. September 2018 flood extent
flood.plot(
    ax=ax,
    color="lightskyblue",
    edgecolor="steelblue",
    linewidth=0.35,
    alpha=0.55,
    label="September 2018 flood extent",
    zorder=2
)

# 3. Lokoja LGA
lga.boundary.plot(
    ax=ax,
    color="black",
    linewidth=1.5,
    label="Lokoja LGA boundary",
    zorder=3
)

# 4. Named river polygons
river_styles = {
    "Niger": "darkorange",
    "Benue": "purple"
}

for river_name, color in river_styles.items():

    subset = named_rivers[
        named_rivers["river_label"] == river_name
    ]

    if not subset.empty:
        subset.plot(
            ax=ax,
            color=color,
            edgecolor=color,
            linewidth=1.1,
            alpha=0.8,
            label=f"{river_name} named hydrography",
            zorder=4
        )

# 5. Hydrography lines
hydro_lines.plot(
    ax=ax,
    color="deepskyblue",
    linewidth=0.9,
    alpha=0.85,
    label="Mapped hydrography lines",
    zorder=5
)

# 6. Candidate grid cells
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

    subset = cells[
        cells["group"] == group_name
    ]

    subset.plot(
        ax=ax,
        color=style["color"],
        marker=style["marker"],
        markersize=100,
        edgecolor="black",
        linewidth=0.8,
        label=f"{group_name} GloFAS cells",
        zorder=7
    )

    for _, row in subset.iterrows():
        ax.annotate(
            row["cell"].replace("cell_", ""),
            xy=(
                row.geometry.x,
                row.geometry.y
            ),
            xytext=(6, 6),
            textcoords="offset points",
            fontsize=9,
            fontweight="bold",
            zorder=8
        )

# ============================================================
# MAP FORMATTING
# ============================================================

ax.set_title(
    "GloFAS Candidate Cells and Hydrological Network\n"
    "Lokoja, Nigeria | September 2018 Flood Context",
    fontsize=15,
    fontweight="bold",
    pad=16
)

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

ax.grid(
    True,
    linestyle="--",
    alpha=0.3
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
# FINAL REPORT
# ============================================================

print("\n" + "=" * 65)
print("HYDROLOGICAL NETWORK DIAGNOSTIC COMPLETED")
print("=" * 65)

print("Candidate cells:", len(cells))
print(
    "Cells intersecting Lokoja LGA:",
    int(cells["inside_lokoja_lga"].sum())
)

print("\nCandidate cell inventory:")
print(
    cells[
        [
            "cell",
            "group",
            "inside_lokoja_lga",
            "nearest_named_hydrography",
            "nearest_named_hydrography_distance_m"
        ]
    ].to_string(index=False)
)

print("\nMap:", OUTPUT_MAP)
print("Inventory:", OUTPUT_INVENTORY)