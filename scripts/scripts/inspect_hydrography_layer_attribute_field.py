import geopandas as gpd

path = "data/raw/EMSR314_02_extracted/EMSR314_02LOKOJA_DEL_v1_hydrography_l.shp"
hydro = gpd.read_file(path)

print("CRS:", hydro.crs)
print("Feature count:", len(hydro))
print("Fields:", hydro.columns.tolist())

for column in hydro.columns:
    if hydro[column].dtype == "object":
        print(f"\n{column} values:")
        print(hydro[column].dropna().astype(str).unique()[:50])