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

# --- Step 3: Merge SHARP/NOAA with GOES (Flare Data) ---
merged_df = sharp_noaa_expanded.merge(
    goes_df[["NOAASunspotRegionNumber", "FlareClass"]],
    left_on="NOAA_ARS",
    right_on="NOAASunspotRegionNumber",
    how="inner",
    indicator=False
)


# Drop duplicate NOAA column after merging
merged_df.drop(columns=["NOAASunspotRegionNumber"], inplace=True)
print("merged_df", merged_df.head())

# --- Step 4: Aggregate back (Combine Multiple Flare Classes) ---
# final_df = merged_df.groupby(merged_df.index).agg({
#     **{col: "first" for col in sharp_noaa_df.columns if col != "NOAA_ARS"},  # Keep original SHARP data
#     "NOAA_ARS": lambda x: ",".join(x.dropna().unique()),  # Keep NOAA_ARS as a single string
#     "FlareClass": lambda x: ",".join(x.dropna().unique()) if x.notna().any() else "None"  # Combine flare classes, fill missing
# }).reset_index(drop=True)

# Display results
#print(final_df.head())
#print(final_df.count())

filtered_df = merged_df[merged_df["FlareClass"] != "None"]
print(filtered_df)

# Save the updated dataset
filtered_df.to_csv("results/merged_SHARP_goes_flare_data.csv", index=False)
