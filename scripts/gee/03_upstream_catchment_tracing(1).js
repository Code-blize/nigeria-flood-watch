
/************************************************************
 NIGERIA FLOOD WATCH
 SCRIPT 03: UPSTREAM CATCHMENT TRACING
 Dataset: HydroBASINS Level 6
 Target: Lokoja basin
 HYBAS_ID: 1060909890
************************************************************/

// 1. Load HydroBASINS
var basins = ee.FeatureCollection(
  'WWF/HydroSHEDS/v1/Basins/hybas_6'
);

// 2. Define Lokoja basin
var lokojaID = 1060909890;

// 3. Initialise upstream search
var frontier = ee.List([lokojaID]);

var allUpstream = ee.FeatureCollection([]);

// 4. Trace upstream through 10 generations
for (var level = 1; level <= 50; level++) {

  var upstream = basins.filter(
    ee.Filter.inList('NEXT_DOWN', frontier)
  );

  // Record generation number
  var tagged = upstream.map(function(feature) {
    return feature.set('upstream_level', level);
  });

  allUpstream = allUpstream.merge(tagged);

  // Prepare next generation
  frontier = upstream.aggregate_array('HYBAS_ID');

  // Report results
  print(
    'Generation ' + level + ' basin count:',
    upstream.size()
  );

  print(
    'Generation ' + level + ' basin IDs:',
    frontier
  );
}

// 5. Summary
print('Total upstream features:', allUpstream.size());

print(
  'Generation distribution:',
  allUpstream.aggregate_histogram('upstream_level')
);

// 6. Display upstream network
Map.layers().reset([]);

Map.addLayer(
  allUpstream.style({
    color: '168AAD',
    fillColor: '168AAD18',
    width: 1
  }),
  {},
  'Upstream catchment network'
);

// 7. Highlight Lokoja basin
var lokojaBasin = basins.filter(
  ee.Filter.eq('HYBAS_ID', lokojaID)
);

Map.addLayer(
  lokojaBasin.style({
    color: 'FF0000',
    fillColor: 'FF000033',
    width: 3
  }),
  {},
  'Lokoja target basin'
);

Map.centerObject(lokojaBasin, 6);


// ======================================================
// STEP 5: SAVE THE UPSTREAM CATCHMENT NETWORK
// ======================================================

// Remove duplicate basin IDs, if any
var uniqueUpstream = allUpstream.distinct(['HYBAS_ID']);

// Retrieve Lokoja target basin
var lokojaBasin = basins.filter(
  ee.Filter.eq('HYBAS_ID', 1060909890)
).map(function(feature) {
  return feature.set({
    upstream_level: 0,
    network_role: 'Lokoja target basin'
  });
});

// Label upstream features
uniqueUpstream = uniqueUpstream.map(function(feature) {
  return feature.set(
    'network_role',
    'Upstream contributing basin'
  );
});

// Combine target basin and upstream network
var completeNetwork = uniqueUpstream.merge(lokojaBasin);

print('Unique upstream basins:', uniqueUpstream.size());
print('Complete network including Lokoja:', completeNetwork.size());

// Export complete network with geometries
Export.table.toDrive({
  collection: completeNetwork,
  description: 'NigeriaFloodWatch_HydroBASINS_Upstream_Network',
  folder: 'NigeriaFloodWatch',
  fileNamePrefix: 'hydrobasins_upstream_network_lokoja',
  fileFormat: 'GeoJSON'
});

// Export tabular attributes separately
Export.table.toDrive({
  collection: completeNetwork,
  description: 'NigeriaFloodWatch_HydroBASINS_Attributes',
  folder: 'NigeriaFloodWatch',
  fileNamePrefix: 'hydrobasins_upstream_attributes_lokoja',
  selectors: [
    'HYBAS_ID',
    'NEXT_DOWN',
    'MAIN_BAS',
    'UP_AREA',
    'upstream_level',
    'network_role'
  ],
  fileFormat: 'CSV'
});

// ==========================================
// 4. IDENTIFY THE NIGER AND BENUE RIVER
// ==========================================

// Approximate Lokoja location
var lokojaPoint = ee.Geometry.Point([6.74, 7.80]);

// Load HydroSHEDS free-flowing river network
var rivers = ee.FeatureCollection(
  'WWF/HydroSHEDS/v1/FreeFlowingRivers'
);

// Select river features within 50 km of Lokoja
var riversAroundLokoja = rivers.filterBounds(
  lokojaPoint.buffer(50000)
);

// Inspect the dataset
print('River reaches around Lokoja:', riversAroundLokoja.size());

print(
  'Example river attributes:',
  riversAroundLokoja.first()
);

