cat > data/processed/glofas/glofas_processing_log.md <<'EOF'
# GloFAS Processing Log — Lokoja

**Workflow date:** 2026-11-27  
**Study area:** Lokoja, Kogi State, Nigeria  
**Status:** Initial single-file inspection and candidate-cell preparation completed; historical-series validation and river-network association remain unresolved.

## 1. Sources and inventory

- GRIB file inspected: `data/raw/glofas/extracted/data.grib`
- AOI shapefile: `data/raw/lokoja_lga_extracted/lokoja_lga_utm32n.shp`
- Hydrography line layer: `data/raw/EMSR314_02_extracted/EMSR314_02LOKOJA_DEL_v1_hydrography_l.shp`
- Repository inventory showed GloFAS ZIP archives organized for 2015–2020 under `data/raw/glofas/multiyear/`, plus September 2018 archives in `data/raw/glofas/`.
- The extracted GRIB file was inspected directly. The exact GloFAS product/version and original download/source location were not established from the inspected metadata.

## 2. GRIB structure and metadata

The inspected file contains **one GRIB2 message**. An earlier preliminary message-count statement of 365 was incorrect; the direct Codespaces inspection returned one message.

- Variable: `avg_dis`
- Description: Time-mean discharge from rivers or streams
- Units: `m**3 s**-1` (m³/s)
- Reference date/time: 2018-09-15 00:00
- Validity date/time: 2018-09-16 00:00
- Averaging period: steps 0–24 (`stepType=avg`, `stepRange=0-24`)
- Grid type: `regular_ll`
- Grid dimensions: 7 × 6; 42 grid points
- Coordinate order: longitude, latitude
- Grid spacing: 0.05° × 0.05° (approximately 5.5 km)
- Missing-value marker: 9999
- Bitmap: not present (`bitmapPresent=0`)
- Missing values reported: 0
- `qualityControl` and `quality` keys: unavailable
- No separate quality-flag field was identified.

## 3. Discharge-value checks

For the 42 grid values in the inspected message:

- Minimum: 0 m³/s
- Median: 0.0390625 m³/s
- Mean: 3539.6640625 m³/s
- Maximum: 19711.78125 m³/s
- Zero values: 9
- Negative values: 0
- Missing values detected: 0

No arbitrary discharge threshold was applied. The large values were retained as reported and are not, by themselves, proof of a cell’s river-network association.

## 4. Time-series validation

- Message count: 1
- Validity timestamp: 2018-09-16 00:00
- Duplicate timestamps within this file: none; only one message exists.
- Historical date continuity, gaps, and duplicate timestamps across dates cannot be tested from this single-message file.
- Therefore, this file does not constitute a validated historical time series.

## 5. Candidate-cell selection

Candidate rule: retain grid points whose **point centers fall within the Lokoja AOI**. The rule is spatial; discharge magnitude was not used as a selection criterion.

Ten grid-point centers were reported inside the AOI:

| Cell ID | Longitude | Latitude | Discharge (m³/s) |
|---|---:|---:|---:|
| GLOFAS_01 | 6.625 | 7.925 | 0.015625 |
| GLOFAS_02 | 6.675 | 7.925 | 0.015625 |
| GLOFAS_03 | 6.725 | 7.925 | 0 |
| GLOFAS_04 | 6.775 | 7.925 | 10829.046875 |
| GLOFAS_08 | 6.625 | 7.875 | 0 |
| GLOFAS_09 | 6.675 | 7.875 | 0.03125 |
| GLOFAS_10 | 6.725 | 7.875 | 0.15625 |
| GLOFAS_11 | 6.775 | 7.875 | 10827.109375 |
| GLOFAS_17 | 6.725 | 7.825 | 0.109375 |
| GLOFAS_24 | 6.725 | 7.775 | 10837.515625 |

The AOI test used grid-point centers. It does not test whether complete grid-cell footprints intersect the AOI.

## 6. Spatial alignment

- GRIB grid coordinates: geographic longitude/latitude, EPSG:4326.
- AOI shapefile CRS: EPSG:32632; it was reprojected for the point-in-polygon comparison.
- Hydrography line layer CRS: EPSG:4326; it was reprojected to EPSG:32632 for distance calculations.
- Candidate points rechecked inside AOI: 10 of 10.
- The reported distances are from candidate point centers to the nearest mapped hydrography line clipped to the AOI. They are proximity measurements, not proof of hydrological connectivity.

| Cell ID | Distance to nearest mapped hydrography line |
|---|---:|
| GLOFAS_01 | 8.515196 km |
| GLOFAS_02 | 4.082851 km |
| GLOFAS_03 | 2.931181 km |
| GLOFAS_04 | 0.418469 km |
| GLOFAS_08 | 11.849515 km |
| GLOFAS_09 | 9.195814 km |
| GLOFAS_10 | 5.345917 km |
| GLOFAS_11 | 0.382462 km |
| GLOFAS_17 | 4.068788 km |
| GLOFAS_24 | 1.091184 km |

The hydrography line layer has 22 features and fields `obj_type`, `name`, `notation`, `or_src_id`, `cd_value`, and `geometry`. The provided inspection output did not include attribute values identifying the Niger or Benue. River-specific association and hydrological connectivity therefore remain unconfirmed.

## 7. Working outputs

Raw source files were not modified. Standardized working outputs were saved separately under:

`data/processed/glofas/validated_working/`

- `grid_values_standardized.csv`
- `candidate_cells_standardized.csv`
- `spatial_alignment_standardized.csv`
- `provenance.json`

The provenance file records source paths, SHA-256 checksums, GRIB metadata, and validation counts. The candidate IDs and coordinates were checked against the GRIB grid by the output-generation script.

## 8. Exceptions, limitations, and decisions

1. The inspected GRIB file has one message, so historical time-series checks cannot be completed from it.
2. Exact GloFAS product/version and original download/source location remain to be documented.
3. Quality-control/quality keys were unavailable; no independent quality flags were verified.
4. Candidate selection uses grid-point centers, not complete grid-cell footprints.
5. Distance to mapped hydrography does not establish that a cell is on the Niger or Benue or is hydrologically connected to either.
6. The raw data and source shapefiles were retained unchanged.
7. No discharge-based exclusion threshold was applied.

## 9. Overall status

- **Completed for the inspected file:** GRIB structure and units, value summary, candidate point-center selection, AOI point check, and creation of traceable working outputs.
- **Partially completed:** spatial alignment and single-message time validation.
- **Still required:** identify and document the exact GloFAS product/version/source; inspect the multiyear archives and validate the complete historical series; establish river-specific association using suitable hydrography attributes or a documented network method.
EOF