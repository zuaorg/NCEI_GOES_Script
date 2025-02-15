import pandas as pd
import os

# Define column names, combining DataCode and StationCode, and combining Year, Month, and Day into a single Date column
columns = [
    "DataStationCode", "Date", "UnconfirmedChange", "StartTime", "EndTime", "MaxTime",
    "LatitudeHemisphere", "Latitude", "LongitudeHemisphere", "LongitudeCMD",
    "SXIData", "FlareClass", "FlareIntensity", "StationAbbreviation",
    "IntegratedFlux", "NOAASunspotRegionNumber", "CMPDate",
    "RegionArea", "TotalIntensity"
]

# Directory containing downloaded files
data_dir = "data"

# Initialize an empty list to hold the DataFrames
dataframes = []

# Process each file from 2010 to 2016
for year in range(2010, 2017):
    file_path = os.path.join(data_dir, f"goes_xrs_report_{year}.txt")
    if os.path.exists(file_path):
        # Read the fixed-width formatted file
        df = pd.read_fwf(file_path, widths=[
            5, 6, 2, 5, 5, 5, 1, 2, 1, 2, 25, 2, 6, 5, 8, 6, 9, 8, 7
        ], names=columns, skiprows=1, dtype=str)

        # Add to list
        dataframes.append(df)
        print(f"Processed file for year {year}")
    else:
        print(f"File not found for year {year}")

# Concatenate all DataFrames
merged_df = pd.concat(dataframes, ignore_index=True)

# Ensure all necessary columns are treated as strings
string_columns = [
    "DataStationCode", "Date", "StartTime", "EndTime", "MaxTime",
    "LatitudeHemisphere", "Latitude", "LongitudeHemisphere", "LongitudeCMD",
    "SXIData", "FlareClass", "FlareIntensity", "StationAbbreviation",
    "IntegratedFlux", "NOAASunspotRegionNumber", "CMPDate",
    "RegionArea", "TotalIntensity"
]
merged_df[string_columns] = merged_df[string_columns].astype(str)

# Show all columns
#with pd.option_context('display.max_columns', None):
 #   print(merged_df.head())

# Save the merged DataFrame to a CSV for future use
#merged_df.to_csv("merged_goes_data_2010_2016.csv", index=False)

#print("Data merging complete. Saved to 'merged_goes_data_2010_2016.csv'.")

# Keep only rows where FlareClass is "M" or "X"
filtered_df = merged_df[merged_df["FlareClass"].isin(["M", "X"])]

# Display the result
with pd.option_context('display.max_columns', None):
    print(filtered_df.head())

# Save the filtered data
filtered_df.to_csv("filtered_goes_data.csv", index=False)