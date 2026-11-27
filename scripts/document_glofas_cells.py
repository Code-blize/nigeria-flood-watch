from pathlib import Path
import pandas as pd

INPUT = Path("data/processed/glofas/glofas_candidate_cells.csv")
OUTPUT = Path("data/processed/glofas/glofas_candidate_cells_documented.csv")

if not INPUT.exists():
    raise FileNotFoundError(f"Missing input file: {INPUT.resolve()}")

df = pd.read_csv(INPUT)

required = {"cell_id", "longitude", "latitude", "discharge_m3_s", "inside_aoi"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Input is missing required columns: {sorted(missing)}")

# Candidate rule for this step: grid-point center falls within the AOI.
candidates = df[df["inside_aoi"].astype(str).str.lower().isin(["true", "1"])].copy()

candidates["grid_resolution_degrees"] = "0.05° × 0.05°"
candidates["approx_grid_spacing_km"] = "about 5.5 km"
candidates["selection_rationale"] = (
    "Grid-point center falls within the Lokoja AOI; retained for spatial review."
)
candidates["aoi_relationship"] = "Point center inside AOI"
candidates["river_network_relationship"] = (
    "Pending overlay/check against hydrography; not established by this selection."
)

candidates = candidates[
    [
        "cell_id",
        "longitude",
        "latitude",
        "grid_resolution_degrees",
        "approx_grid_spacing_km",
        "selection_rationale",
        "aoi_relationship",
        "river_network_relationship",
        "discharge_m3_s",
    ]
]

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
candidates.to_csv(OUTPUT, index=False)

print(f"Documented candidate cells: {len(candidates)}")
print(candidates.to_string(index=False))
print(f"\nSaved: {OUTPUT}")