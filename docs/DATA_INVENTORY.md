# NigeriaFloodWatch — Data Inventory

**Document version:** 0.2  
**Project:** NigeriaFloodWatch  
**Pilot study area:** Lokoja, Kogi State, Nigeria  
**Last updated:** 13 November 2026  
**Status:** Phase 1 working inventory

---

## 1. Purpose

This document records the environmental, hydrological, terrain, flood-observation and exposure datasets investigated for NigeriaFloodWatch.

It documents:

- Data provider and source.
- Dataset version and identifier.
- Spatial and temporal coverage.
- Spatial and temporal resolution.
- Access method and acquisition status.
- Licence and attribution requirements.
- Intended application.
- Quality checks, limitations and outstanding work.

Acquisition status distinguishes data retained in the repository from datasets previously explored but not currently retained as local files.

## 2. Study-area datasets

### 2.1 Administrative boundary — Lokoja LGA

| Attribute | Description |
|---|---|
| Dataset | Nigeria Administrative Boundaries |
| Provider | United Nations Second Administrative Level Boundaries (UN SALB) |
| Source | https://salb.un.org/en/data/nga |
| Format | Shapefile |
| Administrative level | LGA / second-level administrative unit |
| Working CRS | EPSG:32632 |
| Geographic export CRS | EPSG:4326 |
| Calculated area | 3,181.1678 km² |
| Repository source | `data/raw/lokoja_lga_utm32n.zip` |
| Processed layer | `data/processed/lokoja_lga_boundary.geojson` |
| Acquisition status | Acquired and QA-checked |

**Quality checks**

- One polygon feature.
- Geometry valid.
- No null or empty geometry.
- Missing source SHX index reconstructed during inspection.
- Calculated area agrees with the previously reported ArcGIS Pro result.

**Intended application**

- Administrative reporting.
- Spatial clipping and overlay.
- Organisation of local exposure and flood information.

**Limitations**

The administrative boundary is not a floodplain boundary or a hydrological catchment. The source licence and conditions concerning redistribution and derivative geometry must be reviewed before commercial deployment.

### 2.2 Local flood-analysis extent — Copernicus EMSR314_02

| Attribute | Description |
|---|---|
| Dataset | EMSR314_02 Lokoja delineation product |
| Provider | Copernicus Emergency Management Service |
| Activation | EMSR314 |
| Event | September 2018 Nigeria flooding |
| Product | Lokoja delineation map and vector package |
| Format | Shapefile and supporting metadata |
| Source | https://mapping.emergency.copernicus.eu/activations/EMSR314/ |
| Original CRS | EPSG:4326 |
| Area of interest | 947.541 km² |
| AOI intersection with Lokoja LGA | 223.853 km² |
| Repository archive | `data/raw/EMSR314_02LOKOJA_01DELINEATION_MAP_v1_vector.zip` |
| Extracted layers | `data/raw/EMSR314_02_extracted/` |
| Local analysis extent | `data/processed/lokoja_local_analysis_extent.geojson` |
| Acquisition status | Acquired and inspected |

**Available layers**

| Layer | Features | Geometry |
|---|---:|---|
| Area of interest | 1 | Polygon |
| Observed event | 1,509 | Polygon / MultiPolygon |
| Hydrography polygons | 108 | Polygon / MultiPolygon |
| Hydrography lines | 22 | LineString |
| Built-up areas | 31 | Polygon |
| Transportation lines | 47 | LineString |
| Transportation points | 7 | Point |
| Physiography lines | 172 | LineString / MultiLineString |

**Observed flood evidence**

- Original flood polygons: 1,509.
- Invalid geometries identified: 104.
- Invalid geometries after repair in a derived working copy: 0.
- Flood polygons intersecting Lokoja LGA after clipping: 54.
- Clipped mapped flood area: 36.009 km².
- Clipped footprint as a proportion of LGA area: 1.1319%.
- Total mapped flood footprint across the Copernicus AOI: approximately 154.759 km².

