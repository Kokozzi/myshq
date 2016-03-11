import json
import sqlite3
from datetime import datetime


conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

with open("new_json.json") as json_file:
    json_data = json.load(json_file)

for sw in json_data["Switches"]:
    cursor.execute("SELECT hostname FROM devices_device WHERE hostname=?",
                   (sw["name"],))
    row = cursor.fetchone()

    if row is not None:
        print(row[0])
    else:
        print("No data")

print(datetime.now())
conn.close()
