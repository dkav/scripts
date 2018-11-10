#!/bin/bash

# Summary: Move images files and their associated xmp sidecar
#
# Usage: mv_img_xmp <File extension of image file>
#

ext=$1
mkdir -p $ext

for x in *.$ext; do
  x=${x%.$ext}
  if [ -e "$x.xmp" ]; then
    echo $x
    mv "$x.$ext" $ext/
    mv "$x.xmp" $ext/
  fi
done
