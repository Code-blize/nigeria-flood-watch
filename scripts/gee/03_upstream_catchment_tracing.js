
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
