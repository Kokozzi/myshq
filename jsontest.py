import json
import sqlite3
from datetime import datetime

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

with open("new_json.json") as json_file:
    json_data = json.load(json_file)

for sw in json_data["Switches"]:
    cursor.execute("SELECT hostname FROM devices_sdn_device \
                    WHERE hostname=?", (sw["name"],))
    row = cursor.fetchone()

    if sw["state"] == 'up':
        status = 1
    elif sw["state"] == 'down':
        status = 0
    cur_time = datetime.now()

    json_vars = (sw["IpAddress"], sw["IpAddressConn"],
                 sw["portNumber"], sw["hardwareAddress"], sw["DateStartConn"],
                 sw["TimeStartConn"], sw["CompanyName"], sw["TypeOfSwitch"],
                 sw["ProtocolVersion"], sw["SN"], sw["config"],
                 status, sw["currentFeatures"], sw["advertisedFeatures"],
                 sw["supportedFeatures"], sw["peerFeatures"], cur_time, )

    if row is not None:
        cursor.execute("UPDATE devices_sdn_device SET ip=?, \
                        ip_conn=?, port=?, hw_address=?, date_start_conn=?, \
                        time_start_conn=?, company=?, device_type=?, \
                        protocol_vers=?, serial=?, config=?, status=?, \
                        curr_features=?, advert_features=?, supp_features=?, \
                        peer_features=?, last_polled=? WHERE hostname=? \
                        ", json_vars + (sw['name'],))
        print("Updated device: " + sw["name"])
    else:
        cursor.execute("INSERT INTO devices_sdn_device (hostname,  ip, \
                        ip_conn, port, hw_address, date_start_conn,\
                        time_start_conn, company, device_type, \
                        protocol_vers, serial, config, \
                        status, curr_features, advert_features, \
                        supp_features, peer_features, last_polled) \
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                        ?, ?, ?, ?, ?, ?)", (sw['name'],) + json_vars)
        print("Added device: " + sw["name"])
    conn.commit()

conn.close()
