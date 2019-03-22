#!/bin/bash

set -e

# Wait for internet connection before anything else
dhcpcd --waitip


# Initialise pacman
pacman-key --init
pacman-key --populate archlinuxarm


# Install required packages
pacman -Syu --noconfirm base-devel polkit xorg python python-pip xorg-xinit mpv vim xdotool xf86-video-fbdev
pip install rpi.GPIO


# Enable the required services
mv /etc/systemd/system/getty@tty1.service.d/override.conf.bak /etc/systemd/system/getty@tty1.service.d/override.conf
systemctl daemon-reload
systemctl enable zoomer.service


# Installation complete, this service can be disabled.
systemctl disable installer.service
reboot