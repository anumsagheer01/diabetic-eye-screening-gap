-- This turns the loaded text into real map data. ST_GEOGFROMTEXT reads a
-- shape written as text and makes a GEOGRAPHY value. SAFE. in front means
-- "if one shape is broken, give NULL instead of failing the whole job."
-- ST_GEOGPOINT makes a point. Remember: longitude FIRST, then latitude.
-- This replaces the earlier version that used Google's older tract map.
CREATE OR REPLACE TABLE `eye-screening-gap-510222.eye_screening.tracts_ga` AS
SELECT
  tract_id,
  tract_name,
  county_fips,
  land_area_m2,
  ST_GEOGPOINT(center_lon, center_lat) AS center_point,
  SAFE.ST_GEOGFROMTEXT(wkt) AS tract_geom
FROM `eye-screening-gap-510222.eye_screening.tracts_2020_raw`;
