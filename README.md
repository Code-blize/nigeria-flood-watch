
# NigeriaFloodWatch

**A geospatial flood intelligence platform for Nigeria, beginning with Lokoja, Kogi State.**

NigeriaFloodWatch is a research and engineering project exploring how satellite observations, rainfall data, terrain, hydrological information and machine learning can be combined to support flood monitoring and hazard estimation.

The project begins with Lokoja, a riverine city near the confluence of the Niger and Benue rivers. The long-term goal is to develop a reliable, validated flood intelligence system with an interactive map and geospatial API.

> **Project status:** Phase 1 — data acquisition — has established a substantial initial data foundation. The project is moving into **Phase 2 — geospatial preprocessing**. Forecasting and deployment are future goals and are not yet validated capabilities.

## Project objectives

NigeriaFloodWatch aims to:

- Process and analyse satellite-derived flood observations.
- Integrate rainfall, terrain, river-network and hydrological datasets.
- Examine the spatial and temporal characteristics of historical flooding in Lokoja.
- Build reproducible geospatial preprocessing and analysis workflows.
- Develop and evaluate machine-learning models for flood hazard estimation.
- Investigate whether the available data can support short-term flood forecasting.
- Eventually provide flood information through an API and an interactive web map.

## Study area

The pilot study area is **Lokoja, Kogi State, Nigeria**.

The project distinguishes between two related geographic areas:

- **Core study area:** Lokoja’s floodplain and surrounding settlements, where observed inundation and local flood hazard will be examined.
- **Hydrological context:** relevant upstream portions of the Niger and Benue systems, which may help explain river conditions affecting Lokoja.

Upstream basin boundaries and river attribution must be independently verified before being used to make specific hydrological claims.

## Project phases

| Phase | Focus |
|---|---|
| 1. Geospatial data acquisition | Identify, acquire and assess relevant datasets. |
| 2. Geospatial preprocessing | Create quality-checked, analysis-ready geospatial data. |
| 3. Exploratory spatial analysis | Investigate historical flood events and spatial patterns. |
| 4. Feature engineering and dataset construction | Define the prediction unit, target and valid training examples. |
| 5. Model development | Train and evaluate suitable baseline and candidate models. |
| 6. API development | Build a service for delivering validated model outputs. |
| 7. Deployment and MLOps | Package, test, deploy and monitor the application. |
| 8. Interactive platform | Present observed and modelled flood information on a web map. |

The current focus is **Phase 2: Geospatial preprocessing**.

## Data sources

The project has acquired or examined data from the following sources:

| Dataset | Intended use | Current notes |
|---|---|---|
| Sentinel-1 Synthetic Aperture Radar (SAR) | Historical flood observation and surface analysis | A September 2018 scene has been acquired and checked for coverage. |
| CHIRPS v3 rainfall | Historical rainfall analysis | Daily and monthly samples have been checked for structural consistency. |
| Shuttle Radar Topography Mission (SRTM) | Elevation and terrain derivatives | Elevation and terrain data have been acquired for the study area. |
| HydroBASINS | Hydrological basin context | An upstream basin network has been assembled; specific river-branch attribution requires verification. |
| Copernicus flood mapping | Historical flood extent | A 2018 event footprint has been repaired and clipped to the Lokoja LGA. |
| Global Flood Awareness System (GloFAS) | Historical river-discharge context | Historical modelled grid-cell data have been retrieved; the cells’ local river attribution is not confirmed. |
| OpenStreetMap (OSM) | Roads and other infrastructure features | A limited road sample has been tested; it is not a complete Lokoja inventory. |
| Leeds/DFO validation data | Exploratory comparison with observed flood information and global flood model outputs | Examined for a 2012 event; comparison results remain provisional pending reproducible checks and clarification of the observation raster’s valid-data mask. |

Additional candidate sources include CHIRPS-GEFS forecast rainfall and records from Nigerian hydrological and disaster-management institutions. Their availability and suitability must be verified before they are used in modelling.

## Scientific principles

The project follows several principles:

