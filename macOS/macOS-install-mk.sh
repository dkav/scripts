#!/bin/zsh
#
# Create a Bootable macOS High Sierra Installer.

echo "Creating a Bootable macOS High Sierra Installer"

sudo /Volumes/Mount\ Hood/Installations/Install\ macOS\ High\ Sierra.app/Contents/Resources/createinstallmedia --volume /Volumes/Untitled --applicationpath /Volumes/Mount\ Hood/Install\ macOS\ High\ Sierra.app --nointeraction
