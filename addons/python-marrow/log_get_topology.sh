#!/bin/bash

dmesg -C
#python test.py 55 apply_tunnel_route:tun1/pp1:10.123.0.5:33:10.123.0.31:44:
python test.py 55 get_topology:
sleep 0.05
dmesg > dmesg1.log &
sleep 0.1
dmesg > dmesg2.log &
sleep 0.2
dmesg > dmesg3.log &