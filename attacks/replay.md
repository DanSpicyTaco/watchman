# Replay Attack

Replay attacks involve recording encrypted uplink commands, then resending the commands to the UAV.
This will allow the attacker to control the UAV using certain messages - the contents of the message do not have to be unencrypted, as the UAV will do that.

## Attack

1. Record uplink commands using aireplay and export it as a `.cpap` file
2. Resend the same commands using `tcpreplay`.
