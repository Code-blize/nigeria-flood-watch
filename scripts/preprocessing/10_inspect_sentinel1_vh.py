from pathlib import Path

import numpy as np
import rasterio
import matplotlib.pyplot as plt

INPUT = Path(
    "data/processed/sentinel1_lokoja_2018_sample_median3.tif"
)
OUTPUT = Path(
    "data/processed/sentinel1_vh_distribution.png"
)

with rasterio.open(INPUT) as src:
    vh = src.read(2, masked=True).compressed()

vh = vh[np.isfinite(vh)]

print(f"Valid VH pixels: {vh.size:,}")
print("VH values are in dB.")
for p in [1, 5, 10, 25, 50, 75, 90, 95, 99]:
    print(f"{p}th percentile: {np.percentile(vh, p):.3f} dB")

plt.figure(figsize=(10, 5))
plt.hist(vh, bins=150, color="steelblue", edgecolor="none")
plt.xlabel("VH backscatter (dB)")
plt.ylabel("Pixel count")
plt.title("Sentinel-1 VH value distribution — filtered test raster")
plt.grid(axis="y", alpha=0.25)
plt.tight_layout()

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(OUTPUT, dpi=150)
plt.close()

print(f"\nSaved histogram to: {OUTPUT}")