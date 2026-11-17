
from pathlib import Path

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from shapely.geometry import Point, box

# ============================================================
# 1. CONFIGURATION
# ============================================================

BASE = Path("data")

FILES = {
    "lga": BASE / "processed/lokoja_lga_boundary.geojson",
    "aoi": BASE / "processed/lokoja_local_analysis_extent.geojson",
    "flood": BASE / "processed/lokoja_2018_flood_extent.geojson",
    "basins": BASE / "processed/hydrobasins_combined_upstream_network_lokoja.geojson",
    "hydro_polygons": (
        BASE / "raw/EMSR314_02_extracted/"
        "EMSR314_02LOKOJA_DEL_v1_hydrography_a.shp"
    ),
    "hydro_lines": (
        BASE / "raw/EMSR314_02_extracted/"
        "EMSR314_02LOKOJA_DEL_v1_hydrography_l.shp"
    ),
}

OUTPUT = BASE / "processed/spatial_verification"
FIGURES = BASE / "figures"

OUTPUT.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)

REGIONAL_MAP = FIGURES / "lokoja_regional_hydrological_study_area.png"
LOCAL_MAP = FIGURES / "lokoja_local_study_area_detail.png"
INVENTORY = OUTPUT / "lokoja_spatial_verification_inventory.csv"
SUMMARY = OUTPUT / "lokoja_spatial_verification_summary.txt"

# Local display window. This is a map extent, not a new AOI.
LOCAL_BOUNDS = (6.70, 7.65, 7.05, 8.05)

# Projected CRS for distance calculations in metres.
METRIC_CRS = "EPSG:32632"

# ============================================================
# 2. CANDIDATE GLOFAS CELLS
# ============================================================

cell_records = [
    ("cell_4", 7.92500, 6.77500, "Group A"),
    ("cell_11", 7.87500, 6.77500, "Group A"),
    ("cell_18", 7.82500, 6.77500, "Group A"),
    ("cell_14", 7.87500, 6.92500, "Group B"),
    ("cell_19", 7.82500, 6.82500, "Group B"),
    ("cell_25", 7.77500, 6.77500, "Group C"),
    ("cell_32", 7.72500, 6.77500, "Group C"),
]

cell_df = pd.DataFrame(
    cell_records,
    columns=["cell", "latitude", "longitude", "group"]
)

cells = gpd.GeoDataFrame(
    cell_df,
    geometry=gpd.points_from_xy(
        cell_df["longitude"],
        cell_df["latitude"]
    ),
    crs="EPSG:4326"
)

# ============================================================
# 3. LOAD AND VALIDATE INPUT DATA
# ============================================================

def load_layer(key):
    path = FILES[key]

    if not path.exists():
        raise FileNotFoundError(
            f"Missing {key} dataset: {path}"
        )

    layer = gpd.read_file(path)

    if layer.empty:
        raise ValueError(f"{key} dataset is empty.")

    if layer.crs is None:
        raise ValueError(f"{key} dataset has no CRS.")

    return layer.to_crs("EPSG:4326")


print("=" * 65)
print("LOKOJA SPATIAL VERIFICATION")
print("=" * 65)

lga = load_layer("lga")
aoi = load_layer("aoi")
flood = load_layer("flood")
basins = load_layer("basins")
hydro_polygons = load_layer("hydro_polygons")
hydro_lines = load_layer("hydro_lines")

layers = {
    "Lokoja LGA": lga,
    "Local analysis extent": aoi,
    "2018 flood extent": flood,
    "HydroBASINS": basins,
    "Hydrography polygons": hydro_polygons,
    "Hydrography lines": hydro_lines,
}

print("\nINPUT DATASET CHECK")
for name, layer in layers.items():
    print(
        f"{name}: {len(layer)} features | "
        f"CRS: {layer.crs}"
    )

# ============================================================
# 4. IDENTIFY NAMED RIVER POLYGONS
# ============================================================

if "name" not in hydro_polygons.columns:
    raise ValueError(
        "Expected 'name' field in hydrography polygons."
    )

