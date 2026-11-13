# NigeriaFloodWatch — Data Inventory

**Document version:** 0.2  
**Project:** NigeriaFloodWatch  
**Pilot study area:** Lokoja, Kogi State, Nigeria  
**Last updated:** 13 November 2026

---

## 1. Purpose

This document records the datasets considered, explored, acquired, and evaluated for **NigeriaFloodWatch**.

It tracks dataset identifiers, access methods, acquisition dates, spatial and temporal characteristics, licensing terms, known limitations, and storage status—explicitly distinguishing datasets **exported and retained in the repository** from those **explored in Google Earth Engine (GEE)** or pending acquisition.

---

## 2. Repository-Retained Datasets (Acquired & Exported)

These datasets have been downloaded or exported from GEE, passed initial quality assurance (QA), and are stored locally/in the project repository.

### 2.1 Administrative boundary data

| Attribute | Description |
|---|---|
| **Dataset** | Nigeria Administrative Boundaries (SALB) |
| **Dataset ID / Source** | `NGA_SALB` — [https://salb.un.org/en/data/nga](https://salb.un.org/en/data/nga) |
| **Provider** | United Nations Second Administrative Level Boundaries (UN SALB) |
| **Access method** | Manual download (Shapefile) |
| **Actual acquisition date** | Pre-9 November 2026 *(record exact download date)* |
| **Repository status** | **Retained in repository** (`lokoja_lga_utm32n`) |
| **Temporal validity** | 2000 – 8 August 2024 (latest listed update) |
| **Working CRS** | WGS 1984 UTM Zone 32N (`EPSG:32632`) |
| **Calculated area** | 3,181.16785 km² (Lokoja LGA) |
| **Licence** | **UN SALB Terms of Use** — Non-commercial use only; geometry or content modifications are prohibited without contributor consent |

* **Intended application:** Define the pilot study area boundary, clip spatial layers, and aggregate flood exposure metrics.
* **Known limitations & licensing risks:** 
  * Area calculation is preliminary and requires cross-checking against an independent reference boundary.
  * **Commercial restriction:** Current licence terms permit research use only and prohibit commercial redistribution or derivative boundary modification without explicit contributor consent. This must be resolved before deploying a commercial NigeriaFloodWatch product.

---

### 2.2 Hydrological basin data

| Attribute | Description |
|---|---|
| **Dataset** | HydroBASINS v1, Level 6 |
| **Dataset / GEE ID** | `WWF/HydroSHEDS/v1/Basins/hybas_6` |
| **Provider** | WWF / HydroSHEDS |
| **Access method** | Google Earth Engine programmatic trace and export (GeoJSON / CSV) |
| **Actual acquisition date** | 9–13 November 2026 *(confirm exact export timestamp)* |
| **Repository status** | **Exported and retained in repository** (297-feature network) |
| **Spatial resolution** | Derived from 15-arc-second HydroSHEDS core hydrography |
| **Licence** | **HydroSHEDS Terms of Use** — Free for scientific, educational, and commercial use with attribution |

#### Key attributes used
* `HYBAS_ID`: Unique basin identifier
* `NEXT_DOWN`: Next downstream basin identifier
* `MAIN_BAS`: Main terminal basin identifier (`1060022420`)
* `UP_AREA`: Accumulated upstream contributing area (km²)

#### Completed upstream tracing results
A recursive upstream topology trace using `NEXT_DOWN` was completed from the Lokoja confluence outlet (`HYBAS_ID = 1060909890`), resolving the full contributing catchment network across **two primary tributary branches (Niger and Benue)**:

| Metric | Result |
|---|---:|
| **Outlet target basin** | `1060909890` |
| **Main terminal basin** | `1060022420` |
| **Primary upstream branches** | **2** (Niger and Benue systems) |
| **Total upstream basin features** | **297** |
| **QA status** | Topology connectivity and feature count QA completed |

* **Intended application:** Define upstream contributing catchments for Lokoja, separate Niger vs. Benue hydrological signals, and guide GloFAS discharge grid-cell selection.
* **Known limitations:** Level 6 sub-basins represent coarse regional aggregations; finer sub-basin delineation (e.g., Level 7–8) or river-network snapping may be required for local tributary routing around Lokoja town.

---

### 2.3 Historical flood & reference layers (Copernicus EMS)

| Attribute | Description |
|---|---|
| **Dataset** | Copernicus Emergency Management Service Rapid Mapping — Activation `EMSR314` (Area of Interest `02`: Lokoja) |
| **Dataset ID** | `EMSR314_02` |
| **Provider** | Copernicus EMS On-Demand Mapping (European Union) |
| **Access method** | Manual download (Vector package) |
| **Actual acquisition date** | Pre-13 November 2026 *(record exact download date)* |
| **Repository status** | **Retained in repository** (raw archive + QA-repaired & Lokoja-clipped layers) |
| **Temporal coverage** | Event-specific: September 2018 Nigeria floods |
| **Licence** | **Copernicus EMS Data Policy** — Free and open reuse for research and commercial purposes, subject to mandatory source attribution |

#### Acquired layers & flood geometry QA summary

| Layer Category | Description / Geometry Processing Metrics | Status in Repository |
|---|---|---|
| **Observed Event Flood Extent** | • **1,509** total flood polygons in raw product<br>• **104** invalid geometries repaired during QA<br>• **54** flood features intersecting Lokoja LGA<br>• **36.009 km²** total clipped flood footprint within Lokoja LGA | **Retained & QA-completed** |
| **Hydrography** | Reference rivers, streams, and permanent water bodies mapped for `EMSR314_02` | **Retained** |
| **Built-up** | Settlement footprints and urban/built-up exposure polygons | **Retained** |
| **Transportation** | Road networks and transport infrastructure lines | **Retained** |
| **Physiography** | Topographic/landform reference features included in the activation package | **Retained** |

* **Intended application:** Serve as historical ground-truth validation for September 2018 flood extent and provide baseline exposure layers (built-up areas and roads) for Lokoja.
* **Known limitations:** 
  * Represents a single historical flood event (September 2018) and is bound by satellite acquisition timing and cloud/sensor constraints at the time of activation.
  * Auxiliary layers (built-up, transportation) reflect 2018 baseline conditions and require comparison against current OpenStreetMap data for modern exposure mapping.

---

## 3. Datasets Explored in Google Earth Engine (Not Yet Retained in Repository)

These datasets have been queried, visualised, or tested via sample scripts in GEE, but full production exports have **not** yet been formally archived in the repository.

| Dataset | GEE Asset / Dataset ID | Provider | Spatial / Temporal Specs | Licence | Exploration Status & Pending Actions |
|---|---|---|---|---|---|
| **Sentinel-1 SAR GRD** | `COPERNICUS/S1_GRD` | Copernicus / ESA | 10 m, 25 m, or 40 m; Oct 2014 – present; acquisition-dependent revisit | Copernicus Sentinel Data Terms (free & open with attribution) | **Explored in GEE only.** Initial coverage checks completed; standardized GEE export workflow and speckle/incidence-angle preprocessing need consolidation. |
| **CHIRPS Daily (v2 / v3)** | `UCSB-CHG/CHIRPS/DAILY` *(verify v3 asset ID)* | Climate Hazards Center (UCSB) | 0.05° (~5.5 km); daily; 1981 – near present | Public Domain (CC0 / USGS-UCSB open access) | **Sample explored in GEE.** Basin rainfall aggregation tested; exact exported sample, version alignment (v2 vs. v3), and QA logs must be recorded in the repository. |
| **SRTM Digital Elevation Model** | `USGS/SRTMGL1_003` | NASA / USGS | 1 arc-second (~30 m at equator); static (2000 mission) | NASA / USGS Open Data (retain source acknowledgement) | **Sample explored in GEE.** Terrain/elevation sampling tested; clipped Lokoja/basin DEM raster and QA metadata need formal export to repository. |

* **Known limitations (GEE-explored datasets):**
  * **Sentinel-1 GRD:** Revisit intervals over Nigeria vary by orbital pass and mission status (e.g., Sentinel-1B outage from Dec 2021 until Sentinel-1C availability); emergent vegetation and urban double-bounce can cause false negatives/positives in SAR flood detection.
  * **CHIRPS:** Satellite-gauge blended estimates can underestimate extreme convective short-duration rainfall bursts across West Africa and carry a latency lag for final gauge-corrected products.
  * **SRTM:** Reflects surface elevation (including canopy and building heights rather than bare-earth DTM) circa February 2000, introducing vertical bias in vegetated floodplains and newly urbanized areas.

---

## 4. Pending & External Candidate Datasets

These datasets are either partially sampled outside GEE or awaiting formal access requests and verification.

| Dataset | Identifier / Access Endpoint | Provider | Spatial / Temporal Specs | Licence | Status & Known Limitations |
|---|---|---|---|---|---|
| **OpenStreetMap (OSM)** | Geofabrik / Overpass API (`nigeria-latest`) | OpenStreetMap Contributors | Vector features (roads, buildings, waterways); continuous updates | **ODbL** (Open Database License — attribution & share-alike required) | **Sample explored externally.** Extract date, bounding polygon, and download tool must be documented before retaining in repository. Completeness varies across rural Kogi State. |
| **GloFAS Historical & Forecast Discharge** | Copernicus Climate Data Store (`cems-glofas-historical` / `forecast`) | Copernicus EMS / ECMWF | 0.05° grid; daily; v4 historical (1979 – near present) + medium-range forecasts | Copernicus CDS Licence (free & open with attribution) | **Pending acquisition.** CDS API access and exact grid-cell coordinates representing the Niger/Benue confluence at Lokoja require confirmation. Coarse 0.05° grid requires river-network snapping. |

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

