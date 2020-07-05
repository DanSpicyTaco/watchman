# Send video stream
# Receive flight commands

import time
import subprocess
from lib import network


# NAME = "raspberrypi.hub"

# # Get the IP address of this machine
# output = subprocess.check_output(
#     "nmap -sn 192.168.1.0/24 -oG - 192.168.1", shell=True)
# hosts = output.decode().split("\n")[1:-1]

# for host in hosts:
#     info = host.split(" ")
#     name = info[2].split("\t")[0][1:-1]

#     if name == NAME:
#         addr = info[1]
#         port = 3030
#         break

# gcs = network.Server((addr, port))
gcs = network.Server(('127.0.0.1', 3001))

data = b''
while data.decode() != "exit":
    data = gcs.receive(20)
    print(data.decode())
