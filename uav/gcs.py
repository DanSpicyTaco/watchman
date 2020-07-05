# Send flight commands to the pi
# Receive video stream

import curses
import time
import subprocess
from lib import network


class Screen:
    def __init__(self):
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
    # Movement
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

    def __exit__(self, exc_type, exc_value, traceback):
        curses.endwin()


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
        uav.send(bytes(key))


# NAME = "raspberrypi.hub"

# # Get the IP address of this machine
# output = subprocess.check_output(
#     "nmap -sn 192.168.1.0/24 -oG - 192.168.1", shell=True)
# hosts = output.decode().split("\n")[1:-1]

# for host in hosts:
#     info = host.split(" ")
#     name = info[2].split("\t")[0][1:-1]

#     if name == NAME:
#         addr = info[1]
#         port = 3030
#         break

# Set up communication
# uav = network.Client((addr, port))
uav = network.Client(('127.0.0.1', 3001))

with Screen() as screen:
    # TODO Create thread for receiving downlink

    # Send the key to the uav
    key = ''
    while key != ord('q'):
        key = screen.getch()
        screen.move_joystick(key)
        send_key(uav, key)

    # Close communication
    uav.send(b"exit")
