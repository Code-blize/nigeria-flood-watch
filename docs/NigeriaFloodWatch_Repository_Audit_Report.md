# NigeriaFloodWatch — Repository Audit Report

**Audit date:** 11 November 2026  
**Repository:** https://github.com/Code-blize/nigeria-flood-watch  
**Branch inspected:** `main`  
**Latest inspected recursive tree SHA:** `b298841fa780b8d4a1d1a9f165afabb21e5186e4`  
**Audit scope:** Repository structure, tracked assets, Python source, Google Earth Engine scripts, tracked data, engineering configuration and documentation.  
**Audit type:** Read-only inspection. No repository files were changed.

---

## 1. Executive summary

NigeriaFloodWatch has a useful early-stage research repository. It contains substantive project specification and architecture documents, exploratory Google Earth Engine scripts, and two HydroBASINS exports. The HydroBASINS CSV was independently checked during this audit and is structurally consistent with a single target-basin network.

However, the repository is **not yet a functioning Python application or reproducible software pipeline**. The Python files and `pyproject.toml` are empty placeholders. There are no tests, configured dependencies, Docker build files or GitHub Actions workflows. Most requested environmental and historical-flood datasets are not tracked.

The repository is best described as an **early-stage geospatial research scaffold with initial hydrological exploration**, not an operational flood-monitoring or forecasting system.

The most important scientific limitation remains unresolved: the exported 256-feature HydroBASINS network traces upstream of one candidate target basin (`1060909890`). It has not been demonstrated to represent the complete Niger–Benue contributing catchments at Lokoja. The additional candidate `1060909900` remains to be assessed.

### Overall status

| Audit area | Result | Notes |
|---|---|---|
| Repository structure and asset inventory | Completed | Full recursive tree inspected; 26 tracked blobs and 12 directories. |
| Python code audit | Completed | Six Python files and `pyproject.toml` are one-byte newline placeholders. |
| GEE script audit | Static review completed | Substantive exploratory scripts inspected; scripts were not rerun in the user's Earth Engine account. |
| Data audit | Completed at repository inventory level; one content limitation | CSV independently checked; large GeoJSON geometry/CRS not independently inspected. |
| Engineering audit | Completed | No tests, dependency configuration, Docker build or CI workflow. |
| Documentation reconciliation | Completed | Current spec/architecture are version 1.0; inventory remains version 0.1. |
| Final audit report | Completed | Findings and actions consolidated here. |

---

## 2. Repository structure and tracked assets

The inspected tree contains 26 tracked files (blobs) and 12 actual directories. The repository's top-level structure has a sensible starting shape, but several paths that look like directories are actually one-byte files.

### 2.1 Tracked files

| Path | Size | Audit observation |
|---|---:|---|
| `.github/workflows` | 1 byte | A file, not a populated workflows directory. |
| `.gitignore` | 1 byte | Empty placeholder. |
| `LICENSE` | 1,077 bytes | MIT License. |
| `README.md` | 21 bytes | Contains only a project heading. |
| `data/figures/lokoja_river_basin_overlay_qa.png` | 119,161 bytes | QA image; not a substitute for spatial vector/raster data. |
| `data/processed/hydrobasins_upstream_attributes_lokoja.csv` | 18,439 bytes | Substantive attribute export; inspected. |
| `data/processed/hydrobasins_upstream_network_lokoja.geojson` | 5,864,402 bytes | Substantive spatial export; internal content could not be retrieved through the available GitHub file-reading route due to file size. |
| `data/raw` | 1 byte | A file, not a populated raw-data directory. |
| `docker/.gitignore` | 1 byte | Empty placeholder; no Dockerfile. |
| `docs/ARCHITECTURE.md` | 41,729 characters (retrieved text) | Version 1.0; substantive. |
| `docs/DATA_INVENTORY.md` | 6,132 characters (retrieved text) | Version 0.1; requires expansion and status corrections. |
| `docs/PROJECT_SPEC.md` | 28,329 characters (retrieved text) | Version 1.0; substantive. |
| `notebooks/.gitignore` | 1 byte | No tracked notebooks. |
| `pyproject.toml` | 1 byte | Empty placeholder. |
| `scripts/gee/01_hydrobasins_exploration.js` | 5,204 bytes | Substantive exploratory GEE script. |
| `scripts/gee/02_hydrobasins_network_analysis.js` | 1,783 bytes | Substantive exploratory GEE script. |
| `scripts/gee/03_glofas_exploration` | 1 byte | Empty placeholder; no `.js` extension. |
| `scripts/gee/03_upstream_catchment_tracing(1).js` | 7,933 bytes | Expanded tracing and river-network exploration script. |
| `scripts/gee/03_upstream_catchment_tracing.js` | 3,459 bytes | Earlier, shorter tracing script. |
| `src/api.py` | 1 byte | Empty placeholder. |
| `src/features.py` | 1 byte | Empty placeholder. |
| `src/ingestion/earth_engine.py` | 1 byte | Empty placeholder. |
| `src/model.py` | 1 byte | Empty placeholder. |
| `src/preprocessing.py` | 1 byte | Empty placeholder. |
| `src/utils.py` | 1 byte | Empty placeholder. |
| `test/.gitignore` | 1 byte | No tracked tests. |

