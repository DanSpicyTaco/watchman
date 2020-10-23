# Captured POI Attack

## Attack

1. Record entire flight session using `airodump-ng -c <NETWORK CHANNEL> --bssid <STATION MAC ADDR> -w <PATH TO STORE MSGS> <NETOWORK INTERFACE>`.
2. Use `wireshark` to filter for the downlink message and check if you can get the data from them.
