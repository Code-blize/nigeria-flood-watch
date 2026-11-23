from pathlib import Path

import numpy as np
import rasterio
from scipy.ndimage import distance_transform_edt, median_filter

INPUT = Path("data/raw/sentinel1/sentinel1_lokoja_2018_sample.tif")
OUTPUT = Path("data/processed/sentinel1_lokoja_2018_sample_median3.tif")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with rasterio.open(INPUT) as src:
    profile = src.profile.copy()
    bands = src.read().astype(np.float32)

    filtered_bands = np.empty_like(bands)

    for band_index, band in enumerate(bands):
        valid = np.isfinite(band)

        if not valid.any():
            filtered_bands[band_index] = band
            continue

        # Sentinel-1 values are in dB. Convert to linear power before filtering.
        power = np.full(band.shape, np.nan, dtype=np.float32)
        power[valid] = 10 ** (band[valid] / 10)

        # Temporarily fill missing pixels from the nearest valid pixel so NaNs
        # do not interfere with the filter; restore the original missing mask after.
        nearest_indices = distance_transform_edt(
            ~valid, return_distances=False, return_indices=True
        )
        filled_power = power[tuple(nearest_indices)]

        filtered_power = median_filter(filled_power, size=3)
        filtered_db = 10 * np.log10(np.maximum(filtered_power, 1e-12))

        filtered_db[~valid] = np.nan
        filtered_bands[band_index] = filtered_db

    profile.update(dtype="float32", count=bands.shape[0], nodata=None)

    with rasterio.open(OUTPUT, "w", **profile) as dst:
        dst.write(filtered_bands)

print(f"Saved filtered test raster: {OUTPUT}")
