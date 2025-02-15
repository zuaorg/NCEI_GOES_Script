import pandas as pd

# Load SHARP XLSX file
sharp_df = pd.read_excel("data/SHARP_data.xlsx")
print("SHARP Columns:", sharp_df.columns)

# Load NOAA TXT file, ensuring proper column separation
noaa_df = pd.read_csv("data/all_harps_with_noaa_ars.txt", sep=r"\s+", skiprows=1, header=None, names=["HARPNUM", "NOAA_ARS"])
print("NOAA Columns:", noaa_df.columns)
print(noaa_df.head())

# Merge data based on the SHARP identifier
merged_df = sharp_df.merge(noaa_df, on="HARPNUM", how="left")

# Display the merged dataset
print(merged_df.head())

# Save merged data if needed
merged_df.to_csv("merged_sharp_noaa.csv", index=False)
