# NigeriaFloodWatch
## Project Specification

**Version:** 0.1  
**Project status:** Initial development  
**Pilot location:** Lokoja, Kogi State, Nigeria  
**Primary hazard:** Riverine flooding  
**Target forecast horizon:** 72 hours

---

## 1. Project Overview

NigeriaFloodWatch is a geospatial intelligence and machine-learning platform designed to monitor, analyse and predict flood hazards across Nigeria.

The project will initially focus on Lokoja, Kogi State, a strategically important riverine environment situated near the confluence of the Niger and Benue rivers.

The platform will integrate satellite remote sensing, rainfall observations, meteorological forecasts, hydrological information, terrain characteristics and historical flood records to develop a data-driven flood prediction system.

Its primary objective is to estimate the probability of flood occurrence at specific locations within a defined forecast horizon, initially targeting the next 72 hours.

NigeriaFloodWatch will provide access to flood intelligence through a REST API and an interactive geospatial interface.

The project combines Geographic Information Systems (GIS), remote sensing, hydrological analysis, machine learning, deep learning, data engineering, MLOps, backend development and cloud computing.

## 2. Background and Motivation

Flooding is a significant environmental hazard affecting communities, infrastructure, agricultural activities and economic systems across Nigeria.

Riverine flooding is particularly relevant to communities situated along major river systems. Lokoja provides an important case study because of its geographical position near the Niger–Benue confluence.

Understanding and forecasting flood events in this environment requires the integration of multiple environmental variables, including rainfall, upstream river discharge, elevation, terrain characteristics, drainage networks and historical inundation patterns.

These variables are produced by different observation systems and datasets, often with different spatial resolutions, temporal frequencies, formats and levels of uncertainty.

NigeriaFloodWatch seeks to establish a reproducible geospatial data and machine-learning framework capable of transforming these heterogeneous datasets into useful flood intelligence.

## 3. Problem Statement

Reliable flood forecasting requires timely access to environmental and hydrological information, appropriate data integration methods and models capable of representing the physical and temporal processes associated with flooding.

However, satellite observations, rainfall datasets, river-discharge forecasts, terrain information and historical flood records are not necessarily available in a single harmonised analytical framework.

This creates challenges in understanding flood dynamics, identifying vulnerable locations and estimating the likelihood of future flood occurrence.

NigeriaFloodWatch will address this technical challenge by developing an integrated geospatial and machine-learning pipeline that processes relevant environmental data and produces location-specific flood hazard estimates.

The project will investigate the feasibility of short-term flood forecasting over a 72-hour horizon, with Lokoja serving as the initial pilot environment.

## 4. Project Aim

To develop a geospatial machine-learning platform that integrates satellite observations, rainfall information, hydrological forecasts, terrain characteristics and historical flood records to estimate and communicate flood hazards across Nigeria.

## 5. Specific Objectives

1. Acquire relevant satellite, meteorological, hydrological, terrain and historical flood datasets.
2. Develop reproducible data acquisition and preprocessing pipelines.
3. Harmonise heterogeneous geospatial datasets for integrated analysis.
4. Investigate historical flood patterns and environmental characteristics in Lokoja.
5. Develop meaningful spatial and temporal features for flood prediction.
6. Construct a labelled dataset suitable for machine-learning and deep-learning experiments.
7. Develop, train and evaluate suitable flood prediction models.
8. Investigate the use of forecast rainfall and river discharge for 72-hour flood prediction.
9. Develop a REST API for delivering model predictions.
10. Build an interactive geospatial interface for communicating flood information.
11. Containerise, deploy and monitor the application using cloud infrastructure.
12. Establish reproducible MLOps workflows for experiment tracking, model versioning and deployment.

## 6. Study Area

### 6.1 Pilot Location

Lokoja, Kogi State, Nigeria.

### 6.2 Geographical Rationale

Lokoja is situated near the confluence of the Niger and Benue rivers.

Its geographical position makes it relevant for investigating riverine flood processes influenced by rainfall and hydrological conditions across upstream catchments.

### 6.3 Study Area Structure

The geographical design will use two complementary areas:

**Core study area:**
- Lokoja urban environment.
- Surrounding floodplains.
- River corridors.
- Low-lying settlements.
- Relevant infrastructure and exposed assets.

