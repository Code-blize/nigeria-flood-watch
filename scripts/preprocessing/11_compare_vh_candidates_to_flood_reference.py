from pathlib import Path
import csv

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.features import rasterize

RASTER = Path(
    "data/processed/sentinel1_lokoja_2018_sample_median3.tif"
)
REFERENCE = Path(
    "data/processed/lokoja_2018_flood_extent.geojson"
)
OUT_DIR = Path("data/processed/sentinel1_vh_candidate_masks")
CSV_OUT = Path("data/processed/sentinel1_vh_reference_comparison.csv")

# Exploratory cutoffs only; not validated water thresholds.
THRESHOLDS_DB = [-20, -18, -16, -14]

OUT_DIR.mkdir(parents=True, exist_ok=True)

# Load the flood-reference polygons and reproject them to the raster CRS.
flood = gpd.read_file(REFERENCE)

with rasterio.open(RASTER) as src:
    if flood.crs is None:
        raise ValueError("The flood-reference file has no CRS.")

    flood = flood.to_crs(src.crs)
    geometries = [
        geom for geom in flood.geometry
        if geom is not None and not geom.is_empty
    ]
    if not geometries:
        raise ValueError("No usable geometries found in flood-reference file.")

    # Rasterize polygons using pixel centers (all_touched=False).
    reference_mask = rasterize(
        ((geom, 1) for geom in geometries),
        out_shape=(src.height, src.width),
        transform=src.transform,
        fill=0,
        all_touched=False,
        dtype="uint8",
    ).astype(bool)

    vh = src.read(2, masked=True).filled(np.nan).astype(np.float32)
    valid = np.isfinite(vh)

    # Compare only where VH is valid.
    reference_valid = reference_mask & valid
    reference_pixel_count = int(reference_valid.sum())

    if reference_pixel_count == 0:
        raise ValueError("No valid VH pixels fall inside the reference polygons.")

    pixel_area_m2 = abs(
        src.transform.a * src.transform.e
        - src.transform.b * src.transform.d
    )

    profile = src.profile.copy()
    profile.update(
        count=1,
        dtype="uint8",
        nodata=255,
        compress="deflate",
    )

    rows = []

    for threshold in THRESHOLDS_DB:
        candidate = valid & (vh <= threshold)
        overlap = candidate & reference_mask

        candidate_count = int(candidate.sum())
        overlap_count = int(overlap.sum())
        candidate_outside_reference = int((candidate & ~reference_mask).sum())
        reference_not_candidate = int((reference_valid & ~candidate).sum())

        candidate_share_inside_reference = (
            overlap_count / candidate_count * 100
            if candidate_count else 0.0
        )
        reference_covered_by_candidate = (
            overlap_count / reference_pixel_count * 100
        )

        # 1 = candidate, 0 = valid non-candidate, 255 = missing data.
        output_mask = np.full(vh.shape, 255, dtype=np.uint8)
        output_mask[valid] = 0
        output_mask[candidate] = 1

        output_path = OUT_DIR / f"vh_candidate_le_{abs(threshold)}db.tif"
        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(output_mask, 1)
            dst.set_band_description(1, f"VH <= {threshold} dB candidate")

        rows.append({
            "threshold_db": threshold,
            "valid_reference_pixels": reference_pixel_count,
            "candidate_pixels": candidate_count,
            "candidate_area_km2": candidate_count * pixel_area_m2 / 1_000_000,
            "candidate_pixels_inside_reference": overlap_count,
            "candidate_area_inside_reference_km2":
                overlap_count * pixel_area_m2 / 1_000_000,
            "candidate_share_inside_reference_percent":
                round(candidate_share_inside_reference, 4),
            "reference_covered_by_candidate_percent":
                round(reference_covered_by_candidate, 4),
            "candidate_pixels_outside_reference": candidate_outside_reference,
            "reference_pixels_not_candidate": reference_not_candidate,
            "interpretation_note":
                "Exploratory overlap only; outside-reference pixels are not "
                "automatically false detections."
        })

with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("Saved candidate masks:")
for threshold in THRESHOLDS_DB:
    print(f"  {OUT_DIR / f'vh_candidate_le_{abs(threshold)}db.tif'}")

print(f"\nSaved comparison table: {CSV_OUT}")
print("\nComparison results:")
for row in rows:
    print(
        f"VH <= {row['threshold_db']} dB: "
        f"candidate={row['candidate_pixels']:,} pixels; "
        f"inside reference={row['candidate_pixels_inside_reference']:,}; "
        f"reference covered={row['reference_covered_by_candidate_percent']}%; "
        f"candidate inside reference={row['candidate_share_inside_reference_percent']}%"
    )