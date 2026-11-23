import numpy as np
import rasterio

files = {
    "original": "data/raw/sentinel1/sentinel1_lokoja_2018_sample.tif",
    "filtered": "data/processed/sentinel1_lokoja_2018_sample_median3.tif",
}

for name, path in files.items():
    with rasterio.open(path) as src:
        print(f"\n{name}: {path}")
        print("shape:", src.shape, "bands:", src.count, "CRS:", src.crs)
        for i in range(1, src.count + 1):
            band = src.read(i)
            valid = np.isfinite(band)
            print(
                f"band {i}: valid={valid.sum():,}, "
                f"min={np.nanmin(band):.3f}, "
                f"max={np.nanmax(band):.3f}, "
                f"mean={np.nanmean(band):.3f}, "
                f"std={np.nanstd(band):.3f}"
            )