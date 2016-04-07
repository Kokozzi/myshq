# python test.py 300 get_route:50363146:33:83917578:66:
# python test.py 300 apply_tunnel_route:Karamba:520125194:33:83917578:66:

#50363146 10.123.0.3
import socket
import sys
import struct
import pymnl
import pymnl.genl
from pymnl.attributes import Attr
from pymnl.message import Message, Payload
from pymnl.nlsocket import Socket
import json
import os
from pprint import pprint
import re
# init and bind netlink socket

def IP2Int(ip):
    o = map(int, ip.split('.'))
    res = (16777216 * o[3]) + (65536 * o[2]) + (256 * o[1]) + o[0]
    return res


def Int2IP(ipnum):
    o1 = int(ipnum / 16777216) % 256
    o2 = int(ipnum / 65536) % 256
    o3 = int(ipnum / 256) % 256
    o4 = int(ipnum) % 256
    return '%(o4)s.%(o3)s.%(o2)s.%(o1)s' % locals()

# Example
print('10.123.0.3 -> %s' % IP2Int('10.123.0.3'))
print('50363146 -> %s' % Int2IP(50363146))


sock = Socket(pymnl.NETLINK_USERSOCK)
pid = os.getpid();
data = ""
if len(sys.argv) >= 3:
    pid = int(sys.argv[1])
    data = sys.argv[2]

seq = 0

cmd = data.split(':');
print(cmd)


if cmd[0]=='get_route':
    aa=re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",cmd[1])
    if aa:
        cmd[1] = str(IP2Int(cmd[1]));
    aa=re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",cmd[3])    
    if aa:
        cmd[3] = str(IP2Int(cmd[3]));

if cmd[0]=='apply_tunnel_route':
    aa=re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",cmd[2])
    if aa:
        cmd[2] = str(IP2Int(cmd[2]));
    aa=re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",cmd[4])
    if aa:
        cmd[4] = str(IP2Int(cmd[4]));


print(cmd)
data = ":".join(cmd)
# print("Command:  ",":".join(cmd),"\n")
sock.bind(pid,seq)

print("mypid: %d\n"%pid)
print("data: %s\n"%data);

#payload=0

# if data=="get_topology":
#     payload = pack('b',1)
# if data=="feedback":
#     payload=pack('b',2)

# _payload = Payload()
# _payload.set(Command(payload))    
# init and build request message
nlmsg = Message()
nlmsg.set_type(pymnl.genl.GENL_ID_CTRL)
nlmsg.set_flags(pymnl.message.NLM_F_REQUEST|pymnl.message.NLM_F_ACK)
nlmsg.set_seq(seq)
nlmsg.set_portid(pid)

# init and build a payload
# data = {
#     'command':'test',
#     'params':{
#         'param1':1,
#         'param2':'1'
#     }
# }
#payload = json.dumps(data)
payload = str(data)
nlmsg.add_payload(payload)

#nlmsg.printf()
#print(nlmsg.get_payload().get_data())
# send message through socket
sock.send(nlmsg)

# read returned message from netlink
return_msg = sock.recv(flags=socket.MSG_DONTWAIT)
#return_msg = sock.recv()
sock.close()

# process the messages returned
for msg in return_msg:
    if (msg.get_errno()):
        # tell the user what error occurred
        print("error:", msg.get_errstr())
    else:
        #print msg.get_portid()
        print(msg.get_payload().get_data())
        # _data = json.loads(msg.get_payload().get_data())

        # if 'nodes' in _data.keys():
        #     for node in _data['nodes']:
        #         node['ip'] = socket.inet_ntoa(struct.pack('<L', node['id']))
        #         for link in node['links']:
        #             link['ip'] = socket.inet_ntoa(struct.pack('<L', link['node']))
        # if 'path' in _data.keys():
        #     r = []
        #     for hop in _data['path']:
        #         r.append(socket.inet_ntoa(struct.pack('<L', hop)))

        #     _data['ip_path'] = r

        # pprint(_data)