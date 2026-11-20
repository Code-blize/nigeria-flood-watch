// --------------------------------------------------
// 6B. MONTHLY AGGREGATION VERIFICATION
// --------------------------------------------------

// Sum of the 30 daily AOI-mean rainfall values.
var dailyMeanTotal = dailyRainfall.aggregate_sum(
  'rainfall_mean_mm_day'
);

// Mean of the monthly accumulated raster
// over the exact same AOI and at the same scale.
var monthlyAOIMean = monthlyRainfall.reduceRegion({
  reducer: ee.Reducer.mean(),
  geometry: sampleAOI,
  scale: 5566,
  maxPixels: 1e8,
  bestEffort: true
});

var monthlyMeanValue = monthlyAOIMean.get(
  'monthly_precipitation_mm'
);

// Compare the two results.
var difference = ee.Number(monthlyMeanValue)
  .subtract(ee.Number(dailyMeanTotal));

print('========== CHIRPS AGGREGATION QA ==========');

print('Number of daily records:', chirps.size());

print('Sum of daily AOI-mean rainfall (mm):',
  dailyMeanTotal);

print('Monthly raster AOI-mean rainfall (mm):',
  monthlyMeanValue);

print('Difference (mm):', difference);

print('Monthly raster AOI statistics:', monthlyAOIMean);