**Hydrological context area:**
- Relevant upstream portions of the Niger catchment.
- Relevant upstream portions of the Benue catchment.
- River network and contributing drainage areas.
- Locations relevant to hydrological observations and forecasts.

Exact boundaries, grid dimensions and coordinate reference systems will be established during the geospatial data investigation.

## 7. Scientific Scope

The project distinguishes three related concepts:

**Flood susceptibility:** The relative predisposition of a location to flooding based on physical characteristics.

**Flood hazard:** The likelihood and potential characteristics of a flood event occurring in a particular location and period.

**Flood risk:** The potential consequences of a flood hazard considering exposure and vulnerability.

The primary predictive objective is flood hazard estimation.

The broader platform will progressively incorporate exposure and vulnerability information to support flood-risk analysis.

## 8. Functional Requirements

The system should:

1. Acquire relevant environmental and hydrological datasets.
2. Process satellite imagery and derive flood-related information.
3. Generate rainfall, terrain and hydrological features.
4. Maintain a structured historical flood-event dataset.
5. Construct machine-learning datasets using temporally valid observations.
6. Train and evaluate flood prediction models.
7. Generate location-specific flood hazard estimates.
8. Expose predictions through a REST API.
9. Visualise observed flood extent and model outputs on an interactive map.
10. Provide prediction timestamps, forecast horizons and model-version information.
11. Support automated data updates and model-serving workflows.
12. Record relevant application and prediction metadata.

## 9. Non-Functional Requirements

The system should aim for:

- **Reliability:** Predictions should be based on validated inputs and documented model behaviour.
- **Reproducibility:** Data processing and experiments should be repeatable.
- **Scalability:** Architecture should support expansion beyond Lokoja.
- **Maintainability:** Components should have clearly defined responsibilities.
- **Performance:** API responses should meet defined latency targets.
- **Security:** Application endpoints and infrastructure should follow appropriate security practices.
- **Observability:** Data pipelines, API services and model behaviour should be monitored.
- **Interoperability:** Geospatial outputs should use documented and compatible formats.
- **Transparency:** Data sources, uncertainty, limitations and model versions should be communicated.

## 10. Data Sources

The initial candidate datasets include:

| Dataset | Intended application |
|---|---|
| Sentinel-1 SAR | Satellite-based flood observation and inundation mapping |
| CHIRPS v3 | Historical rainfall analysis |
| CHIRPS-GEFS | Forecast rainfall |
| SRTM DEM | Elevation and terrain derivatives |
| OpenStreetMap | River networks, roads, buildings and infrastructure |
| GloFAS | Historical and forecast river discharge |
| UNOSAT | Historical satellite-derived flood extent |
| NIHSA | Hydrological information and flood bulletins |
| NIWA | River observations and water-level information |
| NEMA | Historical flood reports and disaster information |

Dataset access, temporal coverage, spatial resolution, licensing and suitability will be verified before use.

## 11. Proposed Technology Stack

### Geospatial Processing
- Google Earth Engine
- ArcGIS Pro
- Python
- Rasterio
- GDAL
- GeoPandas
- xarray
- Shapely

### Machine Learning and Deep Learning
- Python
- NumPy
- Pandas
- scikit-learn
- XGBoost
- PyTorch
- MLflow

### Data Engineering
- Python-based ingestion pipelines
- Raster and vector data processing
- Structured dataset storage
- Automated data validation

### Backend Development
- FastAPI
- Pydantic
- REST API architecture

### MLOps and Software Engineering
- Docker
- GitHub Actions
- MLflow
- Automated testing
- Model versioning
- Pipeline monitoring

### Cloud Infrastructure
- Google Cloud Run
- Google Cloud Storage or an appropriate object-storage alternative

### Frontend and Visualisation
- Leaflet
- Deck.gl
- JavaScript or TypeScript
- Interactive geospatial maps

## 12. Proposed System Architecture

The proposed architecture consists of the following layers:

1. **Data acquisition layer:** Acquires satellite, rainfall, hydrological, terrain and historical flood datasets.
2. **Data processing layer:** Performs quality checks, preprocessing, spatial harmonisation and feature extraction.
3. **Geospatial data layer:** Stores and organises processed raster, vector and time-series information.
4. **Machine-learning layer:** Constructs training datasets, trains models and generates predictions.
5. **MLOps layer:** Tracks experiments, manages model versions and supports reproducible deployment.
6. **API layer:** Exposes model predictions and relevant metadata through FastAPI.
7. **Cloud infrastructure layer:** Hosts the API and supports automated application deployment.
8. **Presentation layer:** Provides an interactive map and user-facing flood intelligence interface.

