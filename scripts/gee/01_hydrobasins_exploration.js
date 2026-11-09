
// ======================================================
// NIGERIA FLOOD WATCH
// Step 4: HydroBASINS data exploration
// Study area: Lokoja, Kogi State, Nigeria
// ======================================================

// 1. Define approximate Lokoja location
var lokoja = ee.Geometry.Point([6.74, 7.80]);

// 2. Load HydroBASINS Level 6 directly from GEE
var basins = ee.FeatureCollection(
  'WWF/HydroSHEDS/v1/Basins/hybas_6'
);

// 3. Find basin polygons around Lokoja
var localBasins = basins.filterBounds(
  lokoja.buffer(50000)
);

// 4. Display results
Map.centerObject(lokoja, 8);

Map.addLayer(
  localBasins,
  {color: 'blue'},
  'HydroBASINS Level 6'
);

Map.addLayer(
  lokoja,
  {color: 'red'},
  'Lokoja location'
);

// 5. Inspect the dataset
print('HydroBASINS collection:', basins);
print('Local basin count:', localBasins.size());
print('Sample basin attributes:', localBasins.limit(5));

// 6. Inspect the available attribute fields
print(
  'First basin feature:',
  localBasins.first()
);


// ======================================================
// INSPECT HYDROBASINS ATTRIBUTES
// ======================================================

var firstBasin = ee.Feature(localBasins.first());

// 1. Print all available property names
print(
  'Available basin attributes:',
  firstBasin.propertyNames()
);

// 2. Print all attributes and their values
print(
  'First basin property values:',
  firstBasin.toDictionary()
);

// 3. Print the attributes of all five nearby basins
var basinDetails = localBasins.map(function(feature) {
  return ee.Feature(null, feature.toDictionary());
});

print(
  'All five nearby basin records:',
  basinDetails
);

// 4. Inspect important hydrological identifiers
print('HYBAS_ID values:', localBasins.aggregate_array('HYBAS_ID'));
print('NEXT_DOWN values:', localBasins.aggregate_array('NEXT_DOWN'));
print('MAIN_BAS values:', localBasins.aggregate_array('MAIN_BAS'));
print('UP_AREA values:', localBasins.aggregate_array('UP_AREA'));


// ======================================================
// NIGERIA FLOOD WATCH
// HYDROBASINS: BASIN IDENTIFICATION
// ======================================================

var basinInspection = localBasins.map(function(feature) {

  var centroid = feature.geometry().centroid(1000);
  var coordinates = centroid.coordinates();

  return ee.Feature(null, {
    HYBAS_ID: feature.get('HYBAS_ID'),
    NEXT_DOWN: feature.get('NEXT_DOWN'),
    MAIN_BAS: feature.get('MAIN_BAS'),
    UP_AREA: feature.get('UP_AREA'),
    centroid_longitude: coordinates.get(0),
    centroid_latitude: coordinates.get(1)
  });

});

print('Lokoja nearby basin identification:', basinInspection);


// ======================================================
// HYDROBASINS: INSPECT FIVE BASIN RECORDS
// ======================================================

var basinList = localBasins.toList(5);

var basinInspection = ee.FeatureCollection(
  basinList.map(function(item) {

    var feature = ee.Feature(item);

    var centroid = feature.geometry().centroid(1000);
    var coordinates = centroid.coordinates();

    return feature.set({
      centroid_longitude: coordinates.get(0),
      centroid_latitude: coordinates.get(1)
    });

  })
);

// Print the actual records
print('Basin 1:', basinInspection.first());

print('HYBAS_ID:', basinInspection.aggregate_array('HYBAS_ID'));

print('NEXT_DOWN:', basinInspection.aggregate_array('NEXT_DOWN'));

print('MAIN_BAS:', basinInspection.aggregate_array('MAIN_BAS'));

print('UP_AREA:', basinInspection.aggregate_array('UP_AREA'));

print('Longitude:', basinInspection.aggregate_array('centroid_longitude'));

print('Latitude:', basinInspection.aggregate_array('centroid_latitude'));



/********************************************************
 NIGERIA FLOOD WATCH
 Step 4E: Visualise nearby HydroBASINS
********************************************************/

// Approximate Lokoja location
var lokoja = ee.Geometry.Point([6.74, 7.80]);

// Give each basin a distinct colour
var basinStyles = ee.FeatureCollection(
  localBasins.map(function(feature) {
    var id = ee.Number(feature.get('HYBAS_ID'));

    var colour = ee.String(
      ee.Algorithms.If(
        id.eq(1060909890), 'red',
        ee.Algorithms.If(
          id.eq(1060909900), 'blue',
          ee.Algorithms.If(
            id.eq(1060892990), 'green',
            ee.Algorithms.If(
              id.eq(1060893000), 'orange',
              'purple'
            )
          )
        )
      )
    );

    return feature.set('style', {
      color: colour,
      fillColor: colour.cat('22'),
      width: 2
    });
  })
);

// Display basins
Map.centerObject(lokoja, 8);

Map.addLayer(
  basinStyles.style({styleProperty: 'style'}),
  {},
  'Five HydroBASINS Level 6 polygons'
);

// Display Lokoja
Map.addLayer(
  lokoja,
  {color: 'yellow'},
  'Lokoja reference point'
);

// Print individual basin attributes
print('Basin 1060909890:',
  localBasins.filter(ee.Filter.eq('HYBAS_ID', 1060909890)).first());

print('Basin 1060909900:',
  localBasins.filter(ee.Filter.eq('HYBAS_ID', 1060909900)).first());

print('Basin 1060022420:',
  localBasins.filter(ee.Filter.eq('HYBAS_ID', 1060022420)).first());
