SELECT
  COUNT(*) AS sites,
  COUNTIF(location IS NOT NULL) AS got_a_map_point,
  COUNTIF(location IS NULL) AS no_map_point,
  -- A rough box around Georgia. A point outside it is probably a bad match.
  COUNTIF(location IS NOT NULL
          AND NOT (longitude BETWEEN -85.7 AND -80.7
                   AND latitude BETWEEN 30.3 AND 35.1)) AS outside_georgia_box,
  -- Sites that share an exact point. Suite numbers made some addresses
  -- look different when they are the same building.
  COUNT(DISTINCT ST_ASTEXT(location)) AS distinct_points,
  SUM(has_ophthalmology) AS sites_with_ophthalmology,
  SUM(has_optometry) AS sites_with_optometry
FROM `eye-screening-gap-510222.eye_screening.provider_sites_ga`;
