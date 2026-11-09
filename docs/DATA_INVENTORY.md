# NigeriaFloodWatch — Data Inventory

**Document version:** 0.1  
**Project:** NigeriaFloodWatch  
**Pilot study area:** Lokoja, Kogi State, Nigeria  
**Last updated:** 9 November 2026

## 1. Purpose

This document records the datasets considered, accessed and evaluated for NigeriaFloodWatch.

It tracks data sources, access methods, spatial and temporal characteristics, intended applications, limitations and acquisition status.

## 2. Administrative boundary data

| Attribute | Description |
|---|---|
| Dataset | Nigeria Administrative Boundaries |
| Provider | United Nations SALB |
| Source | https://salb.un.org/en/data/nga |
| Format | Shapefile |
| Access method | Manual download |
| Geographic coverage | Nigeria |
| Administrative level | LGA / second-level administrative units |
| Processing status | Lokoja LGA extracted |
| Working layer | `lokoja_lga_utm32n` |
| Working CRS | WGS 1984 UTM Zone 32N (EPSG:32632) |
| Calculated area | 3,181.16785 km² |

**Intended application:**
- Define the administrative pilot study area.
- Provide a reference boundary for clipping and spatial analysis.
- Support the organisation of flood exposure information.

**Quality-control note:** The area measurement is preliminary and should be checked against an independent boundary or area calculation.

## 3. Hydrological basin data

| Attribute | Description |
|---|---|
| Dataset | HydroBASINS Level 6 |
| Provider | WWF / HydroSHEDS |
| Earth Engine ID | `WWF/HydroSHEDS/v1/Basins/hybas_6` |
| Format | Earth Engine FeatureCollection |
| Access method | Google Earth Engine |
| Original coverage | Africa / global hydrological basin system |
| Working scale | Level 6 |
| Acquisition status | Successfully queried |
| Local exploration | Five features intersecting a 50 km search radius around the approximate Lokoja point |

### Important attributes

| Field | Intended interpretation |
|---|---|
| `HYBAS_ID` | Unique basin identifier |
| `NEXT_DOWN` | Next downstream basin identifier |
| `MAIN_BAS` | Main basin identifier |
| `UP_AREA` | Accumulated upstream contributing area (km²) |

### Initial findings

Five nearby basin records were returned.

Observed downstream identifiers:

- 1060022420
- 1060909890
- 0

All five records returned `MAIN_BAS = 1060022420`.

Observed upstream contributing areas ranged from 15,286.4 to 2,098,663.8 km².

These findings are exploratory. The Niger and Benue contributing catchments have not yet been conclusively identified.

### Intended application

- Reconstruct upstream/downstream drainage connectivity.
- Identify hydrological catchments contributing to Lokoja.
- Support selection of relevant GloFAS discharge information.
- Provide catchment context for rainfall and river-flow analysis.

### Limitations and pending checks

- Verify the interpretation of HydroBASINS attributes.
- Identify the basin containing the Lokoja location.
- Trace upstream connectivity for the Niger and Benue branches.
- Compare catchment relationships with river networks and GloFAS locations.
- Assess whether Level 6 provides sufficient spatial detail.

## 4. Other candidate datasets

| Dataset | Provider | Intended application | Status |
|---|---|---|---|
| Sentinel-1 GRD | Copernicus / Google Earth Engine | SAR observations and historical flood mapping | Pending |
| CHIRPS v3 | Climate Hazards Center | Historical rainfall | Pending |
| CHIRPS-GEFS | Climate Hazards Center | Forecast rainfall | Pending |
| GloFAS | Copernicus Emergency Management Service | Historical and forecast river discharge | Pending |
| SRTM DEM | NASA / USGS | Elevation and terrain analysis | Pending |
| OpenStreetMap | OpenStreetMap contributors | Roads, buildings and infrastructure exposure | Pending |
| UNOSAT flood products | UNOSAT | Historical satellite-derived flood extent | Pending |
| NIHSA / NIWA observations | Nigerian hydrological agencies | River-level and discharge observations | Availability verification pending |

## 5. Data acquisition principles

NigeriaFloodWatch will prioritise:

1. Official APIs and programmatic data access.
2. Google Earth Engine-hosted datasets.
3. Official cloud-hosted scientific datasets.
4. Manual downloads only when reliable programmatic access is unavailable.

All datasets must be assessed for:

- Spatial coverage and resolution.
- Temporal coverage and update frequency.
- Coordinate reference system.
- Data quality and completeness.
- Licensing and usage restrictions.
- Suitability for the intended prediction target.

## 6. Important modelling consideration

Observed satellite imagery, historical rainfall and forecast hydrological variables have different temporal meanings.

They must not be treated as interchangeable inputs.

For a genuine 72-hour flood prediction, model features must represent information available at the prediction issue time. Post-event observations must not leak into future prediction features.

