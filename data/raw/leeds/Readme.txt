----------------
GENERAL INFORMATION
----------------


"Analysis inputs for validation of six global flood models against observed flood events in Nigeria and Mozambique"

Principle Author: Mark Bernhofen
Institution: University of Leeds
Address: School of Civil Engineering, University of Leeds, Leeds, UK, LS2 9JT
Email: cn13mvb@leeds.ac.uk

This dataset contains the inputs used for validation of six global flood models (GFMs) against observed events in Nigeria and Mozambique. The dataset includes shapefiles that contain the analysis areas for the three study regions of Lokoja, Idah, and Chemba. For each study region, the observed flooding (obtained from the Dartmouth Flood Observatory) is included in GeoTIFF raster format at a resolution of 1/1200 decimal degrees (~90m). For each study region, the modelled flood extent from 6 GFMs is included in GeoTIFF raster format, resampled to a resolution of 1/1200 decimal degrees (~90m). Individual GFM output is provided in return periods of 25 and 100 years. The GFMs included are: CaMa-Flood, GLOFRIS, ECMWF, JRC, SSBN, and CIMA-UNEP. Finally, for each study region, the 25 year return period aggregated flood model (an output from the Global Flood Model Intercomparison Project) is included in GeoTIFF raster format at a resolution of 1/1200 decimal degrees (~90m). Each file is in the WGS84 projection.

The file formats can be read by any Geographical Information System Software (GIS)

----------------
FILE OVERVIEW
----------------

Name: Analysis Areas
  contents: Analysis_Areas.zip
  description: Folder containing the analysis area shapefiles for Lokoja, Idah, and Chemba. The shapefiles are in WGS84 projection
Name: Observed Flooding
  contents: Observed_Flooding.zip
  description: Folder containing classified GeoTIFF raster data in the WGS84 projection representing cells in which floodings was observed for the respective flood event in Lokoja, Idah, and Chemba (note: for Lokoja and Idah: 1 - wet; 0 - dry/no data�for Chemba: 2 - wet; 1 - dry; 0 - no data)
Name: Aggregated Models
  contents: Aggregated_Models.zip
  description: Folder containing  classified GeoTIFF raster data in the WGS84 projection with integer value representing how many out of the 6 models agree that a cell is wet in in Lokoja, Idah, and Chemba. (note: 0 - dry/no data)
Name: Lokoja Global Flood Model Output
  contents: Lokoja_GFM_Output.zip
  description: Folder containing classified GeoTIFF Global Flood Model output in the WGS84 projection for return periods of 25 and 100 years in Lokoja. Global flood models include: SSBN, CaMa-Flood, CIMA-UNEP, GLOFRIS, JRC and ECMWF. All Global Flood Model output data is in 1/1200 decimal degree resolution (~90m). (note: 1 - wet; 0 - dry/no data) (note: SSBN output is 20 years not 25)
Name: Idah Global Flood Model Output
  contents: Idah_GFM_Output.zip
  description: Folder containing classified GeoTIFF Global Flood Model output in the WGS84 projection for return periods of 25 and 100 years in Idah. Global flood models include: SSBN, CaMa-Flood, CIMA-UNEP, GLOFRIS, JRC and ECMWF. All Global Flood Model output data is in 1/1200 decimal degree resolution (~90m). (note: 1 - wet; 0 - dry/no data) (note: SSBN output is 20 years not 25)
Name: Chemba Global Flood Model Output
  contents: Chemba_GFM_Output.zip
  description: Folder containing classified GeoTIFF Global Flood Model output in the WGS84 projection for return periods of 25 and 100 years in Chemba. Global flood models include: SSBN, CaMa-Flood, CIMA-UNEP, GLOFRIS, JRC and ECMWF. All Global Flood Model output data is in 1/1200 decimal degree resolution (~90m). (note: 1 - wet; 0 - dry/no data) (note: SSBN output is 20 years not 25)
