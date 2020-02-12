#!/bin/zsh

# Summary: Compact VirtualBox virtual disk
#
# Usage: vbox_compact <Virtual disk>

vdisk=$1

if [ -z "$vdisk" ]; then
    echo "vbox_compact <Virtual disk>"
else
    VBoxManage modifymedium disk $vdisk --compact
fi
