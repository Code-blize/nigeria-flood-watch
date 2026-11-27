from pathlib import Path
import hashlib
import json

import pandas as pd
from eccodes import (
    codes_grib_new_from_file,
    codes_get,
    codes_get_array,
    codes_release,
)

ROOT = Path(".")
GRIB_PATH = ROOT / "data/raw/glofas/extracted/data.grib"
AOI_PATH = ROOT / "data/raw/lokoja_lga_extracted/lokoja_lga_utm32n.shp"
HYDRO_PATH = ROOT / (
    "data/raw/EMSR314_02_extracted/"
    "EMSR314_02LOKOJA_DEL_v1_hydrography_l.shp"
)

CANDIDATES_PATH = ROOT / (
    "data/processed/glofas/glofas_candidate_cells_documented.csv"
)
ALIGNMENT_PATH = ROOT / (
    "data/processed/glofas/glofas_spatial_alignment.csv"
)

OUT_DIR = ROOT / "data/processed/glofas/validated_working"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_file(path):
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path.resolve()}")


for source in [
    GRIB_PATH, AOI_PATH, HYDRO_PATH, CANDIDATES_PATH, ALIGNMENT_PATH
]:
    require_file(source)


# Read raw GRIB values and coordinates.
with GRIB_PATH.open("rb") as file:
    grib = codes_grib_new_from_file(file)

if grib is None:
    raise RuntimeError(f"No GRIB message found in {GRIB_PATH}")

grid_values = pd.DataFrame({
    "cell_id": [
        f"GLOFAS_{i:02d}"
        for i in range(1, len(codes_get_array(grib, "values")) + 1)
    ],
    "longitude": codes_get_array(grib, "longitudes"),
    "latitude": codes_get_array(grib, "latitudes"),
    "discharge_m3_s": codes_get_array(grib, "values"),
})

grib_metadata = {
    "short_name": codes_get(grib, "shortName"),
    "variable_name": codes_get(grib, "name"),
    "units": codes_get(grib, "units"),
    "reference_date": str(codes_get(grib, "dataDate")),
    "reference_time": str(codes_get(grib, "dataTime")),
    "validity_date": str(codes_get(grib, "validityDate")),
    "validity_time": str(codes_get(grib, "validityTime")),
    "step_type": codes_get(grib, "stepType"),
    "start_step": codes_get(grib, "startStep"),
    "end_step": codes_get(grib, "endStep"),
    "grid_type": codes_get(grib, "gridType"),
    "grid_resolution_degrees": "0.05 x 0.05",
}
codes_release(grib)

if len(grid_values) != 42:
    raise ValueError(f"Expected 42 grid points; found {len(grid_values)}")

grid_values.to_csv(OUT_DIR / "grid_values_standardized.csv", index=False)


# Load the previously documented candidate cells and spatial check.
candidates = pd.read_csv(CANDIDATES_PATH)
alignment = pd.read_csv(ALIGNMENT_PATH)

if len(candidates) != 10:
    raise ValueError(f"Expected 10 documented candidates; found {len(candidates)}")

if candidates["cell_id"].duplicated().any():
    raise ValueError("Duplicate candidate cell IDs found.")

if alignment["cell_id"].duplicated().any():
    raise ValueError("Duplicate cell IDs in spatial-alignment file.")

# Confirm the candidate IDs and coordinates match the GRIB grid.
check = candidates[["cell_id", "longitude", "latitude"]].merge(
    grid_values[["cell_id", "longitude", "latitude"]],
    on="cell_id",
    suffixes=("_candidate", "_grib"),
    how="left",
    validate="one_to_one",
)

if check["longitude_grib"].isna().any():
    raise ValueError("A candidate ID is missing from the GRIB grid.")

if not (
    (check["longitude_candidate"] == check["longitude_grib"]).all()
    and (check["latitude_candidate"] == check["latitude_grib"]).all()
):
    raise ValueError("Candidate coordinates do not match the GRIB grid.")

# Join spatial checks; retain explicit unresolved river-network status.
candidate_working = candidates.merge(
    alignment[
        [
            "cell_id",
            "inside_aoi_check",
            "distance_to_hydro_m",
            "distance_to_hydro_km",
        ]
    ],
    on="cell_id",
    how="left",
    validate="one_to_one",
)

candidate_working["river_network_relationship"] = (
    "Proximity to mapped hydrography measured; Niger/Benue association "
    "and hydrological connectivity not confirmed."
)

candidate_working.to_csv(
    OUT_DIR / "candidate_cells_standardized.csv",
    index=False,
)

alignment.to_csv(
    OUT_DIR / "spatial_alignment_standardized.csv",
    index=False,
)


# Record source files, checksums, and key metadata for traceability.
source_files = [
    GRIB_PATH,
    AOI_PATH,
    HYDRO_PATH,
    CANDIDATES_PATH,
    ALIGNMENT_PATH,
]

provenance = {
    "workflow": "GloFAS preparation — validated working outputs",
    "raw_files_modified": False,
    "grib_metadata": grib_metadata,
    "source_files": [
        {
            "path": str(path),
            "sha256": sha256(path),
        }
        for path in source_files
    ],
    "outputs": [
        "grid_values_standardized.csv",
        "candidate_cells_standardized.csv",
        "spatial_alignment_standardized.csv",
    ],
    "validation": {
        "grid_point_count": int(len(grid_values)),
        "candidate_cell_count": int(len(candidate_working)),
        "candidate_ids_and_coordinates_match_grib": True,
        "river_network_association": "Not confirmed",
    },
}

with (OUT_DIR / "provenance.json").open("w", encoding="utf-8") as file:
    json.dump(provenance, file, indent=2)

print("Working outputs created in:", OUT_DIR)
for path in sorted(OUT_DIR.iterdir()):
    print("-", path.name)