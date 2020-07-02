from lib import encryption, network
import time
import subprocess

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
# Set up communication

laptop = network.Server((addr, port))

# Receive the keys from the GCS
# Expecting two 16 byte messages
key = laptop.receive(16)
IV = laptop.receive(16)

# Create the encryptor
encryptor = encryption.Encryption(key=key, IV=IV)

# Send success message to laptop
laptop.send(b'Watchman initialised')

# Main Loop
while True:
    received_index = laptop.receive(16)

    # print(received_index)

    decrypted_index = encryptor.decrypt(received_index)
    encrypted_index = encryptor.encrypt(decrypted_index)
    laptop.send(encrypted_index)

    time.sleep(1)

# Pack up
laptop.close()
