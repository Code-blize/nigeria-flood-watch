
/************************************************************
 NIGERIA FLOOD WATCH
 SCRIPT 03: RECURSIVE UPSTREAM CATCHMENT TRACING
 Dataset: HydroBASINS Level 6
 Target basin: Lokoja (1060909890)
************************************************************/

var basins = ee.FeatureCollection(
  'WWF/HydroSHEDS/v1/Basins/hybas_6'
);

var lokojaBasinID = 1060909890;

// Start with Lokoja's basin
var frontier = ee.List([lokojaBasinID]);

// Store all discovered upstream basins
var allUpstream = ee.FeatureCollection([]);

// Trace up to 10 upstream generations
for (var level = 1; level <= 10; level++) {

  var upstream = basins.filter(
    ee.Filter.inList('NEXT_DOWN', frontier)
  );

  // Record the generation at which each basin was found
  var tagged = upstream.map(function(feature) {
    return feature.set('upstream_level', level);
  });

  allUpstream = allUpstream.merge(tagged);

  // The newly discovered basins become the next search frontier
  frontier = upstream.aggregate_array('HYBAS_ID');

  print(
    'Upstream generation ' + level,
    upstream.size()
  );

  print(
    'Generation ' + level + ' basin IDs',
    frontier
  );
}

// Summary
print('Total upstream basin features:', allUpstream.size());

print(
  'All upstream basin IDs:',
  allUpstream.aggregate_array('HYBAS_ID')
);

// Calculate the total number of discovered features
print(
  'Upstream generation distribution:',
  allUpstream.aggregate_histogram('upstream_level')
);

// Display the discovered network
Map.addLayer(
  allUpstream.style({
    color: '00A6FF',
    fillColor: '00A6FF18',
    width: 1
  }),
  {},
  'Discovered upstream catchments'
);

var lokojaBasin = basins.filter(
  ee.Filter.eq('HYBAS_ID', lokojaBasinID)
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
