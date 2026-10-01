SELECT
  COUNT(*) AS rows_in_table,
  COUNT(DISTINCT tract_id) AS distinct_tracts,     -- should equal rows_in_table
  COUNTIF(diabetes_pct IS NULL) AS missing_values,
  MIN(diabetes_pct) AS lowest_pct,
  ROUND(AVG(diabetes_pct), 1) AS average_pct,
  MAX(diabetes_pct) AS highest_pct,
  SUM(est_adults_with_diabetes) AS est_adults_with_diabetes_total
FROM `eye-screening-gap-510222.eye_screening.places_diabetes_ga`;
