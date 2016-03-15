from easysnmp import Session, EasySNMPTimeoutError
from datetime import datetime
import sqlite3


def os_detect(raw, vendor):
    if vendor == "Cisco":
        temp1 = raw[0].value.split('(', 1)
        temp2 = temp1[1].split(')')
        temp3 = raw[0].value.split(',')
        temp4 = temp3[2]
        os = "Cisco IOS " + temp4[9:] + " (" + temp2[0] + ")"
        return os
    if vendor == "Juniper":
        temp1 = raw[0].value.split('kernel')
        temp2 = temp1[1].split(',')
        os = str(temp2[0]).lstrip()
        return os


def device_polling(device, comm):
    session = Session(hostname=str(device), community=str(comm), version=2)

    descr = session.walk('SNMPv2-MIB::sysDescr')

    sysname = session.walk('SNMPv2-MIB::sysName')
    location = session.walk('SNMPv2-MIB::sysLocation')
    uptime = session.walk('SNMPv2-MIB::sysUpTime')

    if descr[0].value.startswith("Cisco"):
        icon = "Cisco"
        os = os_detect(descr, 'Cisco')

        hardware = session.get('1.3.6.1.2.1.47.1.1.1.1.13.1')
        if str(hardware.value) == 'NOSUCHINSTANCE':
            hardware = session.get('1.3.6.1.2.1.47.1.1.1.1.13.1001')

        serial = session.get('1.3.6.1.2.1.47.1.1.1.1.11.1')
        if str(serial.value) == 'NOSUCHINSTANCE':
            serial = session.get('1.3.6.1.2.1.47.1.1.1.1.11.1001')

    if descr[0].value.startswith("Juniper"):
        icon = "Juniper"
        os = os_detect(descr, 'Juniper')
        hardware = session.get('1.3.6.1.4.1.2636.3.1.2.0')
        serial = session.get('1.3.6.1.4.1.2636.3.1.3.0')

    return sysname[0].value, location[0].value, uptime[0].value, hardware.value, serial.value, os, icon

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
cursor.execute("SELECT id, ip, community FROM devices_device")
data = cursor.fetchall()
for row in data:
    cur = datetime.now()
    try:
        result = device_polling(row[1], row[2])
        cursor.execute(
            "UPDATE devices_device SET sysname=?, \
            location=?, uptime=?, hardware=?, serial=?, \
            os=?, icon=?, status=1, last_polled=?, last_updated=?\
            WHERE ID=?", (result[0], result[1], result[2],
                          result[3], result[4], result[5],
                          result[6], cur, cur, row[0]))
        conn.commit()
        print("Device " + row[1] + " polled")
    except EasySNMPTimeoutError:
        cursor.execute(
            "UPDATE devices_device SET status=0, last_polled=? \
            WHERE ID=?", (cur, row[0]))
        conn.commit()
        print("Device " + row[1] + " down")
conn.close()
