# NigeriaFloodWatch — Data Source and Licence Register

**Project:** NigeriaFloodWatch  
**Study area:** Lokoja, Kogi State, Nigeria  
**Register version:** 1.0  
**Last reviewed:** 13 November 2026  
**Status:** Initial source and licence assessment

## 1. Purpose

This register records the authoritative source, access route, licence or usage conditions, attribution requirements, and outstanding permissions for datasets used or proposed for NigeriaFloodWatch.

The register is intended to support reproducibility, responsible data use, research publication, and possible future deployment of a public-facing flood-monitoring service.

A dataset being publicly accessible does not automatically mean that it can be redistributed without conditions. The licence applying to the actual downloaded product must be checked and retained with the data.

## 2. Source and licence register

| Dataset | Authoritative source | Access route | Licence / usage position | Required action |
|---|---|---|---|---|
| Lokoja LGA boundary | Original supplied administrative boundary dataset; source metadata to be confirmed | Local project archive | Licence not yet established from the retained file | Identify original provider and record its licence before redistribution |
| Copernicus EMSR314_02 flood extent and contextual layers | Copernicus Emergency Management Service | EMS activation product archive | CEMS On-Demand Mapping information is made available under its terms for free, full and open use. Independent rights created through modification or adaptation remain with the creator. Third-party content may have separate terms. | Retain activation ID, product version, source attribution and original archive |
| HydroBASINS | HydroSHEDS / HydroBASINS | HydroSHEDS product download | HydroBASINS is available for scientific, educational and commercial use under the applicable HydroSHEDS product licence. Product-specific licence terms apply. | Retain the product licence and cite Lehner and Grill (2013) |
| Sentinel-1 SAR | European Union Copernicus Sentinel programme / ESA | Copernicus Data Space Ecosystem or Google Earth Engine catalogue | Sentinel data are available on a free, full and open basis, including reproduction, distribution, adaptation and combination, subject to applicable legal limitations. | Record product ID, platform, acquisition time, processing level and processing history |
| CHIRPS v3 | Climate Hazards Center, University of California, Santa Barbara | CHC data repository or supported catalogue | CC BY 4.0 International. CHC also describes CHIRPS3 as public domain to the extent possible under law. | Attribute CHC, retain version and access date, and include the recommended dataset citation |
| CHIRPS-GEFS | Climate Hazards Center / NCEP GEFS | CHC data repository | Confirm the applicable terms for the specific forecast product and distribution route before redistribution. | Record forecast initialization time, lead time, product version and licence information |
| SRTM elevation | NASA / USGS | NASA Earthdata, USGS EarthExplorer or supported catalogue | Terms depend on the specific SRTM product and distribution source. Do not assume all derived or third-party elevation products have identical conditions. | Record product identifier, version, resolution, provider and applicable data-use statement |
| OpenStreetMap | OpenStreetMap contributors / OpenStreetMap Foundation | OSM data extracts or supported APIs | Open Database License (ODbL). Attribution is required. Adapted or derived database distributions may trigger share-alike obligations. | Include OSM attribution and assess ODbL implications before distributing derived databases |
| GloFAS | Copernicus Emergency Management Service / ECMWF | Copernicus Climate Data Store or Early Warning Data Store | CEMS Early Warning Data Store terms provide free access and permit reproduction, distribution, communication, adaptation and combination, subject to restrictions and attribution requirements. Some datasets may be access-restricted. | Accept the applicable dataset terms and retain the required Copernicus attribution |
| NIHSA hydrological observations | Nigeria Hydrological Services Agency | Formal data request | Access, fees and sharing conditions depend on the requested data and NIHSA approval. NIHSA requires acknowledgement and restricts redistribution without permission. | Submit a formal request and retain written permission and usage conditions |
| NIWA observations | Nigerian Institute for Waterways and related official sources, where applicable | Direct institutional request or official data portal | No dataset-specific licence or public redistribution permission confirmed for this project. | Confirm the responsible data holder, access process, fees and written usage conditions |
| UNOSAT flood evidence | United Nations Satellite Centre (UNOSAT) | UNOSAT product portal or individual product download | Terms may differ by product and accompanying data. Do not assume unrestricted redistribution. | Record product-specific terms, attribution and any restrictions |
| NEMA flood records | National Emergency Management Agency, Nigeria | Official publications or formal data request | No general open-data licence confirmed for the specific records proposed for this project. | Request permission and document any restrictions on publication or redistribution |

## 3. Confirmed source requirements

### 3.1 Sentinel-1

- Source: Copernicus Sentinel-1.
- Use the official Sentinel data legal notice.
- Record the satellite platform, product identifier, acquisition date/time, orbit direction, relative orbit, polarisation, product type and processing parameters.
- Distinguish original satellite observations from processed or derived products.
- Do not imply that Copernicus endorses NigeriaFloodWatch.

### 3.2 CHIRPS v3

