#!/bin/bash
dmesg -C

python test.py 55 apply_tunnel_route:oftun1/ofpp1:14721744407806083072:17:14721744407968612352:15:
dmesg > dmesg1.log &
python test.py 55 apply_tunnel_route:oftun2/ofpp2:14721744407968612352:15:14721744407806083072:17:
dmesg > dmesg1.log &