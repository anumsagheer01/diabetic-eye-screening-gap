# This script turns the Census Bureau's map file for Georgia's 2020 tracts
# into a CSV file that BigQuery can load. Each row is one tract: its code,
# its name, and its shape written out as text.

# csv helps write CSV files. os helps with file paths.
import csv
import os

# shapefile (from the pyshp tool) reads the map file.
import shapefile
# shapely turns a shape into WKT, which is the shape written as plain text,
# like POLYGON ((-84.1 33.7, -84.2 33.8, ...)). BigQuery can read that.
from shapely.geometry import shape
from shapely import wkt

# The ~ shortcut does not work inside Python, so expanduser turns it into
# the real path of my home folder.
folder = os.path.expanduser("~/eye-project/data/")

# Open the map file. A "reader" is something that goes through the file
# one piece at a time.
reader = shapefile.Reader(folder + "tl_2020_13_tract/tl_2020_13_tract.shp")

# The first entry in the field list is a technical flag, not a real column,
# so [1:] skips it. Then [0] takes just the name of each field.
field_names = [f[0] for f in reader.fields[1:]]

out_path = folder + "tracts_2020_ga.csv"
count = 0

# "w" means write. newline="" stops blank lines from sneaking into the CSV.
with open(out_path, "w", newline="") as f:
    writer = csv.writer(f)

    # The first row is the column names.
    writer.writerow(["tract_id", "tract_name", "county_fips",
                     "land_area_m2", "center_lat", "center_lon", "wkt"])

    # Go through every tract. Each one has a shape and a record of facts.
    for sr in reader.iterShapeRecords():
        # zip pairs each field name with its value, and dict makes a lookup
        # table, so row["GEOID"] gives the tract's 11 digit code.
        row = dict(zip(field_names, sr.record))

        # Turn the shape into a shapely object, then into text.
        # rounding_precision=6 keeps 6 decimal places, which is about
        # 10 centimeters. That is plenty, and it keeps the file small.
        geom = shape(sr.shape.__geo_interface__)
        shape_text = wkt.dumps(geom, trim=True, rounding_precision=6)

        writer.writerow([
            row["GEOID"],                       # the 11 digit tract code
            row["NAMELSAD"],                    # a readable name like "Census Tract 12.01"
            row["STATEFP"] + row["COUNTYFP"],   # the 5 digit county code
            int(row["ALAND"]),                  # land area in square meters
            float(row["INTPTLAT"]),             # a point near the middle: latitude
            float(row["INTPTLON"]),             # and longitude
            shape_text,
        ])
        count += 1

print("Wrote", count, "tracts to", out_path)