**Named hydrography**

- Niger: one named river polygon.
- Benue: three named river polygons.
- The four named polygons intersect the mapped 2018 flood footprint.

**Intended application**

- Historical flood-event evidence.
- Local river-corridor analysis.
- Contextual settlement and transportation exposure assessment.
- Definition of the provisional local analysis extent.

**Limitations**

The 2018 flood footprint represents one event and its mapped observation period. It is not a permanent floodplain boundary, a complete historical flood catalogue or a complete current exposure inventory.

Copernicus hydrography, settlements and transportation features are event-product context layers. They should not be treated as a complete or current inventory of local infrastructure.

The Copernicus AOI is used as a provisional local analysis extent, not as a claim that the entire 947.541 km² is floodplain.

The source-product reuse conditions and attribution requirements must be retained with redistributed derivatives.

### 2.3 Hydrological study area — HydroBASINS Level 6

| Attribute | Description |
|---|---|
| Dataset | HydroBASINS v1, Level 6 |
| Provider | WWF / HydroSHEDS |
| Earth Engine ID | `WWF/HydroSHEDS/v1/Basins/hybas_6` |
| Format | Earth Engine FeatureCollection; GeoJSON and CSV exports |
| Working CRS | EPSG:4326 |
| Repository network | `data/processed/hydrobasins_combined_upstream_network_lokoja.geojson` |
| Repository attributes | `data/processed/hydrobasins_combined_upstream_attributes_lokoja.csv` |
| Acquisition status | Acquired and structurally QA-checked |

**Combined network results**

| Metric | Result |
|---|---:|
| Target A | 1060909890 |
| Target A total features | 256 |
| Target B | 1060909900 |
| Target B total features | 41 |
| Combined unique features | 297 |
| Shared basin IDs | 0 |
| Target basins | 2 |
| Upstream contributing basins | 295 |
| Upstream generations | 0–39 |
| Duplicate basin identifiers | 0 |
| Invalid basin geometries | 0 |
| Downstream links outside exported network | 0 |

Both candidate branches drain towards the common downstream basin `1060022420`.

**Important attributes**

- `HYBAS_ID`: basin identifier.
- `NEXT_DOWN`: next downstream basin.
- `MAIN_BAS`: main basin identifier.
- `UP_AREA`: accumulated upstream area.
- `SUB_AREA`: individual sub-basin area.
- `PFAF_ID`: Pfafstetter basin identifier.
- `upstream_level`: traced upstream generation.
- `branch_seed`: target basin used for tracing.
- `branch_name`: working branch label.
- `network_role`: target or contributing basin.

**Intended application**

- Upstream drainage context.
- Rainfall aggregation by contributing basin.
- Identification of hydrologically relevant river reaches and discharge locations.
- Support for GloFAS grid-cell investigation.

**Limitations**

The 297-feature network is a candidate combined upstream network. Structural consistency does not independently prove that the two branches correspond respectively to the Niger and Benue catchments.

River identity and hydrological relevance must be checked against authoritative river-network and hydrological evidence before the branches are assigned definitive names.

HydroBASINS is a basin-boundary dataset, not a detailed local river-channel dataset.

## 3. Environmental and hydrometeorological datasets

### 3.1 Sentinel-1 GRD

| Attribute | Description |
|---|---|
| Provider | European Space Agency / Copernicus |
| Dataset | Sentinel-1 Level-1 Ground Range Detected |
| Earth Engine collection | `COPERNICUS/S1_GRD` |
| Variables | VV and VH backscatter where available |
| Spatial resolution | Product-dependent; commonly 10 m pixel spacing for IW GRD |
| Temporal coverage | Mission archive from 2014 onward |
| Access | Google Earth Engine and Copernicus Data Space |
| Licence | Copernicus Sentinel Data Legal Notice |
| Repository sample | No exported sample currently listed |
| Acquisition status | Previous GEE exploration; reproducible sample export not yet evidenced |

