import numpy as np
import rasterio

path = "data/processed/sentinel1_lokoja_2018_sample_median3.tif"

with rasterio.open(path) as src:
    print("Band order:", src.descriptions)
    print("CRS:", src.crs)
    print("Shape:", src.shape)

    for band_number, band_name in [(1, "VV"), (2, "VH")]:
        values = src.read(band_number, masked=True).compressed()
        values = values[np.isfinite(values)]

        print(f"\n{band_name} (dB)")
        for percentile in [1, 5, 25, 50, 75, 95, 99]:
            print(f"{percentile}th percentile: {np.percentile(values, percentile):.3f}")
        print(f"Mean: {values.mean():.3f}")
        print(f"Valid pixels: {values.size:,}")