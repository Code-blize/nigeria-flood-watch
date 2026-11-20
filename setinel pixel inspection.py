import rasterio
import numpy as np

path = "data/raw/sentinel1/sentinel1_lokoja_2018_sample.tif"

with rasterio.open(path) as src:
    for i in range(1, src.count + 1):
        data = src.read(i, masked=True)
        values = data.compressed()
        finite = values[np.isfinite(values)]

        print(f"\nBand {i}: {src.descriptions[i-1]}")
        print("Total pixels:", values.size)
        print("Finite pixels:", finite.size)
        print("NaN pixels:", np.isnan(values).sum())
        print("Infinite pixels:", np.isinf(values).sum())

        if finite.size:
            print("Minimum:", finite.min())
            print("Maximum:", finite.max())
            print("Mean:", finite.mean())
            print("Standard deviation:", finite.std())