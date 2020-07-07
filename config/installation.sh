#!/bin/sh

# Install packages
PACKAGES="nmap openssh-server"
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install $PACKAGES -y

# Setup git and the eca repo
ssh-keyscan github.com >> /home/dan/.ssh/known_hosts
git clone git@github.com:DanSpicyTaco/watchman.git watchman

# Install the requirements
cd watchman
pip3 install -e .

# Enable the wait for network service
# This will wait until the network is connected 
# before starting the sender service every bootup
sudo cp config/network-wait-online.service /etc/systemd/system/network-wait-online.service
sudo systemctl enable network-wait-online.service

# Enable the sender service
sudo cp config/sender.service /etc/systemd/system/sender.service
sudo systemctl enable sender.service

# Enable the UAV service
sudo cp config/sender.service /etc/systemd/system/uav.service
sudo systemctl enable uav.service

