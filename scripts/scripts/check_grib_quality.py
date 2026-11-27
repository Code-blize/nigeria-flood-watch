from pathlib import Path
from eccodes import (
    codes_grib_new_from_file,
    codes_get,
    codes_release,
)

path = Path("data/raw/glofas/extracted/data.grib")

keys = [
    "shortName",
    "name",
    "units",
    "dataDate",
    "dataTime",
    "validityDate",
    "validityTime",
    "stepType",
    "startStep",
    "endStep",
    "stepRange",
    "typeOfStatisticalProcessing",
    "productDefinitionTemplateNumber",
    "bitmapPresent",
    "numberOfDataPoints",
    "numberOfValues",
    "numberOfCodedValues",
    "numberOfMissing",
    "missingValue",
    "qualityControl",
    "quality",
    "generatingProcessIdentifier",
]

with path.open("rb") as f:
    message = codes_grib_new_from_file(f)

if message is None:
    raise RuntimeError(f"No GRIB message found in {path}")

for key in keys:
    try:
        value = codes_get(message, key)
    except Exception:
        value = "unavailable"
    print(f"{key}: {value}")

codes_release(message)