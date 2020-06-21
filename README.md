# ECA

## What is this?

An implementation of part of the [Encrypted Channel Architecture](https://ieeexplore.ieee.org/document/7926571/).
Provides continuous authentication between a GCS and Watchman onboard a UAV.

## How Do I run it?

1. Run `sender.py` on the Watchman
2. Run `receiver.py` on the laptop

## Tasks

[X] Encryption
[X] Networking
[X] Authentication loop
[] Find the IP address and port of the Pi
[] Send IDS alert

## Testing

For running some basic unit tests, run:

```
python -m unittest -b
```

Append `-v` for a verbose output
