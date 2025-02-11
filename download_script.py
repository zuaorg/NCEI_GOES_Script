import os
import requests

# Create a directory for the downloaded data if it doesn't exist
os.makedirs("data", exist_ok=True)

# Base URL for the GOES X-ray flare data
base_url = "https://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-features/solar-flares/x-rays/goes/xrs/goes-xrs-report_{}.txt"

# Loop through the years from 2010 to 2017
for year in range(2010, 2018):  # Range is inclusive of 2010 and exclusive of 2018
    url = base_url.format(year)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Send the request
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        file_path = f"data/goes_xrs_report_{year}.txt"
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"File for {year} downloaded successfully: {file_path}")
    else:
        print(f"Failed to download data for {year}. HTTP Status Code: {response.status_code}")