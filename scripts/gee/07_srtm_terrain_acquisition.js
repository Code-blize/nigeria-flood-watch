
/**
 * NigeriaFloodWatch
 * Script: 07_srtm_terrain_acquisition.js
 *
 * Purpose:
 * Acquire SRTM elevation and derive slope/aspect.
 *
 * AOI: 20 km buffer around Lokoja reference point.
 *
 * Outputs:
 * 1. Elevation, slope and aspect GeoTIFF
 * 2. Terrain statistics CSV
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
// 2. LOAD SRTM
// --------------------------------------------------

var srtm = ee.Image('USGS/SRTMGL1_003')
  .select('elevation')
  .rename('elevation_m');

// Calculate terrain derivatives BEFORE clipping.
// This reduces artificial edge effects at the AOI boundary.
var terrain = ee.Terrain.products(srtm);

var slope = terrain.select('slope').rename('slope_degrees');
var aspect = terrain.select('aspect').rename('aspect_degrees');

// Combine all three bands.
var terrainStack = ee.Image.cat([
  srtm,
  slope,
  aspect
]).clip(sampleAOI);

print('SRTM elevation image:', srtm);
print('Terrain derivatives:', terrainStack);

// --------------------------------------------------
// 3. VISUAL INSPECTION
// --------------------------------------------------

Map.addLayer(
  srtm.clip(sampleAOI),
  {
    min: 20,
    max: 300,
    palette: ['blue', 'cyan', 'yellow', 'orange', 'brown']
  },
  'SRTM elevation'
);

Map.addLayer(
  slope.clip(sampleAOI),
  {
    min: 0,
    max: 30,
    palette: ['white', 'yellow', 'orange', 'red']
  },
  'Terrain slope'
);

Map.addLayer(
  aspect.clip(sampleAOI),
  {
    min: 0,
    max: 360,
    palette: ['blue', 'green', 'yellow', 'red']
  },
  'Terrain aspect',
  false
);

// --------------------------------------------------
// 4. TERRAIN STATISTICS
// --------------------------------------------------

var statistics = terrainStack.reduceRegion({
  reducer: ee.Reducer.minMax()
    .combine({
      reducer2: ee.Reducer.mean(),
      sharedInputs: true
    })
    .combine({
      reducer2: ee.Reducer.stdDev(),
      sharedInputs: true
    }),
  geometry: sampleAOI,
  scale: 30,
  maxPixels: 1e9,
  tileScale: 4
});

print('Terrain statistics:', statistics);

// Convert statistics dictionary to a CSV feature.
var statisticsFeature = ee.Feature(null, statistics)
  .set({
    dataset: 'USGS/SRTMGL1_003',
    sample_area: 'Lokoja 20 km buffer',
    spatial_resolution_m: 30
  });

var statisticsTable = ee.FeatureCollection([
  statisticsFeature
]);

// --------------------------------------------------
// 5. ACQUISITION METADATA
// --------------------------------------------------

var metadata = ee.Feature(null, {
  dataset: 'USGS/SRTMGL1_003',
  product: 'NASA SRTM V3 / SRTM Plus',
  provider: 'NASA / USGS / JPL-Caltech',
  sample_area: 'Lokoja 20 km buffer',
  spatial_resolution_m: 30,
  elevation_band: 'elevation',
  elevation_units: 'metres',
  slope_band: 'slope',
  slope_units: 'degrees',
  aspect_band: 'aspect',
  aspect_units: 'degrees',
  source: 'Google Earth Engine',
  processing: 'Elevation, slope and aspect'
});

var metadataTable = ee.FeatureCollection([metadata]);

print('Metadata:', metadataTable);

// --------------------------------------------------
// 6. EXPORT TERRAIN RASTER
// --------------------------------------------------

Export.image.toDrive({
  image: terrainStack,
  description: 'NigeriaFloodWatch_SRTM_Lokoja_Terrain',
  folder: 'NigeriaFloodWatch',
  fileNamePrefix: 'srtm_lokoja_elevation_slope_aspect',
  region: sampleAOI,
  scale: 30,
  maxPixels: 1e9,
  fileFormat: 'GeoTIFF'
});

// --------------------------------------------------
// 7. EXPORT TERRAIN STATISTICS
// --------------------------------------------------

Export.table.toDrive({
  collection: statisticsTable,
  description: 'NigeriaFloodWatch_SRTM_Lokoja_Statistics',
  folder: 'NigeriaFloodWatch',
  fileNamePrefix: 'srtm_lokoja_terrain_statistics',
  fileFormat: 'CSV'
});

// --------------------------------------------------
// 8. EXPORT METADATA
// --------------------------------------------------

Export.table.toDrive({
  collection: metadataTable,
  description: 'NigeriaFloodWatch_SRTM_Lokoja_Metadata',
  folder: 'NigeriaFloodWatch',
  fileNamePrefix: 'srtm_lokoja_metadata',
  fileFormat: 'CSV'
});