**Intended application**

- SAR-based flood observation.
- Historical inundation mapping.
- Water-change detection.
- Flood-label development.

**Limitations**

- Acquisition dates and orbit direction affect temporal comparability.
- Permanent water, wet soil, vegetation and urban surfaces complicate classification.
- SAR observations after a forecast issue time must not be used as predictors for that forecast.
- GRD pixel spacing must not be interpreted as the spatial resolution of a validated operational forecast.

### 3.2 CHIRPS v3 rainfall

| Attribute | Description |
|---|---|
| Provider | Climate Hazards Center, University of California Santa Barbara |
| Dataset | CHIRPS v3 |
| Earth Engine products | `UCSB-CHC/CHIRPS/V3/DAILY_SAT` and `UCSB-CHC/CHIRPS/V3/DAILY_RNL` |
| Variable | Precipitation |
| Spatial resolution | 0.05° |
| Temporal coverage | 1981 to near present |
| Temporal resolution | Daily and other product intervals |
| Source | https://www.chc.ucsb.edu/data/chirps3 |
| Access | Google Earth Engine and CHC data repository |
| Licence | Record the applicable CHC product terms and attribution |
| Repository sample | No exported sample currently listed |
| Acquisition status | Previous sample exploration; local export and exact product selection need confirmation |

**Product distinction**

The daily satellite-partitioned and reanalysis-partitioned products must be recorded separately. The exact collection used in an experiment must be documented.

**Intended application**

- Historical rainfall analysis.
- Antecedent rainfall features.
- Catchment rainfall aggregation.
- Retrospective flood-event analysis.

**Limitations**

CHIRPS is a gridded precipitation estimate, not a direct rain-gauge observation. Daily estimates and preliminary/final releases have different data-production characteristics.

Historical CHIRPS observations are not substitutes for archived rainfall forecasts available at a historical prediction issue time.

### 3.3 CHIRPS-GEFS rainfall forecast

| Attribute | Description |
|---|---|
| Provider | Climate Hazards Center |
| Dataset | CHIRPS-GEFS |
| Variable | Bias-corrected precipitation forecast |
| Spatial resolution | 0.05° |
| Forecast coverage | Daily forecasts extending approximately 1–16 days |
| Source | https://www.chc.ucsb.edu/data |
| Access | CHC data repository |
| Repository sample | Not retained |
| Acquisition status | Candidate forecast source; access and historical forecast-vintage availability need investigation |

**Intended application**

Potential future forecast rainfall predictor for the 72-hour forecasting objective.

**Limitations**

The project must verify forecast issue time, valid time, lead time, archive availability and historical versioning. A current forecast cannot replace an archived forecast vintage in retrospective validation.

### 3.4 SRTM Digital Elevation Model

| Attribute | Description |
|---|---|
| Provider | NASA / USGS |
| Dataset | Shuttle Radar Topography Mission |
| Common product | SRTM 1 Arc-Second Global |
| Spatial resolution | Approximately 30 m at the equator |
| Variable | Elevation |
| Access | USGS / NASA data services and Google Earth Engine |
| Earth Engine candidate | `USGS/SRTMGL1_003` |
| Licence | NASA Earth observation data access and applicable product terms |
| Repository sample | No raster currently listed |
| Acquisition status | Previously explored; exported raster and QA not evidenced |

**Intended application**

- Elevation and slope.
- Terrain conditioning.
- Drainage and low-lying area analysis.
- Supporting flood-susceptibility features.

**Limitations**

SRTM is a surface-elevation product with vegetation and built-structure effects. It is not a bare-earth hydraulic terrain model and does not provide flood depth or river discharge.

### 3.5 OpenStreetMap