Actual directories in the tree are `.github`, `data`, `data/figures`, `data/processed`, `docker`, `docs`, `notebooks`, `scripts`, `scripts/gee`, `src`, `src/ingestion` and `test`.

### 2.2 Structural discrepancies

- `.github/workflows` is currently a file rather than the conventional directory containing workflow YAML files.
- `data/raw` is a file rather than a directory.
- `data/interim`, `configs`, `models`, `reports` and `frontend` are not present in the inspected tree.
- `notebooks/`, `docker/` and `test/` contain only empty `.gitignore` placeholders.
- The agreed target structure should remain a target design; it should not be imposed wholesale before the data and engineering requirements are clear.

---

## 3. Python code audit

All six tracked Python files were fetched and inspected. Each contains only a newline; no imports, functions, classes, processing logic or error handling are implemented.

| File | Status |
|---|---|
| `src/api.py` | Empty placeholder |
| `src/features.py` | Empty placeholder |
| `src/model.py` | Empty placeholder |
| `src/preprocessing.py` | Empty placeholder |
| `src/utils.py` | Empty placeholder |
| `src/ingestion/earth_engine.py` | Empty placeholder |
| `pyproject.toml` | Empty placeholder |

**Conclusion:** The Python project structure has been sketched, but there is no functioning Python package, ingestion pipeline, feature pipeline, model or API. There are no active imports or dependencies to assess yet.

**Recommendation:** Retain these paths as placeholders. Do not implement a model or API during the repository audit. Dependency management and package layout should be introduced when the Phase 1 data workflows and their actual Python dependencies are established.

---

## 4. Google Earth Engine script audit

The substantive GEE scripts are exploratory and provide reusable starting points. They do not yet form a consolidated, parameterised and quality-controlled ingestion workflow.

### 4.1 Script findings

**`01_hydrobasins_exploration.js`**

- Loads `WWF/HydroSHEDS/v1/Basins/hybas_6`.
- Uses an approximate Lokoja point at `[6.74, 7.80]` and a 50 km buffer to find nearby candidate polygons.
- Contains repeated inspection and visualisation blocks, including redeclared `var` variables.
- `filterBounds` against a 50 km buffer identifies nearby polygons; it does not prove which polygon contains the reference point or which polygons contribute flow to the confluence.

**`02_hydrobasins_network_analysis.js`**

- Compares five candidate IDs: `1060909890`, `1060909900`, `1060892990`, `1060893000` and `1060022420`.
- Displays and prints their attributes.
- Does not itself establish full downstream/upstream topology or classify the two river branches.

**`03_upstream_catchment_tracing.js`**

- Traces upstream from `1060909890` for up to 10 generations.
- Exports a target-plus-upstream network and a CSV attribute table.
- Represents an earlier implementation.

**`03_upstream_catchment_tracing(1).js`**

- Extends the loop to 50 generations.
- Includes additional HydroSHEDS FreeFlowingRivers exploration.
- Continues the loop even after an empty frontier; the reported first empty generation was 40.
- Uses the same HydroBASINS export names as the earlier script, so the two versions should not remain competing canonical workflows.
- Adds a river CSV export for local reaches; the script's CSV selectors include attributes and centroid coordinates rather than a line geometry column.

**`03_glofas_exploration`**

