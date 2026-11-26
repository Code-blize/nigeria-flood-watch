// ==================================================
// NigeriaFloodWatch — Lokoja terrain preprocessing
// Dataset: NASADEM V001
// AOI: 20 km buffer around [6.74, 7.80], then bounds
// Outputs: raw elevation, standardized elevation,
//          slope, aspect
// ==================================================


// --------------------------------------------------
// 1. STUDY AREA AND SOURCE
// --------------------------------------------------

var lokoja = ee.Geometry.Point([6.74, 7.80]);
var sampleAOI = lokoja.buffer(20000).bounds();

var nasadem = ee.Image('NASA/NASADEM_HGT/001');
var rawElevation = nasadem.select('elevation').rename('elevation');

var targetCRS = 'EPSG:32632'; // WGS 1984 UTM Zone 32N
var targetScale = 30;         // metres

Map.centerObject(sampleAOI, 10);
Map.addLayer(sampleAOI, {color: 'red'}, 'Lokoja study area');


// --------------------------------------------------
// 2. RAW ELEVATION EXPORT
// Preserve NASADEM's original geographic grid.
// --------------------------------------------------

Export.image.toDrive({
  image: rawElevation,
  description: 'Lokoja_NASADEM_raw_elevation_v2',
  folder: 'NigeriaFloodWatch',
  fileNamePrefix: 'terrain/raw_elevation_nasadem_lokoja_v2',
  region: sampleAOI,
  crs: 'EPSG:4326',
  scale: 30.9220807759,
  fileFormat: 'GeoTIFF',
  maxPixels: 1e13
});


// --------------------------------------------------
// 3. STANDARDIZED ELEVATION
// Project to UTM Zone 32N at 30 metres.
// --------------------------------------------------

var elevationUTM = rawElevation
  .clip(sampleAOI)
  .resample('bilinear')
  .reproject({
    crs: targetCRS,
    scale: targetScale
  });

var standardizedElevation = elevationUTM.rename('elevation');

Export.image.toDrive({
  image: standardizedElevation,
  description: 'Lokoja_NASADEM_standardized_elevation_UTM32N_30m_v2',
  folder: 'NigeriaFloodWatch',
  fileNamePrefix: 'terrain/standardized_elevation_nasadem_lokoja_UTM32N_30m_v2',
  region: sampleAOI,
  crs: targetCRS,
  scale: targetScale,
  fileFormat: 'GeoTIFF',
  maxPixels: 1e13
});


// --------------------------------------------------
// 4. GENERATE SLOPE AND ASPECT
// --------------------------------------------------

var terrain = ee.Terrain.products(elevationUTM);

var slope = terrain
  .select('slope')
  .clip(sampleAOI)
  .rename('slope');

var aspect = terrain
  .select('aspect')
  .clip(sampleAOI)
  .rename('aspect');


// --------------------------------------------------
// 5. SLOPE EXPORT — degrees
// --------------------------------------------------

Export.image.toDrive({
  image: slope,
  description: 'Lokoja_NASADEM_slope_UTM32N_30m_v2',
  folder: 'NigeriaFloodWatch',
  fileNamePrefix: 'terrain/slope_nasadem_lokoja_UTM32N_30m_v2',
  region: sampleAOI,
  crs: targetCRS,
  scale: targetScale,
  fileFormat: 'GeoTIFF',
  maxPixels: 1e13
});


// --------------------------------------------------
// 6. ASPECT EXPORT — degrees
// --------------------------------------------------

Export.image.toDrive({
  image: aspect,
  description: 'Lokoja_NASADEM_aspect_UTM32N_30m_v2',
  folder: 'NigeriaFloodWatch',
  fileNamePrefix: 'terrain/aspect_nasadem_lokoja_UTM32N_30m_v2',
  region: sampleAOI,
  crs: targetCRS,
  scale: targetScale,
  fileFormat: 'GeoTIFF',
  maxPixels: 1e13
});


// --------------------------------------------------
// 7. VALIDATE TERRAIN VALUES
// --------------------------------------------------

print('Target CRS:', targetCRS);
print('Target scale (metres):', targetScale);

print('Elevation image projection:', elevationUTM.projection());
print('Slope image projection:', slope.projection());
print('Aspect image projection:', aspect.projection());

var terrainStats = standardizedElevation
  .rename('elevation_m')
  .addBands(slope.rename('slope_deg'))
  .addBands(aspect.rename('aspect_deg'))
  .reduceRegion({
    reducer: ee.Reducer.minMax()
      .combine(ee.Reducer.mean(), '', true)
      .combine(ee.Reducer.stdDev(), '', true)
      .combine(ee.Reducer.count(), '', true),
    geometry: sampleAOI,
    crs: targetCRS,
    scale: targetScale,
    maxPixels: 1e13,
    tileScale: 4
  });

print('Terrain validation statistics:', terrainStats);


// --------------------------------------------------
// 8. LIGHTWEIGHT MAP PREVIEWS
// Display at 90 m to reduce tile memory use.
// Exports above remain at 30 m.
// --------------------------------------------------

Map.addLayer(
  standardizedElevation.reproject({
    crs: targetCRS,
    scale: 90
  }),
  {min: 0, max: 550},
  'Elevation preview (90 m)'
);

Map.addLayer(
  slope.reproject({
    crs: targetCRS,
    scale: 90
  }),
  {min: 0, max: 45},
  'Slope preview (90 m)'
);

Map.addLayer(
  aspect.reproject({
    crs: targetCRS,
    scale: 90
  }),
  {min: 0, max: 360},
  'Aspect preview (90 m)'
);