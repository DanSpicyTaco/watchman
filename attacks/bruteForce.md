# Brute Force Attack

Brute-force attacks are generally the slowest and most simple way to gain access into a secured software system.
It involves recording a TCP connection handshake (specifically the initialisation vectors - IVs), then guessing the pre-shared key that was involved to encrypt the messages.
Guesses can be narrowed down by using a "dictionary" - a list of popular or leaked passwords.
The dictionary used was the [BIG-WPA-LIST-1](https://www.mediafire.com/file/m7tjhgfd61lfeu4/BIG-WPA-LIST-1.rar/file), which contains popular passwords for access points.
Once the key is known, the attacker could connect to the UAV and send it spoofed uplink control commands.
Fortunately, brute-force attacks are easy to prevent if a strong password is used.

For the purposes of this experiment, a brute-force attack will be considered successful if the key can be guessed within 5mins.
Furthermore, it is assumed that packet recording begins before the UAV and GCS connect to each other.

## Attack

1. Start recording IVs using `airodump-ng -c <NETWORK CHANNEL> --bssid <STATION MAC ADDR> -w <PATH TO STORE IVS> <NETOWORK INTERFACE>`
2. Once the TCP handshake has been recorded, you will get a confirmation message.
3. Attempt to brute-force the password within 5min using `aircrack-ng -w <PATH TO DICTIONARY> -b <STATION MAC ADDR> <PATH TO STORE IVS>`
4. If 5min have passed, the attack failed.
