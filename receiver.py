from datetime import datetime
from random import randrange
import encryption
import network
import time
import argparse

# Command Line Arguments setup
parser = argparse.ArgumentParser(
    description='GCS (laptop) script for the ECA. Run sender.py on the Watchman before this.')
parser.add_argument('addr', metavar='IP', type=str,
                    help='The IP address of the Watchman.')
parser.add_argument('port', metavar='P', type=int,
                    help='The port of the Watchman.')

# Get the port and IP of the sender (watchman)
args = parser.parse_args()
addr = args.addr
port = args.port

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
        # TODO Send an intrusion detection alert
        break
    else:
        print('.', flush=True, end=" ")

    time.sleep(1)

# Pack up everything
watchman.close()
