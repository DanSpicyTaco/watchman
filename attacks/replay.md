# Replay Attack

Replay attacks involve recording encrypted uplink commands, then resending the commands to the UAV.
This will allow the attacker to control the UAV using certain messages - the contents of the message do not have to be unencrypted, as the UAV will do that.

This attack is special because the IDS cannot detect replayed messages.
However, as all messages are being replayed, this will include the encrypted indexes of the watchman, serving as the detection point.

## Attack

1. Record messages using `airodump-ng -c <NETWORK CHANNEL> --bssid <STATION MAC ADDR> -w <PATH TO STORE MSGS> <NETOWORK INTERFACE>` for 5 seconds.
2. Resend the messages using `tcpreplay -i <NETWORK INTERFACE> <MSGS PATH>` - this will malform the uplink commands being received by the UAV.
