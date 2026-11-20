import rasterio
import numpy as np

path = "data/raw/srtm/srtm_lokoja_elevation_slope_aspect.tif"

with rasterio.open(path) as src:
    data = src.read(1)
    transform = src.transform

    row = 1336
    col = 0

    x, y = rasterio.transform.xy(transform, row, col)

    print("Last row centre coordinate:")
    print("Longitude:", x)
    print("Latitude:", y)

    print("\nRaster bounds:", src.bounds)
    print("Last row NaN count:", np.isnan(data[row]).sum())