| Attribute | Description |
|---|---|
| Provider | OpenStreetMap contributors |
| Data type | Vector geographic features |
| Variables | Roads, buildings, waterways, land use and points of interest |
| Spatial resolution | Feature-dependent |
| Temporal coverage | Continuously updated community database |
| Access | Overpass API, regional extracts and other OSM-compatible services |
| Licence | Open Database License (ODbL) |
| Source | https://www.openstreetmap.org/copyright |
| Repository sample | No local extract currently listed |
| Acquisition status | Previous exploration; dated extract not retained |

**Intended application**

- Settlement and building exposure.
- Road and infrastructure exposure.
- River-network context.
- Supporting spatial analysis.

**Limitations**

Completeness and positional accuracy vary spatially. The extract date and query must be preserved. ODbL attribution and share-alike obligations must be considered when distributing adapted database products.

## 4. Hydrological discharge datasets

### 4.1 Global Flood Awareness System — GloFAS

| Attribute | Description |
|---|---|
| Provider | Copernicus Emergency Management Service |
| Dataset | GloFAS historical and forecast products |
| Historical variable | River discharge |
| Historical temporal resolution | Daily |
| Historical grid resolution | 0.05° for current catalogue products |
| Historical coverage | From 1979 to near real time, version-dependent |
| Access | Copernicus Climate Data Store |
| Source | https://ewds.climate.copernicus.eu/datasets/cems-glofas-historical |
| Repository sample | No downloaded file currently listed |
| Acquisition status | Access and Lokoja-relevant grid-cell assessment outstanding |

**Intended application**

- Historical discharge analysis.
- Upstream hydrological context.
- Potential discharge predictors.
- Evaluation of forecast discharge products.

**Limitations and pending checks**

- Confirm the current historical and forecast product versions.
- Identify grid cells and river reaches relevant to the two candidate upstream branches.
- Check the relationship between GloFAS grid cells and local river topology.
- Verify forecast issue time, valid time and lead time.
- Confirm access to archived forecast vintages before claiming retrospective 72-hour forecast validation.

### 4.2 NIHSA — Nigerian Hydrological Services Agency

| Attribute | Description |
|---|---|
| Provider | Nigerian Hydrological Services Agency |
| Candidate data | River stage, water level, discharge, station records and hydrological reports |
| Spatial coverage | Station-dependent |
| Temporal coverage | To be established |
| Access | Institutional request / official data channels |
| Licence and fees | To be confirmed with provider |
| Repository sample | None listed |
| Acquisition status | Data availability and request process outstanding |

**Intended application**

- Local river-level and discharge observations.
- Independent validation of hydrological products.
- Historical event timing and severity evidence.

### 4.3 NIWA — Nigerian Inland Waterways Authority

| Attribute | Description |
|---|---|
| Provider | Nigerian Inland Waterways Authority |
| Candidate information | Inland waterway, navigation and relevant hydrological information |
| Spatial coverage | To be established |
| Temporal coverage | To be established |
| Access | Institutional enquiry |
| Licence and fees | To be confirmed |
| Repository sample | None listed |
| Acquisition status | Source relevance and data availability assessment outstanding |

**Intended application**

Potential supplementary river and waterway information around Lokoja.

NIWA should not be assumed to provide a complete river-discharge observation archive without confirmation.

## 5. Historical flood evidence and event records

### 5.1 UNOSAT

| Attribute | Description |
|---|---|
| Provider | United Nations Satellite Centre |
| Candidate data | Satellite-derived flood extent products and event reports |
| Format | Product-dependent |
| Temporal coverage | Event-dependent |
| Access | UNOSAT product catalogue and event reports |
| Licence | Product-specific terms to be checked |
| Repository sample | No separate UNOSAT file currently listed |
| Acquisition status | Historical Lokoja/Nigeria products identified; local repository copy not evidenced |

**Intended application**

- Historical flood-event catalogue.
- Independent flood extent evidence.
- Comparison against Copernicus and Sentinel-1 observations.

**Limitations**

Each product must be recorded with its event date, observation date, geographic coverage, mapping method and uncertainty.

### 5.2 NEMA

