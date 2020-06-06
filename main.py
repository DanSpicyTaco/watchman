from datetime import datetime
import encryption
import network

network.Network()
current_time = datetime.now().isoformat()
encryptor = encryption.Encryption(time=current_time)
encrypted_data = encryptor.encrypt("hello")
decrypted_data = encryptor.decrypt(encrypted_data)
print(f"Encrypted: {encrypted_data}\nDecrypted: {decrypted_data}")

keys = encryptor.export_keys()

# Do this in the Pi
encryptor2 = encryption.Encryption(key=keys["key"], IV=keys["IV"])
encrypted_data = encryptor2.encrypt("hello2")
decrypted_data = encryptor2.decrypt(encrypted_data)
print(f"Encrypted2: {encrypted_data}\nDecrypted2: {decrypted_data}")
