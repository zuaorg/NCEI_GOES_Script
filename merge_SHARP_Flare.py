import pandas as pd

# Load merged SHARP and NOAA data
sharp_noaa_df = pd.read_csv("merged_sharp_noaa.csv")
print("SHARP NOAA Columns:", sharp_noaa_df.columns)

# Load merged GOES data (flare data)
goes_df = pd.read_csv("merged_goes_data_2010_2016.csv")
print("GOES Columns:", goes_df.columns)

# --- Step 1: Convert NOAA columns to strings (prevent merging issues) ---
sharp_noaa_df["NOAA_ARS"] = sharp_noaa_df["NOAA_ARS"].astype(str).str.strip()
goes_df["NOAASunspotRegionNumber"] = goes_df["NOAASunspotRegionNumber"].astype(str).str.strip()

# --- Step 2: Expand NOAA_ARS values ---
sharp_noaa_expanded = sharp_noaa_df.assign(NOAA_ARS=sharp_noaa_df["NOAA_ARS"].str.split(",")).explode("NOAA_ARS")

# Ensure NOAA_ARS is a string for merging
sharp_noaa_expanded["NOAA_ARS"] = sharp_noaa_expanded["NOAA_ARS"].str.strip()

# --- Step 3: Merge SHARP/NOAA with GOES (Flare Data) ---
merged_df = sharp_noaa_expanded.merge(
    goes_df[["NOAASunspotRegionNumber", "FlareClass"]],
    left_on="NOAA_ARS",
    right_on="NOAASunspotRegionNumber",
    how="left"
)

# Drop duplicate NOAA column after merging
merged_df.drop(columns=["NOAASunspotRegionNumber"], inplace=True)

# --- Step 4: Aggregate back (Combine Multiple Flare Classes) ---
final_df = merged_df.groupby(merged_df.index).agg({
    **{col: "first" for col in sharp_noaa_df.columns if col != "NOAA_ARS"},  # Keep original SHARP data
    "NOAA_ARS": lambda x: ",".join(x.dropna().unique()),  # Keep NOAA_ARS as a single string
    "FlareClass": lambda x: ",".join(x.dropna().unique()) if x.notna().any() else "None"  # Combine flare classes, fill missing
}).reset_index(drop=True)

# Display results
#print(final_df.head())
#print(final_df.count())

filtered_df = final_df[final_df["FlareClass"] == "None"]
print(filtered_df)

# Save the updated dataset
final_df.to_csv("sharp_flares.csv", index=False)
