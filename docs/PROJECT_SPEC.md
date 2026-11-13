# NigeriaFloodWatch — Project Specification

**Document:** Project specification  
**Version:** 1.0 (Phase 1 baseline)  
**Status:** Working baseline for implementation and research planning  
**Last updated:** 11 November 2026  
**Pilot location:** Lokoja, Kogi State, Nigeria  
**Initial hazard focus:** Riverine flooding associated with the Niger–Benue system  
**Intended forecast horizon:** Up to 72 hours

---

## 1. Purpose of this specification

This document defines the project purpose, scientific scope, intended outputs, study-area concepts, forecasting target, data principles, evaluation requirements and delivery constraints for NigeriaFloodWatch.

Version 1.0 establishes the project's Phase 1 baseline. It does **not** claim that a validated operational forecasting model already exists. Some implementation choices—especially exact study-area geometries, modelling support/resolution, label rules and forecast-input versions—remain subject to evidence gathered during Phase 1.

The specification supersedes the repository's initial `PROJECT_SPEC.md` version 0.1. It should be revised through documented decisions when new evidence materially changes the scope or method.

## 2. Project definition

NigeriaFloodWatch is a research-driven geospatial flood-intelligence system intended to combine satellite remote sensing, rainfall information, hydrological data, terrain characteristics, historical flood observations and exposure information.

The first pilot is Lokoja, Kogi State, located at the Niger–Benue confluence. The initial focus is riverine flooding influenced by hydrological conditions in the upstream Niger and Benue systems.

The long-term objective is to provide reproducible flood information and, once sufficient evidence and historical forecast data are available, short-range flood-hazard predictions through an API and interactive map.

The system is designed to be expandable to other flood-prone locations in Nigeria. Expansion beyond Lokoja is not part of the initial validation claim.

## 3. Aim

To establish and validate a reproducible geospatial and hydrometeorological workflow that characterises riverine flooding around Lokoja and investigates whether available historical observations and forecast products can support reliable flood-hazard prediction up to 72 hours ahead.

## 4. Specific objectives

1. Establish defensible administrative, local floodplain and upstream hydrological study areas for Lokoja.
2. Build a documented inventory and provenance register for relevant environmental, hydrological, terrain, flood-observation and exposure datasets.
3. Acquire representative sample data through authoritative APIs and cloud-hosted processing services where possible.
4. Develop quality-controlled workflows for Sentinel-1 flood observation, rainfall, terrain, river networks and discharge information.
5. Resolve the relevant upstream Niger and Benue drainage topology and identify hydrologically relevant locations for discharge extraction.
6. Build an event catalogue with time-stamped and spatially referenced flood evidence.
7. Define and construct flood labels with explicit treatment of observation gaps, label confidence and event timing.
8. Establish temporally valid predictor datasets that reproduce the information available at a historical forecast issue time.
9. Develop simple, interpretable baselines before evaluating more complex machine-learning methods.
10. Evaluate model performance using temporal, event-based and spatially independent validation.
11. Communicate the difference between observed inundation, susceptibility, forecast hazard and risk.
12. Design an API and geospatial interface that expose prediction provenance, validity time, uncertainty and model version.

## 5. Scope

### 5.1 In scope for the Lokoja pilot

- Riverine flood processes associated with the Niger–Benue confluence.
- Upstream rainfall and hydrological conditions relevant to Lokoja.
- Local floodplain and river-corridor inundation observations.
- Terrain and drainage characteristics that condition local inundation.
- Historical flood-event documentation and satellite-derived flood footprints.
- Settlements, roads, buildings and other exposed assets where suitable data and licence conditions permit.
- Retrospective evaluation of forecast capability using archived forecast inputs, where available.
- A future prediction API and map interface, after the modelling and validation gates are passed.

### 5.2 Out of scope for the initial pilot unless later evidence justifies inclusion

