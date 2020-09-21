# import cv2
# import pickle
import queue
# import struct
import subprocess
import threading
from lib import network


def video_stream(gcs, msgs):
    # webcam = cv2.VideoCapture(0)

    # Send "video stream" (random 6 bit string) to UAV
    while True:
        # Attempt to get a new item from the messages queue
        try:
            item = msgs.get(False)
        except queue.Empty:
            item = None

        if item == "q":
            msgs.task_done()
            # webcam.release()
            break

        # # Get the next video frame
        # ret, frame = webcam.read()

        # # Serialize it and get the length
        # data = pickle.dumps(frame)
        # message_size = struct.pack("=L", len(data))

        # # Send message_size & data
        # gcs.send(message_size + data)


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
        port = 3030
        break

gcs = network.Server((addr, port))

# Message queue for inter-thread communication
msgs = queue.Queue()

# Setup the downlink (video stream) thread
downlink = threading.Thread(target=video_stream, args=(gcs, msgs))
downlink.start()

DATA_TO_COMMAND = {
    '260': 'l',
    '261': 'r',
    '259': 'f',
    '258': 'b',
    '97': 'u',
    '115': 'd',
    '0': 's'
}

# Log all uplink commands to eca.log
with open('/home/dan/watchman/log/eca.log', 'w') as logfile:
    data = ''
    while data != "0":
        byte_data = gcs.receive(20)
        data = str(int.from_bytes(byte_data, byteorder="big"))
        logfile.write(f'{DATA_TO_COMMAND[data]}')
        # logfile.write(f'{data} ')

# Allow the downlink thread to quit
msgs.put("q")
msgs.join()
