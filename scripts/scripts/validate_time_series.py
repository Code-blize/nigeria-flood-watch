from pathlib import Path
from collections import Counter
from eccodes import codes_grib_new_from_file, codes_get, codes_release

path = Path("data/raw/glofas/extracted/data.grib")
records = []

with path.open("rb") as f:
    while True:
        msg = codes_grib_new_from_file(f)
        if msg is None:
            break

        def get(key):
            try:
                return codes_get(msg, key)
            except Exception:
                return None

        records.append({
            "dataDate": get("dataDate"),
            "dataTime": get("dataTime"),
            "validityDate": get("validityDate"),
            "validityTime": get("validityTime"),
            "stepType": get("stepType"),
            "startStep": get("startStep"),
            "endStep": get("endStep"),
        })
        codes_release(msg)

timestamps = [
    (r["validityDate"], r["validityTime"])
    for r in records
    if r["validityDate"] is not None and r["validityTime"] is not None
]

counts = Counter(timestamps)

print("Message count:", len(records))
print("Timestamp fields:", timestamps or "unavailable")
print("Duplicate timestamps:", [t for t, n in counts.items() if n > 1])
print("Record metadata:")
for record in records:
    print(record)

if len(records) == 1:
    print("Series validation: not possible from this single-message file.")