- Empty one-byte file without a `.js` extension.
- No GloFAS query or data-access assessment is implemented.

### 4.2 HydroBASINS interpretation verified from the Earth Engine catalogue

For HydroBASINS Level 6:

- `NEXT_DOWN` identifies the next downstream polygon.
- `SUB_AREA` is the individual polygon area in km².
- `UP_AREA` is total upstream area in km².
- `MAIN_BAS` identifies the most downstream sink of the main basin.

Therefore, `UP_AREA` must not be interpreted as the area of an individual polygon. Use `SUB_AREA` for the individual polygon area. [1]

### 4.3 HydroSHEDS FreeFlowingRivers interpretation

The official Earth Engine catalogue describes FreeFlowingRivers as a static river-network product based on HydroSHEDS hydrography derived from 15 arc-second (approximately 500 m at the equator) source data. It is not a live or time-series river-monitoring dataset. [2]

The dataset's `DIS_AV_CMS` is long-term naturalised average discharge for 1971–2000, in m³/s. Its `RIV_ORD` field is a discharge-based class, not conventional Strahler stream order: lower numeric classes represent larger discharge. Thus `RIV_ORD <= 4` selects the larger discharge classes, but should not be described as a Strahler order filter. [2][3]

Backbone river names and network identifiers are useful for exploration, but local channel identity around Lokoja must be checked using geometry and network connectivity, with authoritative hydrological context. A backbone label alone is not conclusive evidence of the local channel name.

### 4.4 GEE audit conclusion

Retain the exploratory scripts and outputs. Before producing a canonical hydrological network workflow:

1. Resolve the candidate target basin and the additional `1060909900` branch.
2. Verify that the target location is correctly associated with the chosen downstream topology.
3. Trace all relevant contributing branches, not only the network upstream of one assumed target.
4. Verify local river reach connectivity and identity.
5. Consolidate duplicated tracing logic into one documented script after the topology is established.
6. Record dataset IDs, filters, date ranges where relevant, export formats, scale, CRS and processing parameters.

The scripts were statically inspected in this audit. Their execution was not rerun in the user's Earth Engine account.

---

## 5. Tracked data audit

### 5.1 HydroBASINS attribute CSV

The full tracked CSV was independently parsed and checked during this audit.

| Check | Result |
|---|---:|
| Data rows | 256 |
| Unique `HYBAS_ID` values | 256 |
| Duplicate IDs | 0 |
| Missing values across the six columns | 0 |
| Target basin records | 1 (`1060909890`) |
| Other upstream basin records | 255 |
| Maximum `upstream_level` | 39 |
| `UP_AREA` minimum | 189.7 km² |
| `UP_AREA` maximum | 1,730,224.9 km² |

The CSV contains `HYBAS_ID`, `NEXT_DOWN`, `MAIN_BAS`, `UP_AREA`, `upstream_level` and `network_role`.

A downstream graph check found that all 255 non-target basins point to another member of the exported network and all 256 records have a downstream path to target `1060909890`. No cycles were detected. The longest route to the target contains 39 downstream transitions.

**Interpretation:** This confirms internal consistency of the exported single-target network according to its `NEXT_DOWN` relationships. It does not establish that the target is the correct confluence outlet or that the network includes both Niger and Benue contributing branches.

### 5.2 HydroBASINS GeoJSON

The tracked GeoJSON is 5,864,402 bytes. The GitHub file-reading route rejected full retrieval of this large file, so its geometry types, coordinate reference information, geometry validity and feature-by-feature topology were not independently rechecked in this audit.

The project owner previously reported that the export had 256 features, 256 unique basin IDs and no missing IDs. That prior QA is recorded as owner-reported, not reproduced here.

### 5.3 QA image

`data/figures/lokoja_river_basin_overlay_qa.png` is a 119,161-byte PNG figure. It is a visual QA asset, not a source boundary or analysis-ready geospatial dataset.

### 5.4 Other reported outputs not tracked in this repository

The project continuation notes report the existence of:

- `lokoja_river_network_attributes.csv`
- `lokoja_major_river_network.geojson`
- A projected Lokoja LGA layer, `lokoja_lga_utm32n`

These outputs do not appear in the inspected GitHub tree. They may exist in ArcGIS Pro, Google Drive or another local location, but they are not currently tracked in this repository.

