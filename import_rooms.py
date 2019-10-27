import pandas as pd
import requests
import json

excel = pd.read_excel("rooms_list.xlsx")

session = requests.Session()
url = "https://127.0.1.1/rooms/api/admin/locations"

# verify=False because local build so no 
# SSL cert was needed but requests throws
# an exception
response = session.get(url, verify=False)

# using Indico's API requires the X-CSRF-Token
# and the indico_session cookie to go through.
# Acquiring these headers requires a user to be
# logged in to Indico
headers = {
    "X-CSRF-Token": "ec862943-e561-4315-9e3d-3088076c0092"
}

cookies = {
    "indico_session": "a025c2c6-fba0-49d8-93b2-7dbe01f0ac4c"
}


# creating locations if not already created using 
# the BUILDING_NUMBER column from the excel sheet
for index, row in excel.iterrows():
    
    building_number = row["BUILDING_NUMBER"]
    # room_name_format is a required field to 
    # make a new location
    data = {
        "room_name_format":"{building}/{floor}-{number}",
        "name": building_number
    }
    
    response = session.post(url, headers=headers, cookies=cookies, data=data, verify=False)
    
# fetching information of all available locations from
# the API, mainly location_id, to create a room specific
# to that location only
response = session.get(url, headers=headers, cookies=cookies, verify=False)
location_data = json.loads(response.text)
