# This makes a histogram (a bar chart of counts) showing how diabetes rates
# vary across Georgia census tracts. It shows at a glance that need is not
# the same everywhere.

import sys
import pandas as pd
# matplotlib is the drawing toolbox. "Agg" tells it to draw into a picture
# file, since Cloud Shell has no screen to draw on.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# The first word after the script name is the CSV file to read.
data = pd.read_csv(sys.argv[1])
values = data["diabetes_pct"].dropna()    # dropna removes empty rows

fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(values, bins=30, color="#3b6ea8", edgecolor="white")

# A dashed red line at the average, with a label next to it.
average = values.mean()
ax.axvline(average, color="#c0392b", linestyle="--", linewidth=2)
ax.text(average, ax.get_ylim()[1] * 0.95, f"  average {average:.1f}%",
        color="#c0392b", va="top")

ax.set_title("How common diagnosed diabetes is across Georgia census tracts")
ax.set_xlabel("Adults with diagnosed diabetes (%), CDC estimate")
ax.set_ylabel("Number of census tracts")
fig.tight_layout()
fig.savefig(sys.argv[2], dpi=200)         # the second word is the picture file to save
print("Saved", sys.argv[2])
