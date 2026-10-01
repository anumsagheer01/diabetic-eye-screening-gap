SELECT
  (SELECT COUNT(*) FROM `eye-screening-gap-510222.eye_screening.tracts_ga`) AS tracts_with_map_shapes,
  (SELECT COUNT(*) FROM `eye-screening-gap-510222.eye_screening.places_diabetes_ga`) AS tracts_in_cdc_file,
  (SELECT COUNT(*)
     FROM `eye-screening-gap-510222.eye_screening.tracts_ga` AS t
     JOIN `eye-screening-gap-510222.eye_screening.places_diabetes_ga` AS p
       USING (tract_id)) AS tracts_that_match,
  (SELECT COUNTIF(tract_geom IS NULL)
     FROM `eye-screening-gap-510222.eye_screening.tracts_ga`) AS shapes_missing;