// Display the river network
Map.addLayer(
  riversAroundLokoja.style({
    color: '00FFFF',
    width: 2
  }),
  {},
  'HydroSHEDS river network'
);

// Display Lokoja
Map.addLayer(
  lokojaPoint,
  {color: 'FFFFFF'},
  'Approximate Lokoja location'
);

Map.centerObject(lokojaPoint, 8);

// ==========================================
// 5. INSPECT MAJOR RIVER REACHES
// ==========================================

// Get named rivers in the Lokoja search area
var riverNames = ee.List(
  riversAroundLokoja.aggregate_array('BB_NAME')
).distinct();

print('River names in search area:', riverNames);

// Keep higher-order river reaches
var majorRivers = riversAroundLokoja.filter(
  ee.Filter.lte('RIV_ORD', 4)
);

print('Major river reaches:', majorRivers.size());

// Sort by long-term average discharge
var largestReaches = majorRivers
  .sort('DIS_AV_CMS', false)
  .limit(20);

// Inspect their attributes
print(
  'Top 20 major river reaches by average discharge:',
  largestReaches
);

// Visualise the major river network
Map.addLayer(
  majorRivers.style({
    color: 'FF0000',
    width: 3
  }),
  {},
  'Major river reaches'
);

// ==========================================
// 6. INSPECT RIVER NETWORK ATTRIBUTES
// ==========================================

print(
  'Available river fields:',
  ee.Feature(riversAroundLokoja.first()).propertyNames()
);

print(
  'River name frequency:',
  riversAroundLokoja.aggregate_histogram('BB_NAME')
);

print(
  'River order frequency:',
  riversAroundLokoja.aggregate_histogram('RIV_ORD')
);

print(
  'Sample of 10 river reaches:',
  riversAroundLokoja.limit(10)
);

// Inspect the 20 largest reaches individually
print(
  'Largest river reach attributes:',
  largestReaches.aggregate_array('BB_NAME')
);

print(
  'Largest reach discharge:',
  largestReaches.aggregate_array('DIS_AV_CMS')
);

print(
  'Largest reach river order:',
  largestReaches.aggregate_array('RIV_ORD')
);

// Inspect the complete attributes of the largest river reach
var largestReach = ee.Feature(largestReaches.first());

print(
  'Largest reach complete properties:',
  largestReach.toDictionary()
);

// Inspect network identifiers for the 20 largest reaches
var networkRecords = largestReaches.map(function(feature) {
  feature = ee.Feature(feature);

  return ee.Feature(null, {
    BB_NAME: feature.get('BB_NAME'),
    RIV_ORD: feature.get('RIV_ORD'),
    DIS_AV_CMS: feature.get('DIS_AV_CMS'),
    NOID: feature.get('NOID'),
    NDOID: feature.get('NDOID')
  });
});

print('River network identifiers:', networkRecords);

// Display the largest reaches separately
Map.addLayer(
  largestReaches.style({
    color: 'FF0000',
    width: 4
  }),
  {},
  '20 largest river reaches'
);

// ==========================================
// EXPORT ALL 457 RIVER REACHES FOR ANALYSIS
// ==========================================

var riverTable = riversAroundLokoja.map(function(feature) {
  feature = ee.Feature(feature);

  var coordinates = feature.geometry()
    .centroid(100)
    .coordinates();

  return ee.Feature(
    feature.geometry(),
    feature.toDictionary([
      'GOID',
      'REACH_ID',
      'BAS_ID',
      'BAS_NAME',
      'BB_ID',
      'BB_NAME',
      'BB_DIS_ORD',
      'RIV_ORD',
      'DIS_AV_CMS',
      'UPLAND_SKM',
      'NOID',
      'NDOID',
      'NUOID',
      'COUNTRY',
      'INC',
      'CSI_FF'
    ])
  ).set({
    longitude: coordinates.get(0),
    latitude: coordinates.get(1)
  });
});

print('Total exported river reaches:', riverTable.size());

Export.table.toDrive({
  collection: riverTable,
  description: 'NigeriaFloodWatch_Lokoja_River_Network',
  folder: 'NigeriaFloodWatch',
  fileNamePrefix: 'lokoja_river_network_attributes',
  selectors: [
    'GOID', 'REACH_ID', 'BAS_ID', 'BAS_NAME',
    'BB_ID', 'BB_NAME', 'BB_DIS_ORD',
    'RIV_ORD', 'DIS_AV_CMS', 'UPLAND_SKM',
    'NOID', 'NDOID', 'NUOID', 'COUNTRY',
    'INC', 'CSI_FF', 'longitude', 'latitude'
  ],
  fileFormat: 'CSV'
});
