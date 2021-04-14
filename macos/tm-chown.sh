#!/bin/zsh
#
# Script to change file permissions in Time Machine backup folders.
# Needs to be executed from root.

olduid=501
newuid=502

bypass=/System/Library/Extensions/TMSafetyNet.kext/Contents/Helpers/bypass

IFS=''
while read dir; do
  echo $dir
  hddir="$dir/Macintosh HD"
  find -xP $dir -user $olduid -print0 | $bypass xargs -0 chown -h $newuid
  $bypass mv "$hddir/.DocumentRevisions-V100/PerUID/$olduid" "$hddir/.DocumentRevisions-V100/PerUID/$newuid"
done < dir.csv

