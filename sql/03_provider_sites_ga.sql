-- This joins each site to its map coordinates and builds a GEOGRAPHY point,
-- which is BigQuery's map data type. Sites that did not geocode keep an
-- empty (NULL) location instead of being thrown away, so the checks can
-- count them honestly.
CREATE OR REPLACE TABLE `eye-screening-gap-510222.eye_screening.provider_sites_ga` AS
WITH joined AS (
  SELECT
    s.site_id, s.street, s.city, s.zip5,
    s.n_providers, s.has_ophthalmology, s.has_optometry,
    g.match_status, g.match_type,
    -- The coordinates arrive as one piece of text like "-84.39,33.75".
    -- SPLIT cuts it at the comma. Longitude is first, latitude is second.
    SAFE_CAST(SPLIT(g.coordinates, ',')[SAFE_OFFSET(0)] AS FLOAT64) AS longitude,
    SAFE_CAST(SPLIT(g.coordinates, ',')[SAFE_OFFSET(1)] AS FLOAT64) AS latitude
  FROM `eye-screening-gap-510222.eye_screening.provider_sites_raw` AS s
  LEFT JOIN `eye-screening-gap-510222.eye_screening.geocode_results_raw` AS g
    USING (site_id)
)
SELECT
  *,
  IF(longitude IS NOT NULL AND latitude IS NOT NULL,
     ST_GEOGPOINT(longitude, latitude),   -- longitude FIRST, then latitude
     NULL) AS location
FROM joined;
