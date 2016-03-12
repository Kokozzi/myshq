import json
import sqlite3
from datetime import datetime


conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

with open("new_json.json") as json_file:
    json_data = json.load(json_file)

for sw in json_data["Switches"]:
    cursor.execute("SELECT ip, ip_conn, port, \
                   hw_address, date_start_conn, \
                   time_start_conn, company, device_type, \
                   protocol_vers, serial, config, \
                   status, curr_features, advert_features, \
                   supp_features, peer_features \
                   FROM devices_sdn_device WHERE hostname=?",
                   (sw["name"],))
    row = cursor.fetchone()

    if row is not None:
        print(row[0])
    else:
        print("No data")

print(datetime.now())
conn.close()
