# Deauthentication Attack

Management frames, as outlined in 802.11 standards, are special messages used for communication between access points (e.g. routers) and stations (e.g. laptops/phones).
One type of management frame is a **deauthentication** frame, which is sent from the router to a station.
When the station receives the deauthentication frame, it automatically disconnects from the router.
It is possible to create a fake deauthentication frame and send it to a station.
As management frames are usually unencrypted, the station will think it is a legitmate message and disconnect from the router.
A deauthentication attack involves flooding the network with lots of fake deauthentication messages, such that the target station is unable to connect back to the router.
This effectively causes a denial of service.

<pre align="center">
   <img src="img/deauth_diagram.png">
</pre>

## Attack

1. Ensure `airodrump-ng <NETWORK INTERFACE> --bssid <NETWORK BSSID> -c <NETWORK CHANNEL>` is running on one terminal.
2. Open a new terminal and run the deauthentication attack: `aireplay-ng --deauth 0 -c <STATION MAC ADDR> -a <NETWORK BSSID> <NETWORK INTERFACE>`.

   <pre align="center">
      <img src="img/deauth_attack.png">
   </pre>

## Fixing the issue

Move to the 802.11w protocol - one that uses authenticated management frames.
