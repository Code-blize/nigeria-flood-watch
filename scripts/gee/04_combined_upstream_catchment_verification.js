
/************************************************************
 NIGERIA FLOOD WATCH
 TASK 3.3 — COMBINED UPSTREAM CATCHMENT VERIFICATION

 Dataset: HydroBASINS Level 6
 Existing target: 1060909890
 Additional target: 1060909900

 Purpose:
 1. Trace both upstream networks independently.
 2. Compare their basin IDs and detect overlap.
 3. Construct the combined network.
 4. Report counts and generation distributions.
 5. Export the verified combined network.
************************************************************/

var basins = ee.FeatureCollection(
  'WWF/HydroSHEDS/v1/Basins/hybas_6'
);

var targetA = 1060909890;
var targetB = 1060909900;

// -----------------------------------------------------
// FUNCTION: TRACE ONE TARGET'S UPSTREAM NETWORK
// -----------------------------------------------------

function traceCatchment(targetID, branchName) {

  var frontier = ee.List([targetID]);
  var upstream = ee.FeatureCollection([]);

  // HydroBASINS network tracing: maximum 50 generations.
  for (var level = 1; level <= 50; level++) {

    var next = basins.filter(
      ee.Filter.inList('NEXT_DOWN', frontier)
    );

    var tagged = next.map(function(feature) {
      return feature.set({
        upstream_level: level,
        branch_seed: targetID,
        branch_name: branchName,
        network_role: 'Upstream contributing basin'
      });
    });

    upstream = upstream.merge(tagged);

    frontier = next.aggregate_array('HYBAS_ID');
  }

  // Remove duplicate upstream basin IDs.
  upstream = upstream.distinct(['HYBAS_ID']);

  // Add the target basin itself.
  var target = basins
    .filter(ee.Filter.eq('HYBAS_ID', targetID))
    .map(function(feature) {
      return feature.set({
        upstream_level: 0,
        branch_seed: targetID,
        branch_name: branchName,
        network_role: 'Target basin'
      });
    });

  return upstream.merge(target);
}

// -----------------------------------------------------
// TRACE BOTH NETWORKS INDEPENDENTLY
// -----------------------------------------------------

var branchA = traceCatchment(
  targetA,
  'Target_A_1060909890'
);

var branchB = traceCatchment(
  targetB,
  'Target_B_1060909900'
);

// -----------------------------------------------------
// COMPARE NETWORK MEMBERSHIP
// -----------------------------------------------------

var idsA = ee.List(
  branchA.aggregate_array('HYBAS_ID')
).distinct();

var idsB = ee.List(
  branchB.aggregate_array('HYBAS_ID')
).distinct();


var sharedIDs = idsA.map(function(id) {
  return ee.Algorithms.If(
    idsB.contains(id),
    id,
    null
  );
}).removeAll([null]);




var onlyA = idsA.removeAll(idsB);
var onlyB = idsB.removeAll(idsA);

print('========== INDIVIDUAL NETWORKS ==========');

print('Target A total features:', branchA.size());
print('Target B total features:', branchB.size());

print('Target A unique IDs:', idsA.size());
print('Target B unique IDs:', idsB.size());

print('Shared basin IDs:', sharedIDs);
print('Shared basin count:', sharedIDs.size());

print('Only in Target A:', onlyA.size());
print('Only in Target B:', onlyB.size());

// -----------------------------------------------------
// BUILD THE COMBINED NETWORK
// -----------------------------------------------------

var combined = branchA
  .merge(branchB)
  .distinct(['HYBAS_ID']);

print('========== COMBINED NETWORK ==========');

print('Combined unique basin count:', combined.size());

print(
  'Combined generation distribution:',
  combined.aggregate_histogram('upstream_level')
);

print(
  'Combined target basin IDs:',
  combined.filter(
    ee.Filter.eq('network_role', 'Target basin')
  ).aggregate_array('HYBAS_ID')
);

// -----------------------------------------------------
// VERIFY DOWNSTREAM LINK COMPLETENESS
// -----------------------------------------------------

var combinedIDs = ee.List(
  combined.aggregate_array('HYBAS_ID')
).distinct();

var upstreamOnly = combined.filter(
  ee.Filter.eq(
    'network_role',
    'Upstream contributing basin'
  )
);


var checkedLinks = upstreamOnly.map(function(feature) {

  var downstreamID = feature.get('NEXT_DOWN');

  var linkExists = combinedIDs.contains(downstreamID);

  return feature.set(
    'link_missing',
    ee.Algorithms.If(linkExists, 0, 1)
  );

});

var brokenLinks = checkedLinks.filter(
  ee.Filter.eq('link_missing', 1)
);

print(
  'Upstream downstream links outside network:',
  brokenLinks.size()
);

print('Broken-link records:', brokenLinks);


print('Upstream downstream links outside network:',
  brokenLinks.size());

print('Broken-link records:', brokenLinks);

// -----------------------------------------------------
// EXPORT COMBINED NETWORK
// -----------------------------------------------------

Export.table.toDrive({
  collection: combined,
  description: 'NigeriaFloodWatch_Combined_HydroBASINS_Network',
  folder: 'NigeriaFloodWatch',
  fileNamePrefix: 'hydrobasins_combined_upstream_network_lokoja',
  fileFormat: 'GeoJSON'
});

// Export attributes.
Export.table.toDrive({
  collection: combined,
  description: 'NigeriaFloodWatch_Combined_HydroBASINS_Attributes',
  folder: 'NigeriaFloodWatch',
  fileNamePrefix: 'hydrobasins_combined_upstream_attributes_lokoja',
  selectors: [
    'HYBAS_ID',
    'NEXT_DOWN',
    'MAIN_BAS',
    'UP_AREA',
    'SUB_AREA',
    'PFAF_ID',
    'upstream_level',
    'branch_seed',
    'branch_name',
    'network_role'
  ],
  fileFormat: 'CSV'
});
