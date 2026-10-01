# This script reads the giant national list of health care providers and
# keeps only the eye doctors in Georgia who are still active. It drops names
# completely, because the project only needs where eye care is, not who is
# there.

# sys lets the script read the words typed after its name in the terminal.
import sys
# zipfile lets Python read inside a zip file without unpacking all of it.
import zipfile
# pandas is a toolbox for working with tables, like Excel but in code.
import pandas as pd

# sys.argv is the list of words typed after the script name.
# Number 0 is the script's own name, so my first real input is number 1.
zip_path = sys.argv[1]     # the downloaded zip file
out_folder = sys.argv[2]   # the folder where the results get saved

# Specialty codes start with these letters. Ophthalmology starts with 207W
# and optometry starts with 152W. Checking only the start also catches
# sub-specialties, like retina doctors.
OPHTHALMOLOGY_PREFIX = "207W"
OPTOMETRY_PREFIX = "152W"

with zipfile.ZipFile(zip_path) as z:
    # namelist() lists every file inside the zip. The main data file starts
    # with npidata_pfile. There is also a small file with just the column
    # names, which gets skipped.
    candidates = [
        n for n in z.namelist()
        if n.lower().startswith("npidata_pfile")
        and n.lower().endswith(".csv")
        and "fileheader" not in n.lower()
    ]
    if not candidates:
        print("I could not find the main data file. These files are inside:")
        print(z.namelist())
        sys.exit(1)
    data_name = candidates[0]
    print("Reading:", data_name)

    # The file has hundreds of columns. nrows=0 reads only the column names.
    with z.open(data_name) as f:
        header = list(pd.read_csv(f, nrows=0).columns)

    # Column names are long and could change a little between months, so
    # this finds them by keywords instead of typing them out exactly.
    def find_cols(*words):
        return [c for c in header if all(w.lower() in c.lower() for w in words)]

    # A provider can list up to 15 specialties, each in its own column.
    taxonomy_cols = find_cols("taxonomy code")
    address_cols = find_cols("business practice location address")
    street_col = [c for c in address_cols if "first line" in c.lower()][0]
    city_col = [c for c in address_cols if "city" in c.lower()][0]
    state_col = [c for c in address_cols if "state" in c.lower()][0]
    zip_col = [c for c in address_cols if "postal" in c.lower()][0]

    # NEW: the file now includes providers who were deactivated, meaning
    # they retired, closed, or stopped being active. These two columns hold
    # the dates, so I can tell who is still active.
    deact_cols = find_cols("deactivation date")
    react_cols = find_cols("reactivation date")
    deact_col = deact_cols[0] if deact_cols else None
    react_col = react_cols[0] if react_cols else None

    # Print what was found, so I can check it looks right.
    print("Street column:", street_col)
    print("City column:", city_col)
    print("State column:", state_col)
    print("Zip column:", zip_col)
    print("Number of specialty columns:", len(taxonomy_cols))
    print("Deactivation date column:", deact_col)
    print("Reactivation date column:", react_col)

    # Only these columns get read. Skipping the rest saves a lot of memory.
    keep = [street_col, city_col, state_col, zip_col] + taxonomy_cols
    if deact_col:
        keep.append(deact_col)
    if react_col:
        keep.append(react_col)

    pieces = []                # a list that collects the Georgia eye care rows
    rows_seen = 0              # a counter for how many rows were read in total
    eye_rows_before = 0        # Georgia eye care rows, before removing inactive ones
    deactivated_removed = 0    # how many of those were deactivated

    # The file has millions of rows, so it is read in chunks of 200,000
    # rows at a time. That keeps memory use small.
    with z.open(data_name) as f:
        for chunk in pd.read_csv(f, usecols=keep, dtype=str, chunksize=200000):
            rows_seen += len(chunk)

            # Keep only rows where the practice state is Georgia.
            chunk = chunk[chunk[state_col] == "GA"]
            if chunk.empty:
                continue

            # Fill empty specialty cells with blank text so the text checks
            # below do not break on missing values.
            tax = chunk[taxonomy_cols].fillna("")

            # For each row, check whether ANY of its specialty columns
            # starts with the ophthalmology code, or the optometry code.
            chunk["has_ophthalmology"] = tax.apply(
                lambda col: col.str.startswith(OPHTHALMOLOGY_PREFIX)
            ).any(axis=1).astype(int)
            chunk["has_optometry"] = tax.apply(
                lambda col: col.str.startswith(OPTOMETRY_PREFIX)
            ).any(axis=1).astype(int)

            # Keep rows that are at least one of the two kinds of eye doctor.
            chunk = chunk[(chunk["has_ophthalmology"] == 1) | (chunk["has_optometry"] == 1)]
            eye_rows_before += len(chunk)

            # NEW: drop deactivated providers. A row counts as deactivated if
            # it has a deactivation date and no reactivation date on or after
            # it. to_datetime turns the text dates into real dates, and
            # errors="coerce" turns blank or odd values into "not a date".
            if deact_col and len(chunk) > 0:
                dd = pd.to_datetime(chunk[deact_col], format="%m/%d/%Y", errors="coerce")
                if react_col:
                    rd = pd.to_datetime(chunk[react_col], format="%m/%d/%Y", errors="coerce")
                else:
                    rd = pd.Series(pd.NaT, index=chunk.index)
                is_deactivated = dd.notna() & (rd.isna() | (rd < dd))
                deactivated_removed += int(is_deactivated.sum())
                chunk = chunk[~is_deactivated]

            pieces.append(chunk[[street_col, city_col, zip_col, "has_ophthalmology", "has_optometry"]])

print("Rows read from the national file:", rows_seen)
if not pieces:
    print("No Georgia eye care rows found. Something is off with the column names.")
    sys.exit(1)

print("Georgia eye care rows before removing deactivated:", eye_rows_before)
print("Deactivated rows removed:", deactivated_removed)

eye = pd.concat(pieces, ignore_index=True)
print("Georgia eye care provider rows kept:", len(eye))

# Clean up the address text so the same address typed two ways still matches.
eye["street"] = eye[street_col].str.upper().str.strip()
eye["city"] = eye[city_col].str.upper().str.strip()
eye["zip5"] = eye[zip_col].str[:5]      # some zips have 9 digits, 5 is enough
eye["state"] = "GA"
eye = eye.dropna(subset=["street", "city", "zip5"])

# Several doctors often work at one address, and a clinic is one place a
# patient can go, not several. So this groups rows by address into one row
# per site. The "one" column is just a 1 on every row, so adding it up
# counts the rows.
eye["one"] = 1
sites = (
    eye.groupby(["street", "city", "state", "zip5"], as_index=False)
       .agg(n_providers=("one", "sum"),
            has_ophthalmology=("has_ophthalmology", "max"),
            has_optometry=("has_optometry", "max"))
)

# Give every site an ID number so map coordinates can be matched back later.
sites.insert(0, "site_id", range(1, len(sites) + 1))
print("Unique sites after combining same addresses:", len(sites))

# One file with everything, for loading into BigQuery.
sites.to_csv(out_folder + "/sites_ga.csv", index=False)

# One file in the exact shape the Census address tool wants in the next
# mini part: five columns, no header row.
sites[["site_id", "street", "city", "state", "zip5"]].to_csv(
    out_folder + "/geocoder_input.csv", index=False, header=False
)
print("Done. Files saved in", out_folder)
