
from pathlib import Path
import geopandas as gpd

# --------------------------------------------------
# INPUT DIRECTORY
# --------------------------------------------------

data_dir = Path("data/raw/EMSR314_02_extracted")

files = {
    "Hydrography polygons": (
        data_dir / "EMSR314_02LOKOJA_DEL_v1_hydrography_a.shp"
    ),
    "Hydrography lines": (
        data_dir / "EMSR314_02LOKOJA_DEL_v1_hydrography_l.shp"
    ),
}

# --------------------------------------------------
# INSPECT EACH LAYER
# --------------------------------------------------

for layer_name, file_path in files.items():

    print("\n" + "=" * 65)
    print(layer_name.upper())
    print("=" * 65)

    if not file_path.exists():
        print("FILE NOT FOUND:", file_path)
        continue

    gdf = gpd.read_file(file_path)

    print("\nFile:", file_path)
    print("Feature count:", len(gdf))
    print("CRS:", gdf.crs)
    print("Geometry types:")
    print(gdf.geometry.geom_type.value_counts())

    print("\nAttribute fields:")
    print(gdf.columns.tolist())

    # Display all non-geometry attributes.
    attributes = gdf.drop(columns="geometry")

    print("\nFirst 15 records:")
    print(attributes.head(15).to_string(index=False))

    # Identify records with potentially useful names.
    name_columns = [
        col for col in gdf.columns
        if any(term in col.lower() for term in [
            "name", "river", "water", "type", "class", "description"
        ])
    ]

    if name_columns:
        print("\nPotential river identification fields:")
        print(
            gdf[name_columns]
            .drop_duplicates()
            .to_string(index=False)
        )

print("\nHydrography inspection completed.")
