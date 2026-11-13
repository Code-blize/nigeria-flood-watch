
/**
 * NigeriaFloodWatch
 * Script: 06_chirps_v3_sample_acquisition.js
 *
 * Purpose:
 * Acquire historical CHIRPS v3 daily rainfall for Lokoja.
 *
 * Period: September 2018
 * Product: CHIRPS v3 DAILY_RNL (ERA5-based)
 * AOI: 20 km buffer around Lokoja reference point.
 *
 * Outputs:
 * 1. Monthly accumulated rainfall GeoTIFF
 * 2. Daily AOI-mean rainfall CSV
 * 3. Acquisition metadata CSV
 */

// --------------------------------------------------
// 1. STUDY AREA
// --------------------------------------------------

var lokoja = ee.Geometry.Point([6.74, 7.80]);
var sampleAOI = lokoja.buffer(20000).bounds();

Map.centerObject(sampleAOI, 10);
Map.addLayer(sampleAOI, {color: 'red'}, 'Lokoja sample AOI');

// --------------------------------------------------
// 2. DATE RANGE
// --------------------------------------------------

var startDate = '2018-09-01';
var endDate = '2018-10-01';

// --------------------------------------------------
// 3. LOAD CHIRPS V3 DAILY REANALYSIS
// --------------------------------------------------

var chirps = ee.ImageCollection('UCSB-CHC/CHIRPS/V3/DAILY_RNL')
  .filterBounds(sampleAOI)
  .filterDate(startDate, endDate)
  .select('precipitation')
  .sort('system:time_start');

print('CHIRPS daily image count:', chirps.size());
print('CHIRPS collection:', chirps);

// --------------------------------------------------
// 4. CHECK COLLECTION
// --------------------------------------------------

var imageCount = chirps.size();

print('Expected daily images:', 30);
print('Actual daily images:', imageCount);

// --------------------------------------------------
// 5. MONTHLY ACCUMULATED RAINFALL
// --------------------------------------------------

var monthlyRainfall = chirps
  .sum()
  .rename('monthly_precipitation_mm')
  .clip(sampleAOI);

Map.addLayer(
  monthlyRainfall,
  {
    min: 0,
    max: 500,
    palette: ['white', 'lightblue', 'blue', 'darkblue']
  },
  'September 2018 accumulated rainfall'
);

print('Monthly rainfall image:', monthlyRainfall);

// --------------------------------------------------
// 6. DAILY AOI-MEAN RAINFALL TABLE
// --------------------------------------------------

var dailyRainfall = ee.FeatureCollection(
  chirps.map(function(image) {

    var dailyMean = image.reduceRegion({
      reducer: ee.Reducer.mean(),
      geometry: sampleAOI,
      scale: 5566,
      maxPixels: 1e8,
      bestEffort: true
    });

    return ee.Feature(null, {
      date: ee.Date(image.get('system:time_start'))
        .format('YYYY-MM-dd'),
      rainfall_mean_mm_day: dailyMean.get('precipitation'),
      dataset: 'CHIRPS_V3_DAILY_RNL'
    });

  })
);

print('Daily rainfall table:', dailyRainfall);

// --------------------------------------------------
// 7. ACQUISITION METADATA
// --------------------------------------------------

var metadata = ee.Feature(null, {
  dataset: 'UCSB-CHC/CHIRPS/V3/DAILY_RNL',
  version: 'CHIRPS v3',
  product: 'DAILY_RNL',
  temporal_basis: 'Daily estimates derived using ERA5',
  sample_area: 'Lokoja 20 km buffer',
  start_date: startDate,
  end_date_exclusive: endDate,
  expected_days: 30,
  spatial_resolution_m: 5566,
  rainfall_band: 'precipitation',
  rainfall_units: 'mm/day',
  monthly_output_units: 'mm/monthly accumulation',
  source: 'Climate Hazards Center, UC Santa Barbara'
});

var metadataTable = ee.FeatureCollection([metadata]);

print('Acquisition metadata:', metadataTable);

// --------------------------------------------------
// 8. EXPORT MONTHLY RAINFALL RASTER
// --------------------------------------------------

Export.image.toDrive({
  image: monthlyRainfall,
  description: 'NigeriaFloodWatch_CHIRPS_Lokoja_201809',
  folder: 'NigeriaFloodWatch',
  fileNamePrefix: 'chirps_v3_lokoja_2018_09_monthly',
  region: sampleAOI,
  scale: 5566,
  maxPixels: 1e9,
  fileFormat: 'GeoTIFF'
});

// --------------------------------------------------
// 9. EXPORT DAILY RAINFALL TABLE
// --------------------------------------------------

Export.table.toDrive({
  collection: dailyRainfall,
  description: 'NigeriaFloodWatch_CHIRPS_Lokoja_Daily_201809',
  folder: 'NigeriaFloodWatch',
  fileNamePrefix: 'chirps_v3_lokoja_2018_09_daily',
  fileFormat: 'CSV'
});

// --------------------------------------------------
// 10. EXPORT METADATA
// --------------------------------------------------

Export.table.toDrive({
  collection: metadataTable,
  description: 'NigeriaFloodWatch_CHIRPS_Lokoja_Metadata',
  folder: 'NigeriaFloodWatch',
  fileNamePrefix: 'chirps_v3_lokoja_metadata',
  fileFormat: 'CSV'
});