- A nationally operational warning service.
- A guarantee of flood safety or evacuation decisions.
- A fully coupled hydraulic/hydrodynamic simulation of the Niger and Benue rivers.
- Explicit prediction of every urban drainage, pluvial or flash-flood mechanism in Lokoja.
- A 10 m operational forecast merely because Sentinel-1 or a DEM has a fine pixel size.
- A claim of validated 72-hour prediction before historical forecast-vintage inputs and suitable flood labels are available.
- Automated deployment of a public-facing warning service during Phase 1.

Pluvial/urban drainage flooding may be investigated separately if evidence shows it is a material component of the target events and suitable rainfall, drainage and event data can be obtained. It must not silently be mixed with riverine labels.

## 6. Study-area framework

The project will maintain three distinct spatial concepts. Their geometries must be produced and documented separately.

### 6.1 Administrative study area — Lokoja LGA

Purpose:

- Administrative reporting and project organisation.
- Summarising exposure and results by administrative unit.
- Providing a broad reference boundary for local data discovery.

Existing work:

- Lokoja LGA was extracted from the UN SALB Nigeria administrative-boundary dataset.
- The source geometry was in EPSG:4326.
- A working projected layer was created in WGS 84 / UTM zone 32N (EPSG:32632).
- The reported calculated area is **3,181.16785 km²**.

The reported area is a preliminary project value and should receive an independent geometry/area quality check. The LGA boundary is not a floodplain boundary and must not be used as a substitute for the hydrological catchment.

### 6.2 Local floodplain analysis area

Purpose:

- Analyse observed inundation around Lokoja's urban environment and river corridors.
- Define local areas where flood footprints, terrain and exposed assets are assessed.
- Provide the local spatial domain for any later inundation or exposure products.

The floodplain analysis area must be evidence-derived. It may use a combination of:

- Historical flood footprints and event reports.
- Sentinel-1-derived water/inundation observations.
- River and channel geometry.
- Terrain and elevation information.
- Hydrologically meaningful low-lying areas and drainage pathways.
- Settlements and infrastructure that fall within or near observed flood-affected areas.

A fixed-radius buffer around Lokoja, an arbitrary low-elevation threshold, or the full LGA polygon is not sufficient on its own to define the floodplain. The final boundary and inclusion rules belong to the Phase 1 study-area task and must be recorded with the evidence used.

### 6.3 Hydrological Study Area

The hydrological study area is defined using a combined upstream catchment network derived from HydroBASINS (WWF HydroSHEDS v1). The network captures two candidate upstream branches associated with the Lokoja study location.

#### 6.3.1 Network composition

The combined network contains **297 unique HydroBASINS features**:

| Component | Target basin | Total features, including target | Upstream contributing features |
|---|---:|---:|---:|
| Target A | 1060909890 | 256 | 255 |
| Target B | 1060909900 | 41 | 40 |
| **Combined network** | **Two targets** | **297** | **295** |

The two branches have no shared basin IDs. Both connect downstream to basin `1060022420`. The combined network contains generations 0–39, with no duplicate basin IDs, invalid geometries, or downstream links outside the exported network.

#### 6.3.2 Hydrological consistency

The combined upstream cumulative area for the two target basins is approximately **2,069,192.6 km²**. Including the downstream basin's reported sub-area of 29,461.2 km² gives approximately **2,098,653.8 km²**, compared with its reported upstream area of 2,098,663.8 km². The difference is approximately 10 km² (about 0.0005%).

This close agreement provides an internal consistency check for the exported basin network. It does not independently establish the real-world river identity or validate hydrological flow direction.

#### 6.3.3 Interpretation and limitations

- Target A and Target B are retained as neutral identifiers. Their identities must not be labelled as the Niger and Benue branches until independently verified using authoritative river-network information.
- HydroBASINS features represent drainage catchments, not river-channel geometries.
- The combined network is a broad upstream hydrological context for investigating potential upstream influences on Lokoja. It is not the local floodplain boundary.
- Its large spatial extent does not imply that every included catchment contributes equally or immediately to flooding at Lokoja.
- Further hydrological analysis should consider travel time, rainfall distribution, river discharge, connectivity and the temporal relationship between upstream conditions and observed flooding.

#### 6.3.4 Retained outputs

