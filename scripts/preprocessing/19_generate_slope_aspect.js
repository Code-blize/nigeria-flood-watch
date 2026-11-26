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
  sampleAOI.area(1).divide(1e6)
);

print('========== INSPECTION COMPLETE ==========');

// --------------------------------------------------
// 11. INVESTIGATE NEGATIVE ELEVATION PIXELS
// --------------------------------------------------

var negativeMask = elevation.lt(0).selfMask();

var negativeElevation = elevation.updateMask(negativeMask);

var negativeCount = negativeElevation.reduceRegion({
  reducer: ee.Reducer.count(),
  geometry: sampleAOI,
  scale: 30,
  maxPixels: 1e9,
  tileScale: 4
});

var negativeStatistics = negativeElevation.reduceRegion({
  reducer: ee.Reducer.minMax(),
  geometry: sampleAOI,
  scale: 30,
  maxPixels: 1e9,
  tileScale: 4
});

print('Negative elevation pixel count:', negativeCount);

print('Negative elevation statistics:', negativeStatistics);

// Display negative elevation locations.
Map.addLayer(
  negativeElevation,
  {
    min: -20,
    max: 0,
    palette: ['red', 'yellow']
  },
  'Negative elevation pixels'
);

// --------------------------------------------------
// 12. INSPECT SOURCE-DATA CLASS COUNTS
// --------------------------------------------------

var sourceHistogramDictionary = ee.Dictionary(
  sourceHistogram.get('num')
);

print(
  'Source-data class codes:',
  sourceHistogramDictionary.keys()
);

print(
  'Source-data class pixel counts:',
  sourceHistogramDictionary.values()
);

// --------------------------------------------------
// 13. INSPECT WATER PIXELS
// --------------------------------------------------

var waterHistogramDictionary = ee.Dictionary(
  waterHistogram.get('swb')
);

print(
  'Water-body class codes:',
  waterHistogramDictionary.keys()
);

print(
  'Water-body pixel counts:',
  waterHistogramDictionary.values()
);

// --------------------------------------------------
// 14. CHECK SOURCE CLASSES OF NEGATIVE PIXELS
// --------------------------------------------------

var negativeSourceDistribution = sourceIndex
  .updateMask(negativeMask)
  .reduceRegion({
    reducer: ee.Reducer.frequencyHistogram(),
    geometry: sampleAOI,
    scale: 30,
    maxPixels: 1e9,
    tileScale: 4
  });

print(
  'Source classes contributing to negative elevations:',
  negativeSourceDistribution
);
// --------------------------------------------------
// 15. LOCATE NEGATIVE ELEVATION PIXELS
// --------------------------------------------------

var negativePixelSamples = nasadem
  .select(['elevation', 'num', 'swb'])
  .sample({
    region: sampleAOI,
    scale: 30,
    geometries: true,
    tileScale: 4
  })
  .filter(ee.Filter.lt('elevation', 0));

print(
  'Negative elevation pixel details:',
  negativePixelSamples
);

var negativeList = negativePixelSamples.toList(2);

var negative1 = ee.Feature(negativeList.get(0));
var negative2 = ee.Feature(negativeList.get(1));

print('Negative pixel 1 properties', negative1.toDictionary());
print('Negative pixel 1 coordinates', negative1.geometry().coordinates());

print('Negative pixel 2 properties', negative2.toDictionary());
print('Negative pixel 2 coordinates', negative2.geometry().coordinates());

// --------------------------------------------------
// STEP 5: GENERATE SLOPE AND ASPECT
// --------------------------------------------------

// Project elevation to a metre-based CRS before terrain calculations.
var elevationUTM = nasadem
  .select('elevation')
  .resample('bilinear')
  .reproject({
    crs: 'EPSG:32632',
    scale: 30
  });

// Calculate terrain derivatives.
var terrain = ee.Terrain.products(elevationUTM);

var slope = terrain.select('slope').clip(sampleAOI);
var aspect = terrain.select('aspect').clip(sampleAOI);

// Export slope in degrees.
Export.image.toDrive({
  image: slope,
  description: 'Lokoja_NASADEM_slope',
  folder: 'NigeriaFloodWatch',
  fileNamePrefix: 'terrain/slope_nasadem_lokoja',
  region: sampleAOI,
  crs: 'EPSG:32632',
  scale: 30,
  fileFormat: 'GeoTIFF',
  maxPixels: 1e13
});

// Export aspect in degrees.
Export.image.toDrive({
  image: aspect,
  description: 'Lokoja_NASADEM_aspect',
  folder: 'NigeriaFloodWatch',
  fileNamePrefix: 'terrain/aspect_nasadem_lokoja',
  region: sampleAOI,
  crs: 'EPSG:32632',
  scale: 30,
  fileFormat: 'GeoTIFF',
  maxPixels: 1e13
});