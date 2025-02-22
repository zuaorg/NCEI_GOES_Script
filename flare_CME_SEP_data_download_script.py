import requests
import json
import csv

# Base URL for DONKI API
base_url = "https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/"


# Function to fetch data from the API
def fetch_data(endpoint, params):
    url = f"{base_url}{endpoint}"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None


# Function to save data to CSV
def save_to_csv(data, filename, fieldnames):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


# Parameters for the date range from 2010 to 2019
params = {
    'startDate': '2010-01-01',
    'endDate': '2024-12-31'
}

# Fetch CME data
cme_data = fetch_data("CME", params)

# Fetch Solar Flare data
params['catalog'] = 'M2M_CATALOG'  # Default catalog
flare_data = fetch_data("FLR", params)

# Define fieldnames for CSV files
cme_fieldnames = ['activityID', 'startTime', 'sourceLocation', 'activeRegionNum', 'instruments', 'cmeAnalyses',
                  'linkedEvents', 'note', 'catalog']
flare_fieldnames = ['flrID', 'catalog', 'instruments', 'beginTime', 'peakTime', 'endTime', 'classType',
                    'sourceLocation', 'activeRegionNum', 'note', 'submissionTime', 'versionId', 'link', 'linkedEvents']

# Save CME data to CSV if available
if cme_data:
    cme_list = []
    for cme in cme_data:
        cme_entry = {key: cme.get(key, '') for key in cme_fieldnames}
        cme_list.append(cme_entry)

    save_to_csv(cme_list, 'data/cme_data_2010_2024.csv', cme_fieldnames)
    print("CME data saved to 'data/cme_data_2010_2024.csv'")

# Save Solar Flare data to CSV if available
if flare_data:
    flare_list = []
    for flare in flare_data:
        flare_entry = {key: flare.get(key, '') for key in flare_fieldnames}
        flare_list.append(flare_entry)

    save_to_csv(flare_list, 'data/flare_CME_SEP_data_2010_2024.csv', flare_fieldnames)
    print("Solar Flare data saved to 'data/flare_CME_SEP_data_2010_2024.csv'")