The following processed files document the combined network:

- `data/processed/hydrobasins_combined_upstream_network_lokoja.geojson`
- `data/processed/hydrobasins_combined_upstream_attributes_lokoja.csv`

The earlier single-branch outputs are retained for comparison:

- `data/processed/hydrobasins_upstream_network_lokoja.geojson`
- `data/processed/hydrobasins_upstream_attributes_lokoja.csv`

The combined network is the current working hydrological study-area definition. Any future changes must be documented with the source dataset version, basin identifiers, processing method and validation results.
### 6.4 Boundary decision record

For each study-area geometry, record:

- Name, purpose and version.
- Source dataset(s) and original identifiers.
- Selection, tracing and editing rules.
- CRS and area/length calculation method.
- Date created and software/script version.
- Quality checks and known uncertainties.
- Whether the geometry is provisional or approved for analysis.

## 7. Scientific terminology

NigeriaFloodWatch will use the following terms consistently.

**Flood observation:** Evidence that surface water/inundation was present at an observed time, obtained from satellite imagery, field observations, reports or another documented source.

**Flood extent / inundation footprint:** A spatial representation of the area observed or interpreted to be inundated for a specified event and observation time. It must include source, time and confidence information.

**Flood susceptibility:** The relatively persistent predisposition of a location to inundation based on terrain, geomorphology, drainage, proximity to channels and other relatively static or slowly changing characteristics. Susceptibility is not a time-specific forecast.

**Flood hazard:** The likelihood and, where data permit, characteristics of flooding at a particular location and time or forecast period. A forecast probability is a hazard estimate, not a risk estimate.

**Exposure:** People, settlements, buildings, roads, services, agricultural land and other assets located in areas that may be affected.

**Vulnerability:** The propensity of exposed people or assets to suffer harm, given their physical, social, economic and other characteristics.

**Flood risk:** Potential consequences arising from the interaction of flood hazard with exposure and vulnerability. A hazard probability alone must not be called a complete risk estimate.

## 8. Forecasting objective and prediction contract

### 8.1 Intended target

The intended forecasting target is the probability that a defined spatial unit experiences observed inundation during a forecast-valid period extending up to 72 hours after a forecast issue time.

Let:

- `u` be a defined spatial unit (for example, a river reach, hydrological unit, floodplain cell or settlement unit, depending on the validated modelling design);
- `t0` be the forecast issue time;
- `H` be the forecast-valid horizon, with a maximum initial value of 72 hours;
- `Y(u, t0, H)` be the flood label for that unit and valid period;
- `X(t0)` be the information genuinely available at the issue time.

The intended probability is:

`P(Y(u, t0, H) = 1 | X(t0))`

The operational meaning of `Y=1` will be “documented inundation is present in or intersects unit `u` at one or more valid observation times within the forecast window,” subject to a declared minimum evidence/quality rule. If the project later chooses to predict *new flood onset* rather than inundation presence/continuation, that will be a separately specified target and label.

The initial product should distinguish whether flooding was already observed at or before `t0` from whether inundation is observed during the forecast-valid period. This prevents a continuation forecast from being misrepresented as a prediction of new onset.

### 8.2 Forecast time semantics

Every prediction record must contain:

- `issued_at`: when the prediction was generated.
- `valid_from` and `valid_to`: the period the prediction describes.
- `lead_time`: the lead from issue time to the relevant forecast period.
- `input_as_of`: latest information timestamp permitted in the predictor set.
- Source forecast issue/run times and valid times for forecast inputs.

All stored timestamps should use UTC. User-facing display may be converted to Africa/Lagos time, but the original UTC timestamps must be retained.

The 72-hour horizon is a maximum intended horizon, not a promise of hourly output. Forecast time steps must be constrained by the temporal resolution of the available forecasts and labels. Daily windows may be used if the source products and observed labels cannot support finer lead-time resolution.

### 8.3 Prediction unit and spatial resolution

The final prediction unit and grid size are **not fixed in this specification**. They must be selected after the following are assessed together:

