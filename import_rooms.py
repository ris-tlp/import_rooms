import pandas as pd
import requests
import json

excel = pd.read_excel("rooms_list.xlsx")

session = requests.Session()
url = "https://127.0.1.1/rooms/api/admin/locations"

# verify=False because local build 
# so no SSL cert was needed but requests throws
# an exception
response = session.get(url, verify=False)

# using Indico's API requires the X-CSRF-Token and
# the indico_session cookie to go through.
# Acquiring these headers requires a user to be logged
# in to Indico
headers = {
    "X-CSRF-Token": ""
}

cookies = {
    "indico_session": ""
}


# creating locations if not already created
for index, row in excel.iterrows():
    
    building_number = row["BUILDING_NUMBER"]
    data = {
        "room_name_format":"{building}/{floor}-{number}",
        "name": building_number
    }
    
    response = session.post(url, headers=headers, cookies=cookies, data=data, verify=False)
