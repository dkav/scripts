#!/bin/zsh
#
# Script to append original recording date and time to DV clips.

exiftool -d "clip-%Y-%m-%d %H;%M;%S.%%e" "-testname<DateTimeOriginal" ./*

read -p "Rename files? " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
  exiftool -d "clip-%Y-%m-%d %H;%M;%S.%%e" "-filename<DateTimeOriginal" ./*
fi
