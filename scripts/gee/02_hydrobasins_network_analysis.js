
/************************************************************
 NIGERIA FLOOD WATCH
 SCRIPT 02: HYDROBASINS NETWORK ANALYSIS
 Study area: Lokoja, Kogi State, Nigeria
 Dataset: HydroBASINS Level 6
************************************************************/

// 1. Define Lokoja reference location
var lokoja = ee.Geometry.Point([6.74, 7.80]);

// 2. Load HydroBASINS Level 6
var basins = ee.FeatureCollection(
  'WWF/HydroSHEDS/v1/Basins/hybas_6'
);

// 3. Select the five previously identified basins
var basinIDs = [
  1060909890,
  1060909900,
  1060892990,
  1060893000,
  1060022420
];

// 4. Define distinct colours
var basinColours = [
  'E63946',  // Red
  '277DA1',  // Blue
  '43AA8B',  // Green
  'F9C74F',  // Yellow
  '9B5DE5'   // Purple
];

// 5. Clear the previous map layers
Map.layers().reset([]);

// 6. Set map extent
Map.centerObject(lokoja, 8);

// 7. Display each basin independently
basinIDs.forEach(function(id, index) {

  var basin = basins.filter(
    ee.Filter.eq('HYBAS_ID', id)
  );

  var styledBasin = basin.style({
    color: basinColours[index],
    fillColor: '00000000',
    width: 3
  });

  Map.addLayer(
    styledBasin,
    {},
    'Basin ' + id
  );

  print(
    'Basin ' + id,
    basin.first()
  );

});

// 8. Display Lokoja reference point
Map.addLayer(
  lokoja,
  {color: 'FFFFFF', pointSize: 9},
  'Lokoja reference point'
);

// 9. Print basin summary
var nearbyBasins = basins.filterBounds(
  lokoja.buffer(50000)
);

print('Nearby basin count:', nearbyBasins.size());

print(
  'Selected basin IDs:',
  basinIDs
);

print(
  'Selected basin upstream areas:',
  basinIDs.map(function(id) {
    var feature = basins.filter(
      ee.Filter.eq('HYBAS_ID', id)
    ).first();

    return ee.Feature(feature).get('UP_AREA');
  })
);

