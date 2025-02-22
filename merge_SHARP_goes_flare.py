import pandas as pd

# Load merged SHARP and NOAA data
sharp_noaa_df = pd.read_csv("results/merged_HARPNUM_NOAAnum.csv")

# Load merged GOES data (flare data)
goes_df = pd.read_csv("results/filtered_goes_flare_data.csv")


# --- Step 1: Convert NOAA columns to strings (prevent merging issues) ---
sharp_noaa_df["NOAA_ARS"] = sharp_noaa_df["NOAA_ARS"].astype(str).str.strip()
goes_df["NOAASunspotRegionNumber"] = goes_df["NOAASunspotRegionNumber"].astype(str).str.strip().str.replace('.0', '')


# --- Step 2: Expand NOAA_ARS values ---
sharp_noaa_expanded = sharp_noaa_df.assign(NOAA_ARS=sharp_noaa_df["NOAA_ARS"].str.split(",")).explode("NOAA_ARS")

# Ensure NOAA_ARS is a string for merging
sharp_noaa_expanded["NOAA_ARS"] = sharp_noaa_expanded["NOAA_ARS"].str.strip()

# # Step 3: Convert to datetime for time-based filtering
# sharp_noaa_expanded["T_REC"] = pd.to_datetime(sharp_noaa_df["T_REC"])
# goes_df["DateTime"] = pd.to_datetime(goes_df["DateTime"])
#
# # Perform a cross join by creating a key column
# sharp_noaa_expanded["key"] = 1
# goes_df["key"] = 1
# cross_joined_df = sharp_noaa_expanded.merge(goes_df, on="key").drop(columns=["key"])
# print(cross_joined_df.count())
#
# # Step 2: Filter rows where DateTime is within 12 hours after T_REC
# time_filtered_df = cross_joined_df[
#     (cross_joined_df["DateTime"] >= cross_joined_df["T_REC"]) &
#     (cross_joined_df["DateTime"] <= cross_joined_df["T_REC"] + pd.Timedelta(hours=24))
# ]
# print(time_filtered_df.count())



# --- Step 3: Merge SHARP/NOAA with GOES (Flare Data) ---
merged_df = sharp_noaa_expanded.merge(
    goes_df[["NOAASunspotRegionNumber", "FlareClass", "DateTime"]],
    left_on=["NOAA_ARS"],
    right_on=["NOAASunspotRegionNumber"],
    how="left"
)

# Inspect columns right after merging
#print(merged_df.columns)

# Drop duplicate NOAA column after merging
merged_df.drop(columns=["NOAASunspotRegionNumber"], inplace=True)
#print("merged_df", merged_df.head())

# # Step 3: Convert to datetime for time-based filtering
# merged_df["T_REC"] = pd.to_datetime(merged_df["T_REC"])
# merged_df["DateTime"] = pd.to_datetime(merged_df["DateTime"])
#
filtered_df = merged_df[
    ~(merged_df["DateTime"] < merged_df["T_REC"])
]

# filtered_df = filtered_df[merged_df["FlareClass"] != "None"]
print(filtered_df.count())

# Display the result
with pd.option_context('display.max_columns', None):
    print(filtered_df.head())

# Save the updated dataset
filtered_df.to_csv("results/merged_SHARP_goes_flare_data.csv", index=False)
