from pathlib import Path

import numpy as np
import rasterio
import matplotlib.pyplot as plt

files = {
    "Original": Path("data/raw/sentinel1/sentinel1_lokoja_2018_sample.tif"),
    "Filtered": Path("data/processed/sentinel1_lokoja_2018_sample_median3.tif"),
}

out_dir = Path("data/processed/sentinel1_previews")
out_dir.mkdir(parents=True, exist_ok=True)

# Use the same display range for each matching band so the comparison is fair.
for band_number, band_name in [(1, "VV"), (2, "VH")]:
    arrays = {}

    for label, path in files.items():
        with rasterio.open(path) as src:
            arrays[label] = src.read(band_number, masked=True).filled(np.nan)

    combined = np.concatenate([
        a[np.isfinite(a)] for a in arrays.values()
    ])

    low, high = np.percentile(combined, [2, 98])

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    for ax, (label, array) in zip(axes, arrays.items()):
        ax.imshow(array, cmap="gray", vmin=low, vmax=high)
        ax.set_title(f"{label} — {band_name}")
        ax.axis("off")

    fig.suptitle(f"Sentinel-1 {band_name}: original vs. median-filtered")
    fig.tight_layout()

    output = out_dir / f"sentinel1_{band_name.lower()}_comparison.png"
    fig.savefig(output, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved: {output}")
