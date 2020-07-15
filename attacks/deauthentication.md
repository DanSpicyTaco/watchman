# Deauthentication Attack

Management frames, as outlined in 802.11 standards, are special messages used for communication between access points (e.g. routers) and stations (e.g. laptops/phones).
One type of management frame is a **deauthentication** frame, which is sent from the router to a station.
When the station receives the deauthentication frame, it automatically disconnects from the router.
It is possible to create a fake deauthentication frame and send it to a station.
As management frames are usually unencrypted, the station will think it is a legitmate message and disconnect from the router.
A deauthentication attack involves flooding the network with lots of fake deauthentication messages, such that the target station is unable to connect back to the router.
This effectively causes a denial of service.

## Materials

- Attacker setup:
  - [Kali Linux](https://www.kali.org/downloads/)
  - ALFA network adapter
  - [aircrack-ng](https://www.aircrack-ng.org/doku.php?id=Main#download)
- Current architecture (CA):
  - [Watchman](../README.md) (`gcs.py`)
- Watchman (ECA):
  - [Watchman](../README.md) (`gcs.py` and `receiver.py`)

## Procedure

### Setting Up the Attacker

1. Connect the ALFA network adapter to the Kali computer.
   Check that the network adapter is connected by running `iwconfig`.
   Note the name of the connection.
   In this case, it is `wlan0`
   <!-- TODO: insert picutre -->
2. Kill any process that may interfere with the attacks with `aircrack-ng check kill`.
   This may include Wi-Fi processes running for the Linux OS.
   <!-- TODO: insert picutre -->
3. Put the network adapter into _monitor mode_.
   This will allow the attacker to inject (i.e. send) network packets to other stations.
   Double check the adapter is in monitor mode by running `iwconfig` again.
   <!-- TODO: insert picutre -->
4. Find the the access point (AP) of interest with `airodump-ng <NETWORK INTERFACE>`, where network interface is the equivalent of `wlan0`.
   <!-- TODO: insert picutre -->
   Press `CTRL + C` once the AP has been found.
   The AP can be identified by the ESSID column, which represents the name of the AP.
   Note down the BSSID (unique identifier) and channel of the AP.
5. Now, find the MAC address of the target station (i.e. the Raspberry Pi).
   Do this by running `airodrump-ng <NETWORK INTERFACE> --bssid <NETWORK BSSID> -c <NETWORK CHANNEL>`.
   <!-- TODO: insert picutre -->
   Note down the MAC address of the station.

### Attack

1. Ensure that the watchman and UAV are setup.
   For CA experiments, only run `gcs.py`.
   For Watchman experiments, run both `gcs.py` and `receiver.py`.
2. Start "flying" the UAV.
   <!-- TODO: insert picutre -->
3. On the attacker, ensure `airodrump-ng <NETWORK INTERFACE> --bssid <NETWORK BSSID> -c <NETWORK CHANNEL>` is running on one terminal.
   Open a new terminal and run the deauthentication attack: `aireplay-ng --deauth 0 -c <STATION MAC ADDR> -a <NETWORK BSSID> <NETWORK INTERFACE>`.
   <!-- TODO: insert picutre -->

## Results

### Current Architecture

It was expected that the CA would crash, as the connection between the GCS and UAV stopped.

### Watchman

It was expected that the Watchman would not crash, as the IDS would notify the GCS of an attempted attack.

### Simulation

<!-- TODO -->

The logfile from the attack was saved and made into a simulation.
More to come later.
