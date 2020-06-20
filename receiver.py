# Receiver (laptop) script for the ECA

from datetime import datetime
from random import randrange
import encryption
import network


def authenticate(encryptor):
    # Generate a random index between 0 and 100
    index = random(0, 101)

    # Encrypt the index
    encrypted_index = encryptor.encrypt(str(index))

    # Send the encrypted index to the Watchman

    # Wait for a value

    # Decrypt the value
    decrypted_index = encryptor.decrypt(encrypted_index)

    return encrypted_data == decrypted_data


# Initialisation - when the UAV is on the ground
# Create the encryptor
current_time = datetime.now().isoformat()
encryptor = encryption.Encryption(time=current_time)

# Set up communication
watchman = network.Network()

# Send the keys to the Watchman
keys = encryptor.export_keys()

# Main loop

# while 1:
#     if !authenticate(encryptor):
#         break

# Send an intrusion detection alert