1. **Distinguish observations from predictions.** Satellite-detected or recorded flood information must be labelled separately from calculated, modelled or forecast information.
2. **Respect native data resolution.** Resampling a coarse dataset to a finer grid does not create finer-scale information.
3. **Preserve time validity.** Historical observations or reanalysis must not be treated as information that would have been available at a past forecast issue time.
4. **Prevent data leakage.** Model evaluation must account for the temporal and spatial dependence of flood observations.
5. **Report limitations.** Data gaps, uncertainty and unresolved assumptions must be documented rather than hidden.
6. **Validate before making forecast claims.** A 72-hour flood forecast is a long-term objective, not a current project capability.

The project distinguishes among:

- **Observed:** detected by satellite or recorded by an observation source.
- **Calculated:** derived through geospatial analysis.
- **Modelled:** estimated by a trained model.
- **Forecast:** an estimate of future conditions based on information available at a defined forecast issue time.

## Planned technology

The intended technology stack includes:

- **Data acquisition and processing:** Google Earth Engine, Python, GeoPandas, Rasterio, xarray and GDAL.
- **GIS and visual quality assurance:** ArcGIS Pro.
- **Machine learning and experiment tracking:** scikit-learn, PyTorch and MLflow.
- **API and deployment:** FastAPI, Docker, GitHub Actions and Google Cloud Run.
- **Interactive mapping:** Leaflet or Deck.gl.

Tools will be introduced when they serve a specific, testable project need. Heavy satellite processing and model training will be kept separate from API serving.

## Repository structure

The project is intended to use a modular structure similar to the following. The actual repository may differ as implementation progresses.

```text
NigeriaFloodWatch/
├── docs/
├── notebooks/
├── src/
│   └── nigeria_floodwatch/
│       ├── ingestion/
│       ├── preprocessing/
│       ├── features/
│       ├── labels/
│       ├── models/
│       ├── evaluation/
│       ├── api/
│       └── utils/
├── tests/
├── frontend/
├── docker/
├── configs/
├── scripts/
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── models/
└── reports/
```

Large raster datasets should be stored outside ordinary Git commits. Raw source data should be preserved, and preprocessing should produce documented outputs rather than silently replacing the originals.

## Current focus: Phase 2

Phase 2 will establish reproducible preprocessing workflows for the acquired data. Work will include:

- inspecting file metadata, spatial coverage, coordinate reference systems, units and NoData conventions;
- defining and documenting the study-area boundaries;
- choosing appropriate clipping, reprojection and alignment methods;
- validating raster and vector outputs;
- preserving the original resolution and meaning of each dataset;
- documenting transformations, parameters and quality checks.

The next phases will use these prepared datasets for exploratory analysis, feature engineering and model development.

## Limitations

The project is under active development. The available data do not yet establish a validated operational flood forecast.

Important limitations include:

- The 2018 flood extent represents a specific event, not a permanent floodplain.
- GloFAS values are modelled grid-cell estimates, not local gauge measurements; their attribution to the Niger or Benue near Lokoja remains unconfirmed.
- The tested OSM road sample does not represent a complete infrastructure inventory.
- Some institutional records and forecast datasets remain under investigation.
- Earlier Leeds/DFO comparison results are exploratory until reproduced and their observation-validity assumptions are resolved.

These limitations will be revisited as the data are processed and verified.

## Research and engineering approach

The project is being developed incrementally:

1. Define the scientific or engineering question.
2. Choose and explain an appropriate method.
3. Implement a manageable, reproducible step.
4. Test the output and inspect its quality.
5. Record limitations and decisions.
6. Document the verified result before proceeding.

The goal is not simply to produce a model or map. It is to build a system whose data, methods and outputs can be inspected and defended.

## Project status

**Current phase:** Phase 2 — Geospatial preprocessing  
**Pilot:** Lokoja, Kogi State, Nigeria  
**Primary hazard:** Riverine flooding  
**Long-term objective:** Validated flood intelligence, with short-term forecasting investigated only if the data support it.

## Disclaimer

NigeriaFloodWatch is a research and development project. Its outputs are not an official warning system and should not be used as the sole basis for emergency decisions. Any future forecast capability will require rigorous validation and clear communication of uncertainty.

## License

A project licence has not yet been specified. Dataset-specific licences and terms of use must be respected independently of the project’s own licence.