hydro_polygons["name_clean"] = (
    hydro_polygons["name"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
)

named_rivers = hydro_polygons[
    hydro_polygons["name_clean"].isin(["niger", "benue"])
].copy()

named_rivers["river_label"] = (
    named_rivers["name_clean"].str.title()
)

print("\nNAMED HYDROGRAPHY")
print(named_rivers["river_label"].value_counts())

# ============================================================
# 5. SPATIAL VERIFICATION
# ============================================================

lga_union = lga.geometry.union_all()
aoi_union = aoi.geometry.union_all()
flood_union = flood.geometry.union_all()

cells["inside_lga"] = cells.geometry.intersects(lga_union)
cells["inside_local_aoi"] = cells.geometry.intersects(aoi_union)
cells["intersects_2018_flood"] = cells.geometry.intersects(
    flood_union
)

# Distances in metres, not degrees.
cells_m = cells.to_crs(METRIC_CRS)
rivers_m = named_rivers.to_crs(METRIC_CRS)
basins_m = basins.to_crs(METRIC_CRS)

nearest_names = []
nearest_distances = []
intersecting_rivers = []
intersecting_basin_counts = []
intersecting_basin_ids = []

for _, cell in cells_m.iterrows():

    # Nearest named hydrography polygon.
    river_distances = rivers_m.geometry.distance(
        cell.geometry
    )

    nearest_index = river_distances.idxmin()

    nearest_names.append(
        rivers_m.loc[nearest_index, "river_label"]
    )

    nearest_distances.append(
        float(river_distances.loc[nearest_index])
    )

    # Actual polygon intersections.
    touching = rivers_m[
        rivers_m.geometry.intersects(cell.geometry)
    ]

    intersecting_rivers.append(
        ";".join(sorted(touching["river_label"].unique()))
        if not touching.empty else "None"
    )

    # HydroBASINS polygons intersecting the cell point.
    basin_matches = basins_m[
        basins_m.geometry.intersects(cell.geometry)
    ]

    intersecting_basin_counts.append(len(basin_matches))

    if "HYBAS_ID" in basin_matches.columns:
        intersecting_basin_ids.append(
            ";".join(
                basin_matches["HYBAS_ID"].astype(str).tolist()
            )
        )
    else:
        intersecting_basin_ids.append("Not available")

cells["nearest_named_hydrography"] = nearest_names
cells["nearest_hydrography_distance_m"] = nearest_distances
cells["intersecting_named_hydrography"] = intersecting_rivers
cells["intersecting_hydrobasin_count"] = intersecting_basin_counts
cells["intersecting_hydrobasin_ids"] = intersecting_basin_ids

# Save the spatial inventory.
inventory_columns = [
    "cell",
    "group",
    "latitude",
    "longitude",
    "inside_lga",
    "inside_local_aoi",
    "intersects_2018_flood",
    "intersecting_named_hydrography",
    "nearest_named_hydrography",
    "nearest_hydrography_distance_m",
    "intersecting_hydrobasin_count",
    "intersecting_hydrobasin_ids",
]

cells.drop(columns="geometry")[inventory_columns].to_csv(
    INVENTORY,
    index=False
)

print("\nCANDIDATE CELL VERIFICATION")
print(
    cells[inventory_columns].to_string(index=False)
)

# ============================================================
# 6. REGIONAL HYDROLOGICAL STUDY-AREA MAP
# ============================================================

fig, ax = plt.subplots(figsize=(12, 11))

# Complete 297-feature upstream network.
basins.boundary.plot(
    ax=ax,
    color="darkgrey",
    linewidth=0.45,
    alpha=0.75,
    label="HydroBASINS upstream catchments",
    zorder=1
)

# Lokoja LGA.
lga.boundary.plot(
    ax=ax,
    color="black",
    linewidth=1.7,
    label="Lokoja LGA",
    zorder=3
)

# Local analysis extent.
aoi.boundary.plot(
    ax=ax,
    color="blue",
    linewidth=1.5,
    linestyle="--",
    label="Provisional local analysis extent",
    zorder=4
)

# Candidate GloFAS cells.
group_styles = {
    "Group A": ("red", "o"),
    "Group B": ("green", "s"),
    "Group C": ("magenta", "^"),
}

for group_name, (color, marker) in group_styles.items():
    subset = cells[cells["group"] == group_name]

    subset.plot(
        ax=ax,
        color=color,
        marker=marker,
        markersize=65,
        edgecolor="black",
        linewidth=0.6,
        label=f"{group_name} GloFAS cells",
        zorder=6
    )

# Mark the local map window on the regional overview.
ax.add_patch(
    Rectangle(
        (west if "west" in globals() else LOCAL_BOUNDS[0],
         LOCAL_BOUNDS[1]),
        LOCAL_BOUNDS[2] - LOCAL_BOUNDS[0],
        LOCAL_BOUNDS[3] - LOCAL_BOUNDS[1],
        fill=False,
        edgecolor="blue",
        linewidth=1.2,
        linestyle=":",
        label="Local map extent",
        zorder=7
    )
)

# Add a Lokoja inset so the local study area remains legible
# at the regional network scale.
inset = fig.add_axes([0.66, 0.12, 0.27, 0.27])
basins_local_inset = gpd.clip(
    basins,
    gpd.GeoDataFrame(
        geometry=[box(*LOCAL_BOUNDS)],
        crs="EPSG:4326"
    )
)
basins_local_inset.boundary.plot(
    ax=inset, color="lightgrey", linewidth=0.35
)
lga.boundary.plot(ax=inset, color="black", linewidth=1.0)
aoi.boundary.plot(
    ax=inset, color="blue", linewidth=0.9, linestyle="--"
)
for group_name, (color, marker) in group_styles.items():
    cells[cells["group"] == group_name].plot(
        ax=inset, color=color, marker=marker,
        markersize=24, edgecolor="black", linewidth=0.4
    )
inset.set_xlim(LOCAL_BOUNDS[0], LOCAL_BOUNDS[2])
inset.set_ylim(LOCAL_BOUNDS[1], LOCAL_BOUNDS[3])
inset.set_title("Lokoja local detail", fontsize=8)
inset.set_xticks([])
inset.set_yticks([])
inset.set_facecolor("white")
inset.patch.set_alpha(0.95)

# Label the LGA near its centroid.
lga_centroid = lga.to_crs(METRIC_CRS).geometry.union_all().centroid
lga_centroid_wgs84 = gpd.GeoSeries(
    [lga_centroid], crs=METRIC_CRS
).to_crs("EPSG:4326").iloc[0]

ax.annotate(
    "Lokoja",
    xy=(lga_centroid_wgs84.x, lga_centroid_wgs84.y),
    xytext=(7, 7),
    textcoords="offset points",
    fontsize=10,
    fontweight="bold"
)

ax.set_title(
    "Regional Hydrological Study Area\n"
    "Lokoja and Combined Upstream HydroBASINS Network",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.grid(alpha=0.25, linestyle="--")
ax.legend(loc="best", fontsize=8)
ax.set_aspect("equal", adjustable="datalim")

fig.text(
    0.01, 0.01,
    "Sources: HydroBASINS v1; UN SALB Nigeria; Copernicus EMSR314_02. "
    "Candidate GloFAS points are modelled grid locations. "
    "Display CRS: EPSG:4326.",
    fontsize=7, color="dimgray"
)
fig.tight_layout(rect=[0, 0.035, 1, 1])
fig.savefig(REGIONAL_MAP, dpi=300, bbox_inches="tight")
plt.close(fig)

# ============================================================
# 7. LOCAL STUDY-AREA MAP
# ============================================================

west, south, east, north = LOCAL_BOUNDS
local_window = box(west, south, east, north)

# Clip only for visual display.
basins_local = gpd.clip(
    basins,
    gpd.GeoDataFrame(
        geometry=[local_window],
        crs="EPSG:4326"
    )
)

hydro_lines_local = gpd.clip(
    hydro_lines,
    gpd.GeoDataFrame(
        geometry=[local_window],
        crs="EPSG:4326"
    )
)

hydro_polygons_local = gpd.clip(
    hydro_polygons,
    gpd.GeoDataFrame(
        geometry=[local_window],
        crs="EPSG:4326"
    )
)

fig, ax = plt.subplots(figsize=(13, 11))

# Local catchment boundaries.
basins_local.boundary.plot(
    ax=ax,
    color="grey",
    linewidth=0.65,
    alpha=0.65,
    label="HydroBASINS catchment boundaries",
    zorder=1
)

# Flood extent.
flood.plot(
    ax=ax,
    color="lightskyblue",
    edgecolor="steelblue",
    linewidth=0.35,
    alpha=0.55,
    label="September 2018 flood extent",
    zorder=2
)

# LGA and provisional AOI.
lga.boundary.plot(
    ax=ax,
    color="black",
    linewidth=1.7,
    label="Lokoja LGA boundary",
    zorder=3
)

aoi.boundary.plot(
    ax=ax,
    color="blue",
    linewidth=1.4,
    linestyle="--",
    label="Provisional local analysis extent",
    zorder=4
)

# Named river polygons.
for river_name, color in [
    ("Niger", "darkorange"),
    ("Benue", "purple"),
]:
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
            zorder=5
        )

# Hydrography lines. Their names are Unknown in source data.
if not hydro_lines_local.empty:
    hydro_lines_local.plot(
        ax=ax,
        color="deepskyblue",
        linewidth=1.0,
        alpha=0.9,
        label="Mapped hydrography lines (unnamed)",
        zorder=6
    )

# Candidate cells and labels.
for group_name, (color, marker) in group_styles.items():
    subset = cells[cells["group"] == group_name]

    subset.plot(
        ax=ax,
        color=color,
        marker=marker,
        markersize=100,
        edgecolor="black",
        linewidth=0.8,
        label=f"{group_name} GloFAS cells",
        zorder=8
    )

    label_offsets = {
        "cell_4": (7, 9),
        "cell_11": (7, 9),
        "cell_18": (8, 7),
        "cell_14": (7, 8),
        "cell_19": (7, 8),
        "cell_25": (8, 7),
        "cell_32": (8, 7),
    }

    for _, row in subset.iterrows():
        ax.annotate(
            row["cell"].replace("cell_", ""),
            xy=(row.geometry.x, row.geometry.y),
            xytext=label_offsets[row["cell"]],
            textcoords="offset points",
            fontsize=9,
            fontweight="bold",
            zorder=9
        )

ax.set_xlim(west, east)
ax.set_ylim(south, north)

ax.set_title(
    "Lokoja Local Study Area\n"
    "Flood Extent, Hydrography and GloFAS Candidate Cells",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.grid(alpha=0.3, linestyle="--")
ax.legend(loc="best", fontsize=8)
ax.set_aspect("equal", adjustable="box")

fig.text(
    0.01, 0.01,
    "Sources: Copernicus EMSR314_02 hydrography and 2018 flood delineation; "
    "UN SALB Nigeria; HydroBASINS v1; GloFAS historical grid locations. "
    "Display CRS: EPSG:4326. Distances in inventory: EPSG:32632.",
    fontsize=7, color="dimgray"
)
fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig(LOCAL_MAP, dpi=300, bbox_inches="tight")
plt.close(fig)

# ============================================================
# 8. SUMMARY REPORT
# ============================================================

summary_lines = [
    "LOKOJA SPATIAL VERIFICATION SUMMARY",
    "=" * 60,
    f"LGA features: {len(lga)}",
    f"Local analysis extent features: {len(aoi)}",
    f"2018 flood features: {len(flood)}",
    f"HydroBASINS features: {len(basins)}",
    f"Hydrography polygon features: {len(hydro_polygons)}",
    f"Hydrography line features: {len(hydro_lines)}",
    f"Named Niger polygons: {(named_rivers['river_label'] == 'Niger').sum()}",
    f"Named Benue polygons: {(named_rivers['river_label'] == 'Benue').sum()}",
    f"GloFAS candidate cells: {len(cells)}",
    f"Cells intersecting LGA: {int(cells['inside_lga'].sum())}",
    f"Cells intersecting local AOI: {int(cells['inside_local_aoi'].sum())}",
    f"Cells intersecting 2018 flood footprint: {int(cells['intersects_2018_flood'].sum())}",
    "",
    "IMPORTANT LIMITATIONS",
    "- HydroBASINS polygons represent catchments, not river channels.",
    "- The local analysis extent is provisional and event-derived.",
    "- Hydrography line names are Unknown in the source data.",
    "- Spatial proximity does not establish GloFAS river attribution.",
    "- GloFAS grid cells are modelled estimates, not in-situ gauges.",
    "",
    f"Regional map: {REGIONAL_MAP}",
    f"Local map: {LOCAL_MAP}",
    f"Cell inventory: {INVENTORY}",
]

SUMMARY.write_text("\n".join(summary_lines))

print("\n" + "=" * 65)
print("SPATIAL VERIFICATION COMPLETED")
print("=" * 65)
print("\nRegional map:", REGIONAL_MAP)
print("Local map:", LOCAL_MAP)
print("Inventory:", INVENTORY)
print("Summary:", SUMMARY)
print("\n" + "\n".join(summary_lines))
