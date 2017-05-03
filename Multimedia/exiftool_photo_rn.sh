#!/bin/bash

# Summary: Add prefix and timestamp to photo
#
# Usage: rn_photo file/folder <prefix>
#
# Options: -s Remove seconds from file name


fname="%Y%m%dT%H%M%S"

while getopts ":s" opt; do
  case ${opt} in
    s) fname="%Y%m%dT%H%M" ;;
    \?) echo "Invalid option: -$OPTARG" >&2 ;;
  esac
done

shift $(($OPTIND - 1))

exiftool '-FileName<DateTimeOriginal' -d $fname"%%-c$2.%%le" $1