### 5.5 Candidate data not present

No tracked samples were found for:

- Sentinel-1 GRD.
- CHIRPS v3 rainfall.
- CHIRPS-GEFS forecasts.
- SRTM DEM.
- OpenStreetMap infrastructure/settlements.
- GloFAS historical, forecast or reforecast data.
- NIHSA or NIWA gauge/river records.
- NEMA historical flood-event records.
- UNOSAT historical flood footprints.
- A time-stamped historical flood-event catalogue or model labels.

This is consistent with the project's current early data-engineering stage; it must not be represented as successful acquisition.

### 5.6 Data audit conclusion

The tracked CSV has passed basic structural and single-network connectivity checks. The large GeoJSON's internal geometry/CRS checks remain outstanding. The repository does not yet contain the administrative boundary source file, the reported river-network exports or environmental sample datasets.

---

## 6. Engineering and reproducibility audit

| Capability | Current state | Finding |
|---|---|---|
| Python packaging | Missing | `pyproject.toml` is empty. |
| Dependency declaration | Missing | No `requirements.txt`, `environment.yml`, `uv.lock`, `poetry.lock` or equivalent. |
| Python version declaration | Missing | No supported Python version is documented in project configuration. |
| Tests | Missing | `test/` contains only an empty `.gitignore`. |
| Test configuration | Missing | No `pytest.ini`, `tox.ini` or equivalent. |
| Docker | Missing | No Dockerfile or Compose file. |
| CI | Missing | No workflow YAML; `.github/workflows` is a file, not a directory. |
| Root ignore rules | Missing | Root `.gitignore` is empty. |
| Environment template | Missing | No `.env.example`; no environment configuration is defined. |
| Notebooks | Missing | No tracked `.ipynb` files. |
| API | Not implemented | `src/api.py` is empty. |
| Model and features | Not implemented | Corresponding Python files are empty. |
| Data manifests | Missing | No machine-readable dataset manifest is tracked. |
| Data source/licence register | Missing | No dedicated register is present. |

The `LICENSE` file is MIT. This applies to the repository software/documentation as licensed by the project owner; it does not automatically grant rights to third-party satellite, rainfall, hydrological, administrative-boundary or OpenStreetMap data. Each data source needs its own licence and attribution record.

**Conclusion:** The repository is not currently reproducible as an installable Python project. Reproducibility infrastructure should be added when the actual Phase 1 acquisition and processing dependencies have been established, rather than installing a speculative full stack now.

---

## 7. Documentation reconciliation

### 7.1 `docs/PROJECT_SPEC.md` — Version 1.0

**Decision: Retain as the working baseline.**

Strengths:

- Explicitly distinguishes the administrative LGA, local floodplain analysis area and upstream Niger–Benue hydrological area.
- Separates susceptibility, hazard and risk.
- Defines forecast issue time, valid time, lead time and input-as-of time.
- Establishes leakage rules for forecast inputs.
- Distinguishes inundation presence/continuation from new flood onset.
- Supports positive, negative and unknown label states.
- Leaves spatial support and prediction grid open until evidence is assessed.
- Lists Phase 1 completion criteria and scientific decision gates.

### 7.2 `docs/ARCHITECTURE.md` — Version 1.0

**Decision: Retain, with a repository-state correction.**

Strengths:

- Separates satellite flood mapping, hydrological forecasting, susceptibility, exposure and serving.
- Uses GitHub Codespaces for repository development, Colab for research and Earth Engine for supported server-side geospatial processing.
- Uses manifests and file-based storage before considering a database or orchestration platform.
- Separates heavy geospatial processing/model training from the prediction API.
- Provides a target package layout without demanding an immediate restructure.

Correction required: Section 21 refers to an earlier repository tree SHA and older document state. It should be refreshed after this audit so the as-built snapshot matches the current `main` tree and current document versions.

### 7.3 `docs/DATA_INVENTORY.md` — Version 0.1

**Decision: Expand during Phase 1 Task 4.**

Issues:

- The export status is stale: it says the HydroBASINS exports are subject to successful completion, but the exports are now tracked.
- It does not contain the reproduced CSV QA statistics from this audit.
- It does not adequately document the FreeFlowingRivers work.
- It lacks required provider access, temporal coverage, update frequency, spatial resolution, format, CRS, licensing, quality and processing metadata for most sources.
- It needs clear distinctions between observations, historical model estimates, forecast products and reforecasts.

