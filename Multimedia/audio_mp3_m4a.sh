#!/bin/zsh

# Script to convert mp3 spoken audio files to low bit rate
# m4a files using OS X's afconvert

for i in *.mp3
 do afconvert -f 'm4af' -b 24000 -c 1 "$i" "${i%.mp3}.m4a"
done
