import pandas as pd
import os

# Define column names based on the new structure
columns = [
    "DataStationCode", "Date", "UnconfirmedChange", "StartTime", "EndTime", "MaxTime",
    "LatitudeHemisphere", "Latitude", "LongitudeHemisphere", "LongitudeCMD",
    "SXIData", "FlareClass", "FlareIntensity", "StationAbbreviation", "IntegratedFlux",
    "SunspotRegionNumber", "CMPDate", "RegionArea", "TotalIntensity"
]

# Define column widths
# Adjusted to reflect combined columns and appropriate lengths
widths = [
    5,   # DataStationCode: 2 (DataCode) + 3 (StationCode)
    6,   # Date: Year (2) + Month (2) + Day (2)
    2,   # UnconfirmedChange
    4,   # StartTime
    4,   # EndTime
    4,   # MaxTime
    1,   # LatitudeHemisphere
    2,   # Latitude
    1,   # LongitudeHemisphere
    2,   # LongitudeCMD
    3,   # SXIData
    1,   # FlareClass
    2,   # FlareIntensity
    4,   # StationAbbreviation
    7,   # IntegratedFlux
    5,   # SunspotRegionNumber
    8,   # CMPDate: Year (2) + Month (2) + Day (4)
    7,   # RegionArea
    7    # TotalIntensity
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
        df = pd.read_fwf(file_path, widths=widths, names=columns, dtype=str, skiprows=1)

        # Ensure combined date columns retain only the required values
        df["Date"] = df["Date"].str[:6]  # Ensure proper format for Date
        df["CMPDate"] = df["CMPDate"].str[:6]  # Ensure proper format for CMPDate

        dataframes.append(df)
        print(f"Processed file for year {year}")
    else:
        print(f"File not found for year {year}")

# Concatenate all DataFrames
merged_df = pd.concat(dataframes, ignore_index=True)

# Show all columns
with pd.option_context('display.max_columns', None):
    print(merged_df.head())

# Save the merged DataFrame to a CSV for future use
merged_df.to_csv("test_merged_goes_data_2010_2016.csv", index=False)

print("Data merging complete. Saved to 'test_merged_goes_data_2010_2016.csv'.")