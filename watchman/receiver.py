from datetime import datetime
from random import randrange
import time
import subprocess
import os
from lib import encryption, network

NAME = "raspberrypi.hub"

# Get the IP address of this machine
output = subprocess.check_output(
    "nmap -sn 192.168.1.0/24 -oG - 192.168.1", shell=True)
hosts = output.decode().split("\n")[1:-1]

for host in hosts:
    info = host.split(" ")
    name = info[2].split("\t")[0][1:-1]

    if name == NAME:
        addr = info[1]
        port = 3000
        break

# Initialisation - when the UAV is on the ground

# Create the encryptor
current_time = datetime.now().isoformat()
encryptor = encryption.Encryption(time=current_time)

# Set up communication
watchman = network.Client((addr, port))

# Send the keys to the Watchman
keys = encryptor.export_keys()
watchman.send(keys["key"])
watchman.send(keys["IV"])

# Print confirmation message
data = watchman.receive(20)
print(data.decode())

# Start Snort
os.chdir('../snort')
snort = subprocess.Popen(['sh', 'snort.sh'], stdout=subprocess.PIPE)

# Main loop
while True:
    # Generate a random index between 0 and 100
    index = randrange(0, 101)

    # Encrypt the index
    encrypted_index = encryptor.encrypt(str(index))

    # Send the encrypted index to the Watchman
    watchman.send(encrypted_index)

    # Wait for a value
    received_index = watchman.receive(16)

    # Decrypt the value
    decrypted_index = encryptor.decrypt(received_index)

    if int(index) != int(decrypted_index):
        print("\nWatchman communication channel has been tampered")
        break
    else:
        print('.', flush=True, end=" ")

    # An intrusion was found - break
    if snort.poll() is not None:
        print(f"\nIntrusion detected:\n{snort.stdout.readline().decode()}")
        watchman.send(b'Channel attacked')
        break

    time.sleep(1)

# Pack up everything
watchman.close()
