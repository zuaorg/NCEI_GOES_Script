import pandas as pd

# Load merged SHARP and NOAA data
sharp_noaa_df = pd.read_csv("results/merged_HARPNUM_NOAAnum.csv")

# --- Step 1: Expand NOAA_ARS values ---
sharp_noaa_expanded = sharp_noaa_df.assign(NOAA_ARS=sharp_noaa_df["NOAA_ARS"].str.split(",")).explode("NOAA_ARS")

# Ensure NOAA_ARS is a string for merging
sharp_noaa_expanded["NOAA_ARS"] = sharp_noaa_expanded["NOAA_ARS"].str.strip()

# Step 2: Load merged DONKI flare data
flare_df = pd.read_csv("results/flare_data_with_CME_SEP.csv", on_bad_lines="skip")

# Filter rows where linkedEventType is 'CME'
cme_df = flare_df[flare_df["linkedEventType"] == "CME"].copy()
# Rename the column linkedEventType to linkedCME
cme_df = cme_df.rename(columns={"flrID": "flrIDCme", "linkedEventType": "linkedCME", "linkedEventTime": "linkedCMETime"})
print("CME count:", cme_df.shape[0])  # shape[0] gives the row count


# Filter rows where linkedEventType is 'SEP'
sep_df = flare_df[flare_df["linkedEventType"] == "SEP"].copy()
# Rename the column linkedEventType to linkedSEP
sep_df = sep_df.rename(columns={"flrID": "flrIDSep", "linkedEventType": "linkedSEP", "linkedEventTime": "linkedSEPTime"})
print("SEP count:", sep_df.shape[0])  # shape[0] gives the row count

print(flare_df.columns)
print(cme_df.columns)
print(sep_df.columns)


# --- Step 3: Merge SHARP/NOAA with DONKI (Flare, CME, SEP Data) ---
merged_df = sharp_noaa_expanded.merge(
    flare_df[["activeRegionNum", "flrID", "flareClass"]],
    left_on=["NOAA_ARS"],
    right_on=["activeRegionNum"],
    how="left"
).drop(columns="activeRegionNum")

merged_df = merged_df.merge(
    cme_df[["activeRegionNum", "flrIDCme", "linkedCMETime", "linkedCME"]],
    left_on=["NOAA_ARS", "flrID"],
    right_on=["activeRegionNum", "flrIDCme"],
    how="left"
).drop(columns=["activeRegionNum", "flrIDCme"])

merged_df = merged_df.merge(
    sep_df[["activeRegionNum", "flrIDSep", "linkedSEPTime", "linkedSEP"]],
    left_on=["NOAA_ARS", "flrID"],
    right_on=["activeRegionNum", "flrIDSep"],
    how="left"
).drop(columns=["activeRegionNum", "flrIDSep"])

# Convert columns to datetime format
merged_df["linkedSEPTime"] = pd.to_datetime(merged_df["linkedSEPTime"])
merged_df["linkedCMETime"] = pd.to_datetime(merged_df["linkedCMETime"])
merged_df["T_REC"] = pd.to_datetime(merged_df["T_REC"])

# Apply the filter: Keep rows where either linkedSEPTime or linkedCMETime is within 48 hours after T_REC
filtered_df = merged_df[
    (
        ((merged_df["linkedSEPTime"] - merged_df["T_REC"]).between(pd.Timedelta(0), pd.Timedelta(hours=48))) |
        ((merged_df["linkedCMETime"] - merged_df["T_REC"]).between(pd.Timedelta(0), pd.Timedelta(hours=48)))
    ) |
    (
        merged_df["linkedSEP"].isna() & merged_df["linkedCME"].isna()
    ) |
    (
        merged_df["flrID"].isna()
    )
]

print(filtered_df.columns)

print("count:", filtered_df.shape[0])

filtered_df.to_csv("results/final_SHARP_CME_SEP.csv")