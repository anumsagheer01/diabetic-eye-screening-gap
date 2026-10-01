-- This builds a tidy table with one row per Georgia census tract.
-- CrudePrev is the plain percent of adults with diagnosed diabetes, with
-- no age adjustment. Later parts multiply it by the number of adults to
-- estimate how many patients live in each area.
CREATE OR REPLACE TABLE `eye-screening-gap-510222.eye_screening.places_diabetes_ga` AS
SELECT
  CAST(TractFIPS AS STRING) AS tract_id,        -- the 11 digit tract code, kept as text
  CAST(CountyFIPS AS STRING) AS county_id,      -- the 5 digit county code, kept as text
  DIABETES_CrudePrev AS diabetes_pct,           -- percent of adults with diabetes
  TotalPop18plus AS adults,                     -- adults living in the tract
  ROUND(TotalPop18plus * DIABETES_CrudePrev / 100) AS est_adults_with_diabetes,
  DIABETES_Crude95CI AS diabetes_range_text     -- margin of error, kept as text for now
FROM `eye-screening-gap-510222.eye_screening.places_raw`
WHERE StateAbbr = 'GA';                         -- keeps only Georgia
