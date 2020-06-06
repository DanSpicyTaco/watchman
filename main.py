from datetime import datetime
import encryption
import network

network.Network()
encryption.Encryption(datetime.now().isoformat())
