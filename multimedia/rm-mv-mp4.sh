#!/bin/bash
#
# Rename and move mp4 files that are named mp4
# and are stored in a timestamped folder.
#
# From dir1/dir2/1683743051104/mp4
#   to dir1/mp4/20230510_282411.mp4

find $1 -name 'mp4' |
  while IFS= read -r FILE; do
    FDIR="$(dirname "${FILE}")"
    BDIR="$(basename "${FDIR}")"
    FDATE=$(date -d  @"$(  echo "($BDIR + 500) / 1000" | bc)" \
      +'%y%m%d_%H%M%S')
    echo $BDIR
    cp -f $FILE "$FDIR/../../mp4/$FDATE.mp4"
  done
