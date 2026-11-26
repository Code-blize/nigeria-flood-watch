## Step 7 — Record and preserve terrain products

### Study area
- AOI: 20 km buffer around [6.74, 7.80], converted to rectangular bounds
- Location: Lokoja, Kogi State, Nigeria

### Source
- DEM: NASADEM V001 (`NASA/NASADEM_HGT/001`)
- Elevation band: `elevation`
- Source CRS: EPSG:4326
- Source elevation units: metres

### Outputs
| Product | Expected CRS | Expected cell size | Status |
|---|---|---:|---|
| Raw elevation | EPSG:4326 | ~30.9 m nominal source resolution | Preserved |
| Standardized elevation | EPSG:32632 | 30 m | Exported; ArcGIS metadata checked |
| Slope | EPSG:32632 | 30 m | Exported; ArcGIS metadata checked |
| Aspect | EPSG:32632 | 30 m | **Not validated: ArcGIS reports EPSG:4326** |

### Validation notes
- Elevation and slope exports were reported in EPSG:32632 with 30 m cells.
- Aspect export metadata reports WGS 1984 / EPSG:4326 and cell size 30.
- The aspect CRS and cell-size units are inconsistent. Do not use this aspect raster for analysis until the CRS is corrected and verified.
- Keep the original export unchanged for traceability; create a corrected output with a new filename.

### Preservation
- Keep the original NASADEM source and raw export unchanged.
- Keep processed outputs, validation results, and the processing script together.
- Record the export filename and date for each product.
