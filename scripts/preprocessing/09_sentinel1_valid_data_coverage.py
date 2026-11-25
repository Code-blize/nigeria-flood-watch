from pathlib import Path
import json

import numpy as np
import rasterio

INPUT = Path(
    "data/processed/sentinel1_lokoja_2018_sample_median3.tif"
)
OUTPUT = Path(
    "data/processed/sentinel1_valid_data_coverage.json"
)

band_names = {1: "VV", 2: "VH"}

with rasterio.open(INPUT) as src:
    report = {
        "source_file": str(INPUT),
        "crs": str(src.crs),
        "width_pixels": src.width,
        "height_pixels": src.height,
        "band_count": src.count,
        "bands": {},
    }

    total_pixels = src.width * src.height

    for band_number, band_name in band_names.items():
        data = src.read(band_number, masked=True)
        valid = (~np.ma.getmaskarray(data)) & np.isfinite(data.data)

        valid_count = int(valid.sum())
        missing_count = int(total_pixels - valid_count)

        report["bands"][band_name] = {
            "band_number": band_number,
            "valid_pixels": valid_count,
            "missing_pixels": missing_count,
            "valid_percent": round(100 * valid_count / total_pixels, 6),
            "missing_percent": round(100 * missing_count / total_pixels, 6),
        }

    # Record the shared valid-data mask status.
    vv_valid = src.read(1, masked=True)
    vh_valid = src.read(2, masked=True)

    vv_mask = (~np.ma.getmaskarray(vv_valid)) & np.isfinite(vv_valid.data)
    vh_mask = (~np.ma.getmaskarray(vh_valid)) & np.isfinite(vh_valid.data)

    report["vv_vh_valid_masks_identical"] = bool(
        np.array_equal(vv_mask, vh_mask)
    )

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

print(json.dumps(report, indent=2))
print(f"\nSaved coverage report to: {OUTPUT}")