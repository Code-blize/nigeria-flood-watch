
/**
 * NigeriaFloodWatch
 * Script: 05_sentinel1_sample_acquisition.js
 *
 * Purpose:
 * Acquire one Sentinel-1 GRD sample around Lokoja during
 * the September 2018 flood-event period.
 *
 * Temporary sample AOI: 20 km buffer around Lokoja reference point.
 * This is NOT the final local floodplain boundary.
 *
 * Outputs (Google Drive):
 * 1. Sentinel-1 VV/VH GeoTIFF
 * 2. Sentinel-1 acquisition metadata CSV
 */

// --------------------------------------------------
// 1. STUDY LOCATION AND SAMPLE AREA
// --------------------------------------------------

var lokoja = ee.Geometry.Point([6.74, 7.80]);

var sampleAOI = lokoja.buffer(20000).bounds();

Map.centerObject(sampleAOI, 10);
Map.addLayer(sampleAOI, {color: 'red'}, 'Temporary 20 km sample AOI');
Map.addLayer(lokoja, {color: 'yellow'}, 'Lokoja reference point');

// --------------------------------------------------
// 2. TEMPORAL WINDOW
// --------------------------------------------------

var startDate = '2018-09-01';
var endDate = '2018-10-01';

// --------------------------------------------------
// 3. SENTINEL-1 COLLECTION
// --------------------------------------------------

var sentinel1 = ee.ImageCollection('COPERNICUS/S1_GRD')
  .filterBounds(sampleAOI)
  .filterDate(startDate, endDate)
  .filter(ee.Filter.eq('instrumentMode', 'IW'))
  .filter(ee.Filter.listContains(
    'transmitterReceiverPolarisation', 'VV'
  ))
  .filter(ee.Filter.listContains(
    'transmitterReceiverPolarisation', 'VH'
  ))
  .select(['VV', 'VH'])
  .sort('system:time_start');

print('Sentinel-1 scenes found:', sentinel1.size());
print('Available Sentinel-1 scenes:', sentinel1);

// --------------------------------------------------
// 4. SELECT ONE SCENE
// --------------------------------------------------

var sampleImage = ee.Image(sentinel1.first()).clip(sampleAOI);

print('Selected sample image:', sampleImage);
print('Acquisition date:',
  ee.Date(sampleImage.get('system:time_start')).format('YYYY-MM-dd')
);

// --------------------------------------------------
// 5. VISUAL QUALITY CHECK
// --------------------------------------------------

Map.addLayer(
  sampleImage.select('VV'),
  {min: -25, max: 0},
  'Sentinel-1 VV'
);

Map.addLayer(
  sampleImage.select('VH'),
  {min: -30, max: -5},
  'Sentinel-1 VH'
);

// --------------------------------------------------
// 6. ACQUISITION METADATA
// --------------------------------------------------

var metadata = ee.Feature(null, {
  dataset: 'COPERNICUS/S1_GRD',
  sample_area: 'Lokoja 20 km buffer',
  start_date: startDate,
  end_date: endDate,
  acquisition_date: ee.Date(
    sampleImage.get('system:time_start')
  ).format('YYYY-MM-dd HH:mm:ss'),
  platform: sampleImage.get('platform_number'),
  instrument_mode: sampleImage.get('instrumentMode'),
  orbit_pass: sampleImage.get('orbitProperties_pass'),
  relative_orbit: sampleImage.get('relativeOrbitNumber_start'),
  polarisation: 'VV,VH',
  resolution_meters: sampleImage.get('resolution_meters'),
  product_type: sampleImage.get('productType'),
  system_index: sampleImage.get('system:index'),
  source: 'Google Earth Engine COPERNICUS/S1_GRD'
});

var metadataTable = ee.FeatureCollection([metadata]);

print('Acquisition metadata:', metadataTable);

// --------------------------------------------------
// 7. EXPORT SAMPLE IMAGE
// --------------------------------------------------

Export.image.toDrive({
  image: sampleImage,
  description: 'NigeriaFloodWatch_Sentinel1_Lokoja_2018_sample',
  folder: 'NigeriaFloodWatch',
  fileNamePrefix: 'sentinel1_lokoja_2018_sample',
  region: sampleAOI,
  scale: 10,
  maxPixels: 1e10,
  fileFormat: 'GeoTIFF'
});

// --------------------------------------------------
// 8. EXPORT METADATA
// --------------------------------------------------

Export.table.toDrive({
  collection: metadataTable,
  description: 'NigeriaFloodWatch_Sentinel1_Lokoja_2018_metadata',
  folder: 'NigeriaFloodWatch',
  fileNamePrefix: 'sentinel1_lokoja_2018_metadata',
  fileFormat: 'CSV'
});