- Native spatial support of forecast rainfall and discharge products.
- Resolution and uncertainty of terrain inputs.
- Spatial resolution and effective mapping accuracy of flood labels.
- Density and representativeness of historical events.
- Hydrological connectivity and the intended decision use.

Upsampling a coarse product to a fine grid does not create new spatial information. The system must not describe resampled 0.05° rainfall or a coarse hydrological forecast as genuine 10 m input information.

The architecture therefore supports multiple spatial supports: catchment/reach-scale hydrological predictors, local inundation footprints, and settlement/exposure summaries. A common analytical grid will only be established when scientifically justified.

### 8.4 Forecast feature eligibility and leakage rules

Predictor inputs for a forecast issued at `t0` must represent information available by `t0`.

Permitted input categories may include:

- Archived rainfall or river-discharge forecasts issued no later than `t0`, for their corresponding valid periods.
- Observations and derived antecedent conditions available by `t0`.
- Static or slowly varying terrain, river-network and land-surface characteristics valid for the study period.
- Historical flood state known by `t0`, where its observation timestamp and availability are documented.

Not permitted as forecast predictors:

- Satellite scenes acquired after `t0`.
- Observed rainfall or discharge from after `t0` substituted for the forecast that would have been available at `t0`.
- Post-event reports, flood footprints or labels from the forecast-valid period.
- Future-derived aggregates or normalisations that use information unavailable at `t0`.

Sentinel-1 imagery acquired during or after an event may support flood mapping and label construction. It must not be used as a predictor for a forecast issued before that acquisition.

Historical observed rainfall and reanalysis discharge can support retrospective analysis, climatology and feature development. They do not by themselves reproduce the information available to an operational forecaster. Genuine forecast evaluation requires archived forecast vintages/reforecasts or another carefully justified as-issued reconstruction.

### 8.5 Missing and uncertain labels

Absence of a detected flood in an image is not automatically a valid negative label. Cloud-free SAR availability, acquisition time, water-detection limitations, image coverage, vegetation/urban effects and independent evidence must be considered.

The label system must support at least three states:

- `1`: flood evidence meets the documented positive-label rule.
- `0`: adequate observation/evidence supports a non-flood label for the target unit and valid period.
- `unknown`: evidence is missing, ambiguous, temporally mismatched or insufficient.

Unknown labels must not be silently converted to zero. Label confidence, source, observation time, event identifier and evidence limitations must be retained.

## 9. Data-source roles (conceptual)

The data inventory and source/licence register remain the authoritative place for detailed product metadata. At specification level, candidate roles are:

| Data family | Candidate source | Intended role | Important distinction |
|---|---|---|---|
| SAR imagery | Sentinel-1 GRD via Earth Engine | Historical water/inundation observation and event-label support | Observation product, not a future forecast input unless acquired before issue time |
| Historical rainfall | CHIRPS v3 | Antecedent rainfall and historical climatology | Satellite/gauge-blended estimate; product vintage and preliminary/final status matter |
| Forecast rainfall | CHIRPS-GEFS | As-issued forecast precipitation features | Forecast cycle and valid time must be archived; do not substitute realised rainfall |
| Terrain | SRTM / NASADEM candidate | Elevation and terrain derivatives | Static conditioning information; resolution and artefacts must be assessed |
| Hydrography | HydroSHEDS / HydroBASINS | River network and drainage topology | Must be checked against local geography and network connectivity |
| Hydrological history | GloFAS historical/reanalysis | Modelled historical discharge and hydrological state | Not equivalent to in-situ gauge observations |
| Hydrological forecasts | GloFAS forecast/reforecast products | Ensemble discharge forecast features and baseline comparison | Product version, issue time, ensemble members and valid times must be retained |
| Exposure | OpenStreetMap and official sources | Settlements, buildings, roads and infrastructure | Data completeness and ODbL attribution/share-alike obligations must be respected |
| Flood event evidence | NIHSA, NIWA, NEMA, UNOSAT and other documented sources | Event chronology, reports, flood footprints and independent validation | Availability, accuracy, licence and spatial/temporal specificity are not yet established |

