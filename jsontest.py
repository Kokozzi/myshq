import json
import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

with open("new_json.json") as json_file:
    json_data = json.load(json_file)

for sw in json_data["Switches"]:
    cursor.execute("SELECT hostname, ip, ip_conn, port, \
                    hw_address, date_start_conn, time_start_conn, \
                    company, device_type, protocol_vers, serial, config, \
                    status, curr_features, advert_features, \
                    supp_features, peer_features FROM devices_sdn_device \
                    WHERE hostname=?", sw["name"])
    row = cursor.fetchone()

    if sw["state"] == 'up':
        status = 1
    elif sw["state"] == 'down':
        status = 0

    if row is not None:
        cursor.execute("UPDATE devices_sdn_device SET ip=?, \
                        ip_conn=?, port=?, hw_address=?, date_start_conn=? \
                        time_start_conn=?, company=?, device_type=?, \
                        protocol_vers=?, serial=?, config=?, status=?, \
                        curr_features=?, advert_features=?, supp_features=?, \
                        peer_features=? WHERE hostname=?\
                        ", (sw["IpAddress"], sw["IpAddressConn"],
                            sw["portNumber"], sw["hardwareAddress"],
                            sw["DateStartConn"], sw["TimeStartConn"],
                            sw["CompanyName"], sw["TypeOfSwitch"],
                            sw["ProtocolVersion"], sw["SN"],
                            sw["config"], status, sw["currentFeatures"],
                            sw["advertisedFeatures"], sw["supportedFeatures"],
                            sw["peerFeatures"], sw["name"]))
    else:
        ins = (sw["name"], sw["IpAddress"], sw["IpAddressConn"],
               sw["portNumber"], sw["hardwareAddress"], sw["DateStartConn"],
               sw["TimeStartConn"], sw["CompanyName"], sw["TypeOfSwitch"],
               sw["ProtocolVersion"], sw["SN"], sw["config"],
               status, sw["currentFeatures"], sw["advertisedFeatures"],
               sw["supportedFeatures"], sw["peerFeatures"])
        cursor.execute("INSERT INTO devices_sdn_device (hostname,  ip, \
                        ip_conn, port, hw_address, date_start_conn,\
                        time_start_conn, company, device_type, \
                        protocol_vers, serial, config, \
                        status, curr_features, advert_features, \
                        supp_features, peer_features) \
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                        ?, ?, ?, ?, ?)", ins)
    conn.commit()

conn.close()