| Attribute | Description |
|---|---|
| Provider | National Emergency Management Agency, Nigeria |
| Candidate data | Flood event reports, situation reports, affected communities and impact information |
| Spatial coverage | Report-dependent |
| Temporal coverage | Report-dependent |
| Access | Official reports and institutional channels |
| Licence | To be confirmed |
| Repository sample | No local report currently listed |
| Acquisition status | Historical record investigation outstanding |

**Intended application**

- Event chronology.
- Affected-community evidence.
- Contextual flood impact and exposure information.

Reported impacts must not be treated as spatially precise flood labels unless the source provides defensible geographic and temporal references.

## 6. Dataset acquisition and quality-control register

The following status reflects the current repository inventory on 13 November 2026.

| Dataset | Locally retained | Quality checks | Remaining work |
|---|---|---|---|
| UN SALB Lokoja boundary | Yes | Geometry, CRS and area | Confirm licence implications |
| HydroBASINS combined network | Yes | IDs, topology links and geometry validity | Independently identify river branches |
| Copernicus EMSR314_02 | Yes | Geometry repair, clipping and area | Preserve event metadata and source terms |
| Sentinel-1 | No sample listed | Initial exploration only | Export and document reproducible sample |
| CHIRPS v3 | No sample listed | Previous exploration only | Confirm product and export sample |
| SRTM | No raster listed | Previous exploration only | Export sample and perform raster QA |
| OSM | No extract listed | Previous exploration only | Acquire dated local extract |
| GloFAS | No sample listed | Not completed | Verify access, variables and grid cells |
| NIHSA | No observations listed | Not completed | Request data availability |
| NIWA | No observations listed | Not completed | Verify relevant data availability |
| UNOSAT | No separate file listed | Source investigation | Acquire relevant products and metadata |
| NEMA | No report listed | Source investigation | Locate and document relevant reports |

## 7. Data provenance and storage conventions

The project uses the following storage structure:

- `data/raw/`: original downloaded files, unchanged.
- `data/interim/`: extracted or intermediate working datasets.
- `data/processed/`: validated, cleaned and analysis-ready outputs.
- `data/figures/`: quality-control maps and figures.

Every retained dataset should have a record of:

1. Provider and dataset name.
2. Version or collection identifier.
3. Download or acquisition date.
4. Observation period.
5. Geographic coverage.
6. CRS and spatial resolution.
7. Temporal resolution and update frequency.
8. Access method and source URL.
9. Licence and required attribution.
10. Processing steps and output filename.
11. Quality checks and limitations.

Original source archives must not be overwritten by geometry repair, reprojection, clipping or other transformations.

## 8. Forecasting and temporal data integrity

Observed satellite imagery, historical rainfall, reanalysis and forecast products have different temporal meanings.

For retrospective prediction experiments:

- Predictor data must represent information available at the forecast issue time.
- Archived forecasts must retain their original issue time and valid time.
- Post-event Sentinel-1 observations may support flood labels but must not leak into earlier predictor features.
- Historical rainfall observations must not be represented as archived forecasts.
- Each flood label must have a documented event and observation time.
- Temporal validation must be event-aware and avoid leakage between training and test periods.

The intended forecast horizon remains up to 72 hours. No operational prediction capability is claimed until appropriate labels, forecast-vintage predictors and independent validation are available.

## 9. Outstanding Phase 1 data priorities

1. Consolidate the Sentinel-1 GEE acquisition workflow and retain a sample.
2. Confirm the exact CHIRPS v3 product previously explored and retain a sample.
3. Export and quality-check a local SRTM sample.
4. Acquire and document a dated OSM extract.
5. Verify GloFAS historical and forecast access and relevant grid cells.
6. Investigate NIHSA and NIWA observation availability.
7. Acquire relevant UNOSAT and NEMA historical records.
8. Complete the separate source and licence register.

**Phase 1 exit requirement:** Essential sample datasets must be reproducibly acquired, spatially and temporally characterised, quality-checked and documented, with unresolved access limitations explicitly recorded.