Heavy satellite processing and model training will be separated from the API-serving workload.

## 13. Prediction Objective

The intended forecasting target is the occurrence of flooding at a defined location within the next 72 hours.

For a spatial unit i and prediction time t:

Y(i,t) = 1 if flooding occurs within the following 72 hours, and 0 otherwise.

The model will estimate:

P(Y(i,t) = 1 | X(i,t))

where X represents environmental and hydrological information available at the prediction time.

The exact spatial unit, flood-event definition, label-generation procedure and forecast timing will be established during dataset construction.

The prediction target must be supported by time-stamped historical flood observations and appropriate forecast inputs.

Sentinel-1 observations will primarily support flood detection, mapping and historical label generation. They will not be treated as independent evidence of future flooding.

## 14. Model Development Strategy

The modelling process will be evidence-driven.

Candidate approaches include:

- Logistic Regression as a simple baseline.
- Random Forest for nonlinear tabular classification.
- XGBoost for gradient-boosted decision trees.
- Convolutional neural networks for satellite-image analysis.
- U-Net for flood segmentation where suitable labelled imagery is available.
- Temporal deep-learning architectures where sufficient sequential hydrological data exists.

Models will be evaluated using appropriate classification metrics, including precision, recall, F1-score, PR-AUC, ROC-AUC and probability calibration.

Temporal and spatial validation will be used to reduce data leakage.

## 15. API and Platform Capabilities

The intended API should support:

- Location-specific flood prediction requests.
- Forecast horizon selection, subject to validated model capabilities.
- Prediction timestamps.
- Flood probability outputs.
- Relevant environmental and hydrological input summaries.
- Model version and metadata retrieval.
- Health and service-status checks.

The interactive platform should distinguish observed flood information from derived geospatial layers and model-generated predictions.

## 16. Deployment Strategy

The application will be containerised using Docker.

FastAPI will provide the backend service, while Google Cloud Run will be investigated as the primary deployment environment.

GitHub Actions will support automated testing and deployment workflows.

MLflow will support experiment tracking and model lifecycle management.

The cloud architecture will separate computationally intensive geospatial processing from real-time prediction serving.

## 17. Evaluation and Success Criteria

Project success will be evaluated through:

**Data engineering**
- Reproducible data ingestion.
- Documented dataset quality.
- Successful spatial harmonisation.
- Reliable update procedures.

**Geospatial analysis**
- Correct spatial alignment.
- Validated flood extent products.
- Documented spatial and temporal limitations.

**Machine learning**
- Evaluation against unseen flood events.
- Appropriate predictive performance.
- Probability calibration.
- Analysis of false positives and false negatives.

**API and deployment**
- Working prediction endpoints.
- Automated tests.
- Successful container deployment.
- Documented API performance.

**Product delivery**
- Interactive geospatial visualisation.
- Accessible documentation.
- Clear communication of uncertainty and limitations.

Performance thresholds will be defined after inspecting the available data and establishing baseline model results.

## 18. Risks and Limitations

Potential risks include:

- Limited historical flood labels.
- Incomplete river gauge observations.
- Inconsistent satellite observation dates.
- Different spatial resolutions across datasets.
- Missing or uncertain historical event timestamps.
- Forecast uncertainty in rainfall and river discharge.
- Class imbalance in flood occurrence data.
- Spatial and temporal data leakage.
- Computational and cloud infrastructure costs.
- Model generalisation challenges beyond the pilot area.

These risks will be documented and addressed throughout development.

## 19. Development Phases

1. Project foundation and data availability assessment.
2. Geospatial data acquisition and preprocessing.
3. Historical flood analysis and dataset construction.
4. Machine-learning and deep-learning development.
5. Model evaluation and experiment tracking.
6. API development and integration.
7. Containerisation and cloud deployment.
8. Interactive mapping and product release.

## 20. Long-Term Vision

NigeriaFloodWatch will begin as a pilot flood intelligence platform for Lokoja and progressively investigate expansion to other flood-prone regions of Nigeria.

The long-term ambition is to establish a reproducible, scalable and scientifically defensible platform that bridges geospatial intelligence, hydrological forecasting and machine learning to support flood preparedness and decision-making.