The exact dataset version, coverage, access method, file format and licence will be verified in the Phase 1 data inventory and licence register before production use.


| Dataset | Spatial / temporal characteristics | Licence / access | Inventory status |
| :--- | :--- | :--- | :--- |
| **UN SALB Nigeria** | Administrative polygons; temporal validity 2000–latest listed update, 8 Aug 2024 | Non-commercial use only; geometry/content changes require contributor consent | Acquired; boundary QA completed |
| **HydroBASINS v1, Level 6** | Global nested sub-basins; derived from 15-arc-second HydroSHEDS core data | Free scientific, educational and commercial use, subject to HydroSHEDS terms | Acquired; 297-feature candidate network QA completed |
| **Sentinel-1 GRD** | 10, 25 or 40 m product resolutions; archive begins October 2014; acquisition-dependent revisit | Copernicus Sentinel Data Terms | Initial GEE exploration completed; acquisition workflow needs consolidation |
| **CHIRPS v3 daily** | 0.05°; daily; 1981–near present | Public domain | Sample acquisition previously explored; exact exported sample and QA need recording |
| **SRTM** | 1 arc-second global product, approximately 30 m at the equator | NASA/USGS data access; retain source acknowledgement | Sample acquisition previously explored; exact raster and QA need recording |
| **OpenStreetMap** | Vector features; update frequency and completeness vary by location | ODbL; attribution and share-alike obligations apply | Sample data previously explored; extract date and download method need recording |
| **Copernicus EMSR314_02** | Event-specific September 2018 flood mapping; vector layers and AOI | Free reuse subject to CEMS terms and source attribution | Acquired; flood geometry QA and LGA clipping completed |
| **GloFAS** | Historical daily discharge; GloFAS v4 historical coverage from 1979 to near present, 0.05° | Copernicus Climate Data Store access and applicable terms | Access and relevant Lokoja grid cells still need confirmation |
| **NIHSA observations** | River-level and discharge data may be available by station and period | Request-based; access, timing and fees depend on data | Request not yet completed |
| **NIWA / NEMA / UNOSAT** | Historical evidence and records vary by source and event | Source-specific terms | Further source-level verification required |

