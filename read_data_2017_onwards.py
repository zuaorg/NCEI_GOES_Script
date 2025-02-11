import xarray as xr
import pandas as pd

# Load the NetCDF file
file_path = "data/sci_xrsf-l2-flsum_g16_s20170209_e20250208_v2-2-0.nc"
ds = xr.open_dataset(file_path)

pd.set_option("display.max_columns", None)  # Display all columns

# Convert the dataset to a pandas DataFrame
df = ds.to_dataframe()

# Print the DataFrame
print(df)
