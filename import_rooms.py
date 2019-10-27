import pandas as pd
import logging
import requests
import json

logging.basicConfig(filename="logs.log", level=logging.INFO)
# truncating log files before new run
open("logs.log", "w").close()

excel = pd.read_excel("rooms_list.xlsx")

session = requests.Session()
url_locations = "https://127.0.1.1/rooms/api/admin/locations"
url_rooms = "https://127.0.1.1/rooms/api/admin/rooms/"

# verify=False because local build so no 
# SSL cert was needed but requests throws
# an exception
try:
    response = session.get(url_locations, verify=False)
except requests.RequestException as e:
    logging.error(e)
    

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
        "room_name_format":"{building}/{floor}-{room}",
        "name": building_number
    }
    
    try:
        response = session.post(url_locations, headers=headers, cookies=cookies, data=data, verify=False)
        logging.info(f"Building {building_number} created")
    except requests.RequestException as e:
        logging.error(e)
    
# fetching information of all available locations from
# the API, mainly location_id, to create a room specific
# to that location only
try:
    response = session.get(url_locations, headers=headers, cookies=cookies, verify=False)
    logging.info("Location information fetched")
except requests.RequestException as e:
    logging.error(e)
    
location_data = json.loads(response.text)

# iterating through each location available
# in the API to create rooms specific to the 
# location_id of that location
for location in location_data:

    location_id = location["id"]
    building = location["name"]
    
    # iterating through each room 
    for index, row in excel.iterrows():
        
        # if the location name (building) from the API
        # is the same building of the room in the 
        # excel sheet, then the room is created
        if(str(row["BUILDING_NUMBER"]) == building):
            
            # TODO: search for room owner 
            
            # initializing payload with room attributes,
            # owner is a required field by indico's room creation
            # API. Manually set to a user for now
            data = {
                "building": building,
                "location_id": location_id,
                "owner": "User:2",  
                "floor": row["FLOOR"],
                "number": row["BUILDING_NUMBER"],
                "latitude": row["LATITUDE"],
                "longitude": row["LONGITUDE"],
                "capacity": row["CAPACITY"]
            }
            try:
                response = session.post(url_rooms, headers=headers, cookies=cookies, data=data, verify=False)
                logging.info(f"Adding [{data}]")
            except requests.RequestException as e:
                logging.error(e)

