
import json
from pathlib import Path
import requests

out_dir = Path("data/raw/osm")
out_dir.mkdir(parents=True, exist_ok=True)

url = "https://osm2cdr.com/api/geo-analysis/simplify"

payload = {
    "bbox": [6.713, 7.773, 6.767, 7.827],
    "params": {
        "layer": "roads",
        "tolerance_m": 1
    }
}

response = requests.post(url, json=payload, timeout=60)
response.raise_for_status()
data = response.json()

# Save the returned GeoJSON
with open(out_dir / "lokoja_roads_sample.geojson", "w") as f:
    json.dump(data["result"], f, indent=2)

# Save acquisition metadata
with open(out_dir / "lokoja_roads_sample_metadata.json", "w") as f:
    json.dump(data["meta"], f, indent=2)

print("Features:", data["meta"]["feature_count"])
print("Layer:", data["meta"]["layer"])
print("Snapshot:", data["meta"]["data_snapshot"])
print("Saved:", out_dir / "lokoja_roads_sample.geojson")