### Sources
* **UN SALB terms and Nigeria metadata:** [salb.un.org](https://un.org) (+1)
* **HydroBASINS documentation:** [hydrosheds.org](https://hydrosheds.org) (+1)
* **Sentinel-1 and CHIRPS catalogues:** [developers.google.com](https://google.com) (+2)
* **SRTM product guide:** [earthdata.nasa.gov](https://nasa.gov)
* **OSM licence:** OpenStreetMap
* **Copernicus EMS terms:** Copernicus EMS On Demand Mapping
* **GloFAS technical documentation:** ECMWF Confluence Wiki (+1)
* **NIHSA request process:** NIHSA

> **A significant licence issue:** UN SALB's published terms restrict SALB data to non-commercial use and prohibit geometry/content changes without contributor consent ([salb.un.org](https://un.org)). We can use the extracted boundary for this research subject to those terms, but we must review this before distributing a commercial **NigeriaFloodWatch** product based on that boundary.


## 10. Model-development strategy

Model choice will be driven by label quality, predictor availability, sample size, spatial/temporal dependence and validation results—not by model complexity.

### 10.1 Required baselines

Candidate baseline methods include:

- Persistence/current-state baseline where a valid current flood-state observation exists.
- Climatology or event-frequency baseline where enough historical observations exist.
- Published operational hydrological forecast information (for example, GloFAS) as a comparator where relevant.
- Logistic Regression for a transparent statistical baseline.
- Random Forest and/or gradient-boosted trees (such as XGBoost) for nonlinear tabular predictors.

### 10.2 Conditional advanced approaches

- U-Net or related segmentation architectures only if sufficiently numerous, consistent and independently checked flood-extent labels are available.
- Temporal deep learning only if the project has sufficiently long, time-aligned hydrological/meteorological series and enough independent flood events.
- Hydrodynamic or hydraulic modelling only if the required channel geometry, cross-sections, bathymetry, boundary conditions, calibration information and computational resources can be obtained.

A hybrid or multi-stage approach may ultimately be more defensible than one model that mixes all spatial scales. The project should first establish whether it can predict catchment/reach-scale hazard, map local inundation, or both, and only then validate any coupling between those outputs.

## 11. Evaluation requirements

Random pixel-level splits alone are not acceptable because adjacent pixels and repeated observations from the same flood event are spatially and temporally dependent.

Evaluation should include, as data permit:

- Chronological train/validation/test separation.
- Event-held-out testing so that observations from the same event do not appear in both training and test sets.
- Spatially blocked testing where transfer to unseen locations is claimed.
- Separate reporting by lead time, event, season and spatial subregion.
- Comparison with simple and operational baselines.
- Probability calibration and reliability assessment.
- Explicit review of false alarms and missed floods.

Candidate metrics:

- Precision, recall/sensitivity and F1-score.
- Precision–Recall AUC (especially where flood labels are rare).
- ROC-AUC as a secondary discrimination metric.
- Brier score and reliability/calibration plots.
- False-alarm ratio, probability of detection and critical success index where appropriate.
- Spatial overlap metrics such as intersection-over-union for flood segmentation/extent products.

Decision thresholds and acceptable performance levels must be determined after the data audit and baseline experiments. No performance threshold is asserted in advance.

## 12. Intended outputs

### 12.1 Research and data outputs

- Versioned study-area geometries and boundary decision records.
- Data inventory, source/licence register and data dictionary.
- Reproducible acquisition and preprocessing scripts/notebooks.
- Quality-assured sample datasets and quality reports.
- Historical flood-event catalogue and evidence-linked labels, if available.
- Feature datasets with explicit temporal and spatial metadata.
- Model experiment records and validation reports in later phases.

### 12.2 Future platform outputs

Once validated, the platform may expose:

- Observed flood extents with observation timestamps and source.
- Static susceptibility layers clearly labelled as such.
- Location- or unit-specific flood-hazard probabilities for supported lead times.
- Data-availability and input-freshness status.
- Model version and prediction issue/valid times.
- Uncertainty and limitations.
- Exposure overlays, separately from hazard predictions.

An API response must be able to say “no prediction available” or “insufficient input coverage”; missing inputs must not be represented as zero flood probability.

## 13. Non-functional requirements

- **Scientific traceability:** Each result can be traced to data versions, code, processing parameters and model version.
- **Reproducibility:** Acquisition and transformations are scripted or clearly recorded.
- **Modularity:** Ingestion, preprocessing, labels, features, modelling and serving have separate responsibilities.
- **Spatial correctness:** CRS, units, grid definitions, georeferencing and resampling methods are explicit.
- **Temporal correctness:** Issue time, valid time, acquisition time and observation time are distinct fields.
- **Interoperability:** Use documented open geospatial and scientific formats where practical.
- **Cost awareness:** Prefer server-side Earth Engine processing, small representative exports and on-demand compute; avoid unnecessary bulk downloads.
- **Maintainability:** Keep code, notebooks, configurations and data manifests organised.
- **Security:** Never commit API keys, service-account keys, CDS tokens or private credentials.
- **Communication:** Maps and predictions must explain whether they are observations, susceptibility, forecast hazard or risk.

## 14. Research and engineering constraints

1. The data foundation takes priority over early model production.
2. No dataset is “complete” until a representative acquisition and quality check have been demonstrated.
3. Source observations, reanalysis, forecasts and model outputs must remain distinguishable.
4. Source spatial resolution and temporal resolution must not be overstated after resampling or aggregation.
5. Raw source files should be immutable where practical; transformations create new, traceable outputs.
6. Large raw rasters and repeated satellite exports should not be committed to Git.
7. The initial computing arrangement is GitHub Codespaces for repository/application development, Google Colab for interactive research, and Google Earth Engine for server-side geospatial processing. This is a working arrangement, not a requirement to store all data in any one of those services.
8. Google Drive may be used as a convenient temporary workspace for small notebook outputs. It is not the authoritative source of truth for code, metadata or reproducibility.
9. Google Cloud Storage and paid cloud services will be introduced only when storage, automation or deployment needs justify the recurring costs.
10. Phase 1 must be completed before the Phase 2 roadmap is introduced.

## 15. Phase 1 completion criteria

Phase 1 is complete only when the following have evidence attached:

1. Repository audit report covering tracked files, code, GEE scripts, data, tests and configuration.
2. Project specification and architecture baseline accepted.
3. Three study-area concepts documented, with defensible provisional or final geometries and uncertainty statements.
4. Data inventory populated with provider, source, coverage, resolution, time range, format, CRS, licence, access and limitations.
5. Separate source and licence register established.
6. Working GEE acquisition workflow demonstrated for Sentinel-1 GRD with query metadata and a small export/sample.
7. Representative CHIRPS v3, SRTM and OSM samples acquired and quality-checked.
8. GloFAS historical/forecast/reforecast access and version assessment documented.
9. NIHSA, NIWA, NEMA and UNOSAT record availability investigated and documented.
10. Consolidated sample-data quality report produced.
11. Unresolved data access, label, spatial coverage and scientific limitations recorded.

A task is not complete merely because a script exists or an Earth Engine task has been submitted; the resulting data and quality checks must be verified.

## 16. Known uncertainties and decision gates

The following remain open and must be resolved with evidence:

- Exact boundaries of the local floodplain and the contributing Niger–Benue hydrological area.
- HydroBASINS target-basin selection, topology and treatment of the candidate `1060909900` branch.
- Verified local identity/connectivity of river reaches near Lokoja.
- Meaning, units and temporal interpretation of HydroBASINS `UP_AREA` and HydroSHEDS `DIS_AV_CMS` attributes.
- Availability and quality of local water-level/discharge gauge records.
- Availability of event-dated flood footprints with adequate spatial accuracy.
- Whether archived CHIRPS-GEFS and GloFAS forecast vintages/reforecasts cover enough past events for operationally honest backtesting.
- Most defensible prediction unit, grid size and lead-time intervals.
- Whether a local 72-hour inundation forecast is achievable with available evidence or whether the first validated product should be at catchment/reach scale.

No unresolved item may be silently converted into an assumed fact.

## 17. Long-term direction

NigeriaFloodWatch should progress from a well-documented Lokoja pilot to additional Nigerian flood-prone environments only after the data pipeline, event labels, validation strategy and limitations are understood. Expansion should reuse the architecture while allowing region-specific hydrological, terrain, data-availability and exposure differences.

---

## References and technical documentation

The links below identify key authoritative documentation consulted for this specification. Dataset versions and access terms must be rechecked during acquisition because catalogues and APIs change.

1. [Google Earth Engine — Sentinel-1 SAR GRD data catalogue](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD)
2. [Google Earth Engine — Sentinel-1 algorithms and filtering guidance](https://developers.google.com/earth-engine/guides/sentinel1)
3. [Climate Hazards Center — CHIRPS v3](https://chc.ucsb.edu/data/chirps3)
4. [Climate Hazards Center — data products, including CHIRPS-GEFS](https://www.chc.ucsb.edu/data)
5. [Copernicus / ECMWF — GloFAS historical data](https://ewds.climate.copernicus.eu/datasets/cems-glofas-historical?tab=overview)
6. [Copernicus / ECMWF — GloFAS forecast data](https://ewds.climate.copernicus.eu/datasets/cems-glofas-forecast?tab=overview)
7. [Copernicus — CDS API setup](https://cds.climate.copernicus.eu/en/how-to-api)
8. [Copernicus — CEMS flood datasets licence](https://cds.climate.copernicus.eu/licences/cems-floods)
9. [Google Earth Engine — Python installation in Colab](https://developers.google.com/earth-engine/guides/python_install-colab)
10. [Google Earth Engine — SRTM and other elevation datasets catalogue](https://developers.google.com/earth-engine/datasets/catalog)
11. [OpenStreetMap — copyright and licence](https://www.openstreetmap.org/copyright)