### 7.4 `README.md`

The README contains only `# nigeria-flood-watch`. It needs a project description, current status, scientific scope, repository navigation and setup guidance after the documentation baseline is settled.

---

## 8. What should be retained

Retain the following existing work:

1. The current repository and its general folder layout; do not rebuild from scratch.
2. `PROJECT_SPEC.md` version 1.0.
3. `ARCHITECTURE.md` version 1.0.
4. The original data inventory as the historical starting record, to be expanded rather than discarded.
5. The UN SALB-derived Lokoja LGA work and its EPSG:32632 working layer, while keeping the boundary file itself available for future QA.
6. The HydroBASINS Level 6 exploration scripts and the 256-record CSV/GeoJSON export.
7. The HydroSHEDS FreeFlowingRivers investigation and previously reported river-network exports, once the untracked outputs are located and checked.
8. The `data/figures` QA-image location.

Do not delete or overwrite existing GEE outputs until the topology review is complete.

---

## 9. Prioritised action plan

The audit identifies the following actions. These are recommendations and sequencing notes, not changes already applied.

### Priority 1 — Scientific and data integrity

1. Resolve whether basin `1060909900` contributes through the downstream confluence basin and establish the full upstream Niger–Benue topology.
2. Verify local river reach identities using geometry, network connectivity and authoritative hydrological context.
3. Independently inspect the tracked GeoJSON's CRS, geometry type, validity, feature count and attributes.
4. Locate and inspect the projected Lokoja LGA boundary and the reported river-network CSV/GeoJSON outputs.
5. Keep all unverified geometries explicitly provisional.

### Priority 2 — Data provenance and acquisition (later Phase 1 tasks)

6. Expand `DATA_INVENTORY.md` in Task 4 using verified source-specific metadata.
7. Create the separate data-source and licence register in Task 4.
8. Establish a machine-readable manifest for each acquired sample and derived asset.
9. Acquire Sentinel-1, CHIRPS v3, SRTM and OSM samples only in their designated roadmap tasks and quality-check them before marking them acquired.
10. Complete GloFAS and historical flood-record investigations in their designated tasks.

### Priority 3 — Engineering improvements when justified

11. Configure Python packaging and dependencies after actual package responsibilities and required libraries are known.
12. Add tests for geometry, data schemas, CRS, time handling, feature eligibility and pipeline outputs as the relevant components are implemented.
13. Add a correct `.github/workflows/` directory and CI checks after runnable tests exist.
14. Add Docker configuration when there is an application or reproducible service to containerise.
15. Update root ignore rules so local credentials, large raw datasets, temporary outputs and runtime artefacts are not committed accidentally.
16. Improve README after the project scope and setup instructions are stable.

---

## 10. Audit conclusion and Phase 1 gate

Task 1 has established the current repository state and documented its strengths, implementation gaps and scientific uncertainties.

**Task 1 outcome:** The repository audit is complete at the public-repository level, with a specific limitation recorded for independent inspection of the large GeoJSON's internal geometry and CRS. The owner's prior structural QA is acknowledged but not presented as independently reproduced. The GEE scripts were statically reviewed but not rerun in the owner's Earth Engine account.

The repository should not yet be described as a functioning flood prediction system. It is a research scaffold with exploratory hydrological analysis and an initial HydroBASINS export.

The audit does not authorise moving directly to model development or deployment. The next activity must follow the agreed Phase 1 roadmap in order.

---

## References

[1] Google Earth Engine Data Catalog — WWF HydroSHEDS Basins Level 6:  
https://developers.google.com/earth-engine/datasets/catalog/WWF_HydroSHEDS_v1_Basins_hybas_6

[2] Google Earth Engine Data Catalog — WWF HydroSHEDS FreeFlowingRivers:  
https://developers.google.com/earth-engine/datasets/catalog/WWF_HydroSHEDS_v1_FreeFlowingRivers

[3] WWF Free-flowing Rivers — Streams Fields:  
https://world-wildlife-fund.gitbook.io/free-flowing-rivers/annex/streams-fields

---

**End of report.**
