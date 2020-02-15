#!/bin/zsh
#
# Script to upgrade and clean Archlinux VM.
# Run under root.

# Upgrade
pacman -Syu --noconfirm

# Clear cache
pacman -Sc --noconfirm

# Delete all the logs from /var/log 
find /var/log -type f -delete

# Clear history
rm /home/dkav/.histfile
history -c && history -w && exit
