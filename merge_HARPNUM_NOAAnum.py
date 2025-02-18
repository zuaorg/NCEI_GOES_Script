import pandas as pd

# Load the SHARP data from Excel
sharp_data = pd.read_excel("data/SHARP_data.xlsx")

# Clean the 'timestamp' column to remove any unwanted spaces and characters
sharp_data['T_REC'] = sharp_data['T_REC'].str.replace('_', ' ').str.replace('TAI', '').str.strip()

# Assuming the column containing the timestamp is called 'T_REC'
sharp_data['T_REC'] = pd.to_datetime(sharp_data['T_REC'].str.replace('_', ' ').str.replace('TAI', ''), format='%Y.%m.%d %H:%M:%S')

# Load NOAA TXT file, ensuring proper column separation
noaa_df = pd.read_csv("data/all_harps_with_noaa_ars.txt", sep=r"\s+", skiprows=1, header=None, names=["HARPNUM", "NOAA_ARS"])

# Merge data based on the SHARP identifier
merged_df = sharp_data.merge(noaa_df, on="HARPNUM", how="left")

# Display the merged dataset
print(merged_df.head())

# Save merged data if needed
merged_df.to_csv("results/merged_HARPNUM_NOAAnum.csv", index=False)
