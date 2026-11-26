/**
 * NigeriaFloodWatch
 * Script: 16_inspect_nasadem_source.js
 *
 * Purpose:
 * Inspect and verify the NASADEM elevation source
 * for the Lokoja study area.
 *
 * Dataset: NASADEM V001
 * Resolution: Approximately 30 m
 *
 * Outputs:
 * - Source band information
 * - Native projection and scale
 * - Valid elevation pixel count
 * - Elevation summary statistics
 * - Source-data index distribution
 * - Water-body mask distribution
 *
 * No exports are created in this step.
 */

// --------------------------------------------------
// 1. STUDY AREA
// --------------------------------------------------

var lokoja = ee.Geometry.Point([6.74, 7.80]);

var sampleAOI = lokoja.buffer(20000).bounds();

Map.centerObject(sampleAOI, 10);

Map.addLayer(
  sampleAOI,
  {color: 'red'},
  'Lokoja study area'
);

// --------------------------------------------------
// 2. LOAD NASADEM
// --------------------------------------------------

var nasadem = ee.Image('NASA/NASADEM_HGT/001');

print('========== NASADEM SOURCE INSPECTION ==========');

print('Dataset:', nasadem);

print('Available bands:', nasadem.bandNames());

// --------------------------------------------------
// 3. SELECT ELEVATION BAND
// --------------------------------------------------

var elevation = nasadem
  .select('elevation')
  .rename('elevation');

// --------------------------------------------------
// 4. INSPECT PROJECTION AND RESOLUTION
// --------------------------------------------------

var nativeProjection = elevation.projection();

print('Native projection:', nativeProjection);

print('Coordinate reference system:', nativeProjection.crs());

print('Nominal pixel scale (metres):',
  nativeProjection.nominalScale());

// --------------------------------------------------
// 5. VISUALISE ELEVATION
// --------------------------------------------------

Map.addLayer(
  elevation,
  {
    min: 0,
    max: 500,
    palette: [
      '08306b',
      '2171b5',
      '6baed6',
      'a1d99b',
      'ffffb2',
      'fd8d3c',
      'bd0026'
    ]
  },
  'NASADEM elevation (m)'
);

// --------------------------------------------------
// 6. CHECK VALID PIXEL COVERAGE
// --------------------------------------------------

var validPixelCount = elevation.reduceRegion({
  reducer: ee.Reducer.count(),
  geometry: sampleAOI,
  scale: 30,
  maxPixels: 1e9,
  tileScale: 4
});

print('Valid elevation pixel count:', validPixelCount);

// --------------------------------------------------
// 7. ELEVATION SUMMARY STATISTICS
// --------------------------------------------------

var elevationReducer = ee.Reducer.minMax()
  .combine(ee.Reducer.mean(), '', true)
  .combine(ee.Reducer.stdDev(), '', true);

var elevationStatistics = elevation.reduceRegion({
  reducer: elevationReducer,
  geometry: sampleAOI,
  scale: 30,
  maxPixels: 1e9,
  tileScale: 4
});

print('Elevation statistics (metres):', elevationStatistics);

// --------------------------------------------------
// 8. INSPECT SOURCE-DATA INDEX
// --------------------------------------------------

// The num band identifies the source contributing
// to each elevation pixel.

var sourceIndex = nasadem.select('num');

var sourceHistogram = sourceIndex.reduceRegion({
  reducer: ee.Reducer.frequencyHistogram(),
  geometry: sampleAOI,
  scale: 30,
  maxPixels: 1e9,
  tileScale: 4
});

print('Elevation source-data distribution:', sourceHistogram);

// --------------------------------------------------
// 9. INSPECT WATER-BODY MASK
// --------------------------------------------------

// 0 = Land
// 255 = Water

var waterMask = nasadem.select('swb');

var waterHistogram = waterMask.reduceRegion({
  reducer: ee.Reducer.frequencyHistogram(),
  geometry: sampleAOI,
  scale: 30,
  maxPixels: 1e9,
  tileScale: 4
});

print('Water-body mask distribution:', waterHistogram);

// --------------------------------------------------
// 10. STUDY AREA INFORMATION
// --------------------------------------------------

print('Study area geometry:', sampleAOI);

print(
  'Study area area (square kilometres):',
  sampleAOI.area().divide(1e6)
);

print('========== INSPECTION COMPLETE ==========');