import pandas as pd

# Load merged SHARP and NOAA data
sharp_noaa_df = pd.read_csv("results/merged_HARPNUM_NOAAnum.csv")

# --- Step 1: Expand NOAA_ARS values ---
sharp_noaa_expanded = sharp_noaa_df.assign(NOAA_ARS=sharp_noaa_df["NOAA_ARS"].str.split(",")).explode("NOAA_ARS")

# Ensure NOAA_ARS is a string for merging
sharp_noaa_expanded["NOAA_ARS"] = sharp_noaa_expanded["NOAA_ARS"].str.strip()

# Load merged DONKI flare data
flare_df = pd.read_csv("results/flare_data_with_CME_SEP.csv", on_bad_lines="skip")

# --- Step 2: Pivot Flare Data to Separate CME and SEP Columns ---
flare_pivoted = flare_df.pivot_table(
    index=["activeRegionNum"],
    columns="linkedEventType",
    values=["linkedEventTime", "flareClass"],
    aggfunc="first"
).reset_index()

# Flatten MultiIndex columns
flare_pivoted.columns = ["activeRegionNum", "CME_Time", "SEP_Time", "CME_Class", "SEP_Class"]

# --- Step 3: Merge SHARP/NOAA with Pivoted Flare Data ---
merged_df = sharp_noaa_expanded.merge(
    flare_pivoted,
    left_on="NOAA_ARS",
    right_on="activeRegionNum",
    how="left"
).drop(columns=["activeRegionNum"])  # Drop duplicate column after merge

# --- Step 3: Merge SHARP/NOAA with GOES (Flare Data) ---
merged_df = sharp_noaa_expanded.merge(
    flare_df[["activeRegionNum", "flareClass", "linkedEventTime", "linkedEventType"]],
    left_on=["NOAA_ARS"],
    right_on=["activeRegionNum"],
    how="left"
)

print(merged_df)