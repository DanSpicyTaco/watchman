import encryption
import network
import time
import argparse

# Command Line Arguments setup
parser = argparse.ArgumentParser(
    description='Watchman script for the ECA.')
parser.add_argument('addr', metavar='IP', type=str,
                    help='The IP address of the Watchman.')
parser.add_argument('port', metavar='P', type=int,
                    help='The port of the Watchman.')

# Get the port and IP of the sender (watchman)
args = parser.parse_args()
addr = args.addr
port = args.port

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
