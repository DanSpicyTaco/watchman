import curses
# import cv2
# import pickle
import queue
# import struct
import subprocess
import threading
from lib import network


class Screen:
    def __init__(self):
        # Initialise
        # cv2.namedWindow("DOWNLINK")

        # Initialise curses screen
        self._screen = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.cbreak()  # Don't wait for newline
        curses.noecho()  # Don't echo the input char
        curses.curs_set(0)  # Invisible cursor
        self._screen.keypad(1)  # Accept arrow keys as inputs

        # Create uplink and downlink windows
        self._uplink = curses.newwin(5, 40, 7, 2)
        self._downlink = curses.newwin(10, 50, 6, 60)

        # Draw everything
        self.instructions()
        self.uplink()
        self.downlink()

    def __enter__(self):
        return self

    ##
    # Getter
    ##
    def getch(self):
        return self._screen.getch()

    ##
    # Draw functions
    ##
    def instructions(self):
        self._screen.addstr(0, 2, "UAV CONTROLLER", curses.color_pair(3))
        self._screen.addstr(1, 2, "INFORMATION", curses.color_pair(2))
        self._screen.addstr(2, 2, "Arrow keys: move the UAV around",
                            curses.color_pair(2))
        self._screen.addstr(3, 2, "'a', 's': change the altitude",
                            curses.color_pair(2))
        self._screen.addstr(4, 2, "'q': quit the program",
                            curses.color_pair(2))
        self._screen.refresh()

    def uplink(self):
        # Altitude
        self._uplink.addstr(0, 0, "ALTITUDE", curses.color_pair(3))
        self._uplink.addstr(2, 3, "^")
        self._uplink.addstr(3, 3, "v")

        # Control pad
        self._uplink.addstr(0, 25, "CONTROL PAD", curses.color_pair(3))
        self._uplink.addstr(2, 30, "^")
        self._uplink.addstr(3, 30, "O", curses.color_pair(1))
        self._uplink.addstr(4, 30, "v")
        self._uplink.addstr(3, 29, "<")
        self._uplink.addstr(3, 31, ">")
        self._uplink.refresh()

    def downlink(self):
        self._downlink.addstr(1, 1, "DOWNLINK", curses.color_pair(3))
        self._downlink.border(0)
        self._downlink.refresh()

    ##
    # Uplink and Downlink
    ##
    def move_joystick(self, key):
        self.uplink()

        if key == curses.KEY_UP:
            self._uplink.addstr(2, 30, "O", curses.color_pair(1))
            self._uplink.addstr(3, 30, "|")
        elif key == curses.KEY_DOWN:
            self._uplink.addstr(4, 30, "O", curses.color_pair(1))
            self._uplink.addstr(3, 30, "|")
        elif key == curses.KEY_LEFT:
            self._uplink.addstr(3, 29, "O", curses.color_pair(1))
            self._uplink.addstr(3, 30, "-")
        elif key == curses.KEY_RIGHT:
            self._uplink.addstr(3, 31, "O", curses.color_pair(1))
            self._uplink.addstr(3, 30, "-")
        elif key == ord('a'):
            self._uplink.addstr(2, 3, "^", curses.color_pair(1))
        elif key == ord('s'):
            self._uplink.addstr(3, 3, "v", curses.color_pair(1))

        self._uplink.refresh()

    def video(self, uav, msgs):
        # payload_size = struct.calcsize("=L")
        counter = 1
        while True:
            # Attempt to get a new item from the messages queue
            try:
                item = msgs.get(False)
            except queue.Empty:
                item = None

            if item == "q":
                msgs.task_done()
                break

            # Make sure the counter is within the box dimensions
            if counter >= 8:
                counter = 2
            else:
                counter += 1

            # # Get the next frame's length
            # data = uav.receive(payload_size)
            # packed_msg_size = data[:payload_size]
            # data = data[payload_size:]
            # msg_size = struct.unpack("=L", packed_msg_size)[0]

            # # Get the next frame
            # data += uav.receive(msg_size)
            # frame_data = data[:msg_size]
            # data = data[msg_size:]

            # # # Extract it
            # frame = pickle.loads(frame_data)

            # # Display it
            # cv2.imshow('DOWNLINK', frame)
            # cv2.waitKey(25)

            # Add the length to the downlink box
            data = uav.receive(20)
            self._downlink.addstr(counter, 1, data.decode())
            self._downlink.refresh()

    def __exit__(self, exc_type, exc_value, traceback):
        curses.endwin()
        # cv2.destroyWindow("DOWNLINK")


def send_key(uav, key):
    valid_keys = [
        curses.KEY_UP,
        curses.KEY_DOWN,
        curses.KEY_LEFT,
        curses.KEY_RIGHT,
        ord('a'),
        ord('s')
    ]

    if key in valid_keys:
        key_bytes = key.to_bytes(2, byteorder="big")
        uav.send(key_bytes)


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

# Set up communication
uav = network.Client((addr, port))

with Screen() as screen:
    # Create thread for receiving downlink
    msgs = queue.Queue()
    downlink = threading.Thread(target=screen.video, args=(uav, msgs))
    downlink.start()

    # Send the key to the uav
    key = ''
    while key != ord('q'):
        key = screen.getch()
        screen.move_joystick(key)
        send_key(uav, key)

    # Wait for the downlink thread to close
    msgs.put("q")
    msgs.join()
