# Vector Processing Log --- NigeriaFloodWatch

## Purpose

Document the preparation and validation of vector layers for the Lokoja,
Kogi State study area. Preserve source data unchanged and keep processed
outputs separate.

## Study-area boundary

-   **Study area:** Lokoja, Kogi State, Nigeria
-   **AOI:** The project's confirmed study-area boundary
-   **AOI geometry and extent:** Checked and confirmed by the project
    owner
-   **Use:** The confirmed AOI was used to clip the vector layers.

## Data preservation and output locations

-   **Raw/source files:** Preserve unchanged in the project's raw-data
    location.
-   **Processed vector outputs:** Store separately from raw files.
-   **Raw-data folder:** `[record actual folder path]`
-   **Processed-output folder:** `[record actual folder path]`
-   **Project:** `NigeriaFloodWatch`

Do not overwrite or delete source files when updating processed outputs.

## Processing record

  --------------------------------------------------------------------------------
  Input / source layer    Processing performed    Output layer
  ----------------------- ----------------------- --------------------------------
  Roads                   Clipped to the          `roads_lokoja_clip`
                          confirmed AOI           

  Settlements             Clipped to the          `settlements_lokoja_clip`
                          confirmed AOI           

  Hydrography polygons    Clipped to the          `hydrography_area_lokoja_clip`
                          confirmed AOI           

  Clipped roads           Projected to WGS 1984   `roads_utm32n`
                          UTM Zone 32N            

  Clipped settlements     Projected to WGS 1984   `settlements_utm32n`
                          UTM Zone 32N            

  Clipped hydrography     Projected to WGS 1984   `hydrography_area_utm32n`
  polygons                UTM Zone 32N            
  --------------------------------------------------------------------------------

The source attributes were inspected. Potentially useful attributes were
retained; no attribute fields were deleted or renamed during this check.
System geometry fields were retained.

## Validation

The project owner reports that the outputs were checked and confirmed
for:

-   Coordinate reference system (CRS)
-   Geometry
-   Feature counts
-   Spatial extent
-   Whether features fall within the AOI

The validation checks were reported as accurate. Record any future
corrections or reruns below rather than silently replacing this record.

## Processing notes

-   A mistaken extra row was added during attribute-table inspection. It
    was identified as accidental; it is not treated as a valid feature
    or processing result.
-   Attribute inspection did not identify a supported reason to delete
    or change fields.
-   The clipped outputs and their UTM 32N copies are retained as
    separate layers.

## Reproducibility details to complete

Fill these in from the project files or geoprocessing history when
available:

-   Processing date: `[YYYY-MM-DD]`
-   ArcGIS Pro version: `[version]`
-   Exact source filenames and paths: `[record paths]`
-   Exact output folder path: `[record path]`
-   Geoprocessing tool names and parameters: `[record from history]`
-   Final feature counts by layer: `[record verified counts]`
-   AOI boundary layer name: `[record exact layer name]`

## Change log

  -----------------------------------------------------------------------
  Date                                Change
  ----------------------------------- -----------------------------------
  `[YYYY-MM-DD]`                      Initial vector processing and
                                      validation log prepared.

  -----------------------------------------------------------------------
