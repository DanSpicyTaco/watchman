#!/bin/sh

# Install packages
PACKAGES="nmap openssh-server"
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install $PACKAGES -y

# Setup git and the eca repo
ssh-keyscan github.com >> /home/dan/.ssh/known_hosts
git clone git@github.com:DanSpicyTaco/ECA.git eca

# Install the requirements
cd eca
pip3 install -r requirements.txt

# Enable the wait for network service
# This will wait until the network is connected 
# before starting the sender service every bootup
sudo cp network-wait-online.service /etc/systemd/system/network-wait-online.service
sudo systemctl enable network-wait-online.service

# Enable the sender service
sudo cp sender.service /etc/systemd/system/sender.service
sudo systemctl enable sender.service
sudo systemctl status sender.service
