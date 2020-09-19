# Network communication
# Can only support one connection
import socket


class Client:
    def __init__(self, dest_addr):
        '''
        Won't initialise until it has connected to a server.
        Server must be up and running first
        '''
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(dest_addr)

        print(f"Connected to {dest_addr}")

    def send(self, message):
        self.socket.sendall(message)
        # print(f"Sent {message}")

    def receive(self, bufsize):
        data = b''
        while len(data) < bufsize:
            packet = self.socket.recv(4096)
            if not packet:
                break
            data += packet

        return data

    def close(self):
        self.socket.close()


class Server:
    def __init__(self, my_addr):
        '''
        Won't initialise until it has accepted a client.
        Only allows for one client.
        '''
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(my_addr)
        self.socket.listen()
        self.client, addr = self.socket.accept()

        print(f"Connected to {addr}")

    def send(self, message):
        self.client.sendall(message)
        # print(f"Sent {message}")

    def receive(self, bufsize):
        data = self.client.recv(bufsize)
        return data

    def close(self):
        self.socket.close()