- Source: Climate Hazards Center, UC Santa Barbara.
- Licence: Creative Commons Attribution 4.0 International.
- Recommended dataset citation: Funk et al. (2026), *The Climate Hazards Center Infrared Precipitation with Stations, Version 3*, Scientific Data.
- DOI: https://doi.org/10.1038/s41597-026-07096-4
- Dataset DOI: https://doi.org/10.15780/G2JQ0P
- Record the version, temporal product, spatial resolution, access date and any transformations.

### 3.3 OpenStreetMap

- Licence: Open Database License (ODbL).
- Required attribution: © OpenStreetMap contributors.
- Licence information: https://www.openstreetmap.org/copyright
- Assess whether a distributed database is an adapted database or a produced work. Do not assume that every map image or analytical output automatically has the same licensing treatment as the underlying database.

### 3.4 HydroBASINS

- Source: HydroSHEDS.
- HydroBASINS product page: https://www.hydrosheds.org/products/hydrobasins
- Record the HydroBASINS version, level, region and download date.
- Retain the applicable product licence and technical documentation with the original data.

### 3.5 Copernicus Emergency Management Service

- Source: Copernicus EMS On-Demand Mapping.
- Activation: EMSR314 — Lokoja, Nigeria.
- Product: EMSR314_02 delineation product.
- Terms: https://mapping.emergency.copernicus.eu/terms-and-conditions/
- Retain the original downloaded archive and its product metadata.
- Identify derived geometries and processing operations separately from original Copernicus layers.

### 3.6 NIHSA

- Official data-request page: https://www.nihsa.gov.ng/request-data
- Access is subject to the Agency's review of the requested data and intended use.
- Do not publish or redistribute supplied observations without confirming the permission granted by NIHSA.
- Keep the request, response, invoice (if applicable), and permission terms in the project records.

### 3.7 GloFAS

- Source: Copernicus Emergency Management Service.
- Access and licence information: https://ewds.climate.copernicus.eu/licences/terms-of-use-cems
- Record the specific GloFAS dataset and version, not merely the platform name.
- Preserve forecast initialization dates and lead times for any forecast data used in model development.

## 4. Attribution and provenance requirements

For every downloaded dataset, maintain the following information:

1. Dataset name and provider.
2. Product name, identifier and version.
3. Original download or access URL.
4. Date accessed or downloaded.
5. Spatial and temporal coverage.
6. Licence name and licence URL, or written permission reference.
7. Required citation and attribution text.
8. Original filename and checksum where practical.
9. Processing steps and derived output filenames.
10. Any restrictions on redistribution, commercial use or publication.

Every derived dataset must be traceable to its source dataset and processing script.

## 5. Project distribution policy

Until the licence and permission status of each input is confirmed:

- Keep original downloaded datasets in the project's raw-data archive.
- Do not redistribute restricted third-party data through the public GitHub repository.
- Do not include restricted datasets in public application downloads or API responses.
- Publish source references, metadata, processing code and derived outputs only where their terms permit.
- Keep written data permissions and licence copies in project documentation.
- Review the combined licensing implications of datasets before releasing a derived database or commercial service.

The project's own code licence does not override the licence or access conditions of third-party datasets.

## 6. Outstanding licence checks

The following checks remain open:

- [ ] Confirm the original provider and licence of the Lokoja LGA boundary.
- [ ] Archive the exact HydroBASINS product licence used.
- [ ] Confirm the terms applicable to the specific CHIRPS-GEFS distribution.
- [ ] Confirm the terms for the exact SRTM product used.
- [ ] Obtain and document NIHSA data permissions if observations are supplied.
- [ ] Confirm NIWA data access and reuse conditions.
- [ ] Check the terms for each UNOSAT product selected.
- [ ] Obtain NEMA permission for any non-public records.
- [ ] Record all dataset-specific GloFAS terms accepted during download.

## 7. Official references

- Copernicus Sentinel data legal notice: https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice
- Copernicus Data Space terms: https://dataspace.copernicus.eu/terms-and-conditions
- CHIRPS v3: https://www.chc.ucsb.edu/data/chirps3
- HydroBASINS: https://www.hydrosheds.org/products/hydrobasins
- HydroSHEDS terms: https://www.hydrosheds.org/terms-of-use
- OpenStreetMap copyright and licence: https://www.openstreetmap.org/copyright
- Copernicus EMS terms: https://mapping.emergency.copernicus.eu/terms-and-conditions/
- Copernicus Early Warning Data Store terms: https://ewds.climate.copernicus.eu/licences/terms-of-use-cems
- NIHSA data request: https://www.nihsa.gov.ng/request-data
- Copernicus Climate Data Store terms: https://cds.climate.copernicus.eu/licences/terms-of-use-cds

---

**Important:** This is a working register. An item marked as requiring confirmation must not be treated as having an unrestricted open licence. Recheck the applicable product terms at the time of download and before public redistribution.
