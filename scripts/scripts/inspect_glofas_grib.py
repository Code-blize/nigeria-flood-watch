from pathlib import Path
from collections import Counter
import math

from eccodes import (
    codes_grib_new_from_file,
    codes_get,
    codes_get_array,
    codes_release,
)

# Adjust this path only if your GRIB file is stored elsewhere.
GRIB_PATH = Path("data/raw/glofas/extracted/data.grib")

if not GRIB_PATH.exists():
    raise FileNotFoundError(
        f"Could not find {GRIB_PATH.resolve()}. "
        "Check the file path and update GRIB_PATH."
    )

def get_key(message, key):
    """Return a GRIB metadata value, or 'unavailable' if the key is absent."""
    try:
        return codes_get(message, key)
    except Exception:
        return "unavailable"

message_count = 0
short_names = Counter()
units = Counter()
dates = Counter()
missing_counts = []
sample_messages = []

with GRIB_PATH.open("rb") as grib_file:
    while True:
        message = codes_grib_new_from_file(grib_file)
        if message is None:
            break

        message_count += 1

        short_name = get_key(message, "shortName")
        unit = get_key(message, "units")
        valid_date = get_key(message, "validDate")
        missing_value = get_key(message, "missingValue")

        short_names[str(short_name)] += 1
        units[str(unit)] += 1
        dates[str(valid_date)] += 1

        try:
            values = codes_get_array(message, "values")
            if missing_value != "unavailable":
                missing_count = sum(
                    1 for value in values
                    if math.isclose(
                        float(value),
                        float(missing_value),
                        rel_tol=0.0,
                        abs_tol=1e-12,
                    )
                )
            else:
                missing_count = "missingValue key unavailable"

            missing_counts.append(missing_count)
        except Exception:
            missing_counts.append("could not read values")

        if len(sample_messages) < 5:
            sample_messages.append({
                "message": message_count,
                "shortName": short_name,
                "name": get_key(message, "name"),
                "units": unit,
                "dataDate": get_key(message, "dataDate"),
                "dataTime": get_key(message, "dataTime"),
                "validDate": valid_date,
                "stepType": get_key(message, "stepType"),
                "startStep": get_key(message, "startStep"),
                "endStep": get_key(message, "endStep"),
                "typeOfLevel": get_key(message, "typeOfLevel"),
                "numberOfPoints": get_key(message, "numberOfPoints"),
                "Ni": get_key(message, "Ni"),
                "Nj": get_key(message, "Nj"),
                "missingValue": missing_value,
            })

        codes_release(message)

print(f"File: {GRIB_PATH}")
print(f"Total messages: {message_count}")
print(f"Variable short names and message counts: {dict(short_names)}")
print(f"Units and message counts: {dict(units)}")
print(f"Valid dates and message counts: {dict(dates)}")
print("\nFirst five messages:")
for item in sample_messages:
    print(item)

print("\nMissing-value check per message:")
print(missing_counts)