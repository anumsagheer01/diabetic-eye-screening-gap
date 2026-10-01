-- A first spatial join. ST_WITHIN asks "is this point inside this shape?"
-- If an address was placed correctly, its point lands inside a Georgia tract.
SELECT COUNT(DISTINCT s.site_id) AS sites_inside_a_georgia_tract
FROM `eye-screening-gap-510222.eye_screening.provider_sites_ga` AS s
JOIN `eye-screening-gap-510222.eye_screening.tracts_ga` AS t
  ON ST_WITHIN(s.location, t.tract_geom)
WHERE s.location IS NOT NULL;
