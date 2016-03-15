import json
import sqlite3
from datetime import datetime

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

with open("new_json.json") as json_file:
    json_data = json.load(json_file)

for sw in json_data["Switches"]:
    cursor.execute("SELECT id FROM devices_sdn_device \
                    WHERE hostname=?", (sw["name"],))
    row = cursor.fetchone()
    device_id = str(row[0])

    if sw["state"] == 'up':
        status = 1
    elif sw["state"] == 'down':
        status = 0
    cur_time = datetime.now()

    device_vars = (sw["IpAddress"], sw["IpAddressConn"], sw["portNumber"],
                   sw["hardwareAddress"], sw["DateStartConn"],
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
                        peer_features=?, last_polled=? WHERE hostname=?",
                       device_vars + (sw['name'],))
        print("Updated device: " + sw["name"])
    else:
        cursor.execute("INSERT INTO devices_sdn_device (hostname,  ip, \
                        ip_conn, port, hw_address, date_start_conn,\
                        time_start_conn, company, device_type, \
                        protocol_vers, serial, config, \
                        status, curr_features, advert_features, \
                        supp_features, peer_features, last_polled) \
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                        ?, ?, ?, ?, ?, ?)", (sw['name'],) + device_vars)
        print("Added device: " + sw["name"])
    conn.commit()

    for port in sw['Ports']:
        cursor.execute("SELECT name FROM devices_sdn_port \
                        WHERE name=? AND hostname_id =?",
                       (port['name'], device_id))
        port_row = cursor.fetchone()

        if port["connection_status"] == 'up':
            status = 1
        elif port["connection_status"] == 'down':
            status = 0

        port_vars = (port['hw_addr'], status, port['TX_bytes'],
                     port['RX_bytes'], port['TX_Pkts'], port['RX_Pkts'],
                     port['Dropped'], port['Error'],)

        if port_row is not None:
            cursor.execute("UPDATE devices_sdn_port SET hw_address=?, status=?, \
                            tx_bytes=?, rx_bytes=?, tx_packets=?, \
                            rx_packets=?, dropped=?, errored=? \
                            WHERE name=? AND hostname_id=?",
                           port_vars + (port['name'], device_id))
            print("Updated port " + port['name'] + " on " +
                  sw['name'] + " device")
        else:
            cursor.execute("INSERT INTO devices_sdn_port (name, \
                            hostname_id, hw_address, status, tx_bytes, \
                            rx_bytes, tx_packets, rx_packets, \
                            dropped, errored) VALUES \
                            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (port['name'], device_id) + port_vars)
            print("Added port " + port['name'] + " on " +
                  sw['name'] + " device")
        conn.commit()

conn.close()
