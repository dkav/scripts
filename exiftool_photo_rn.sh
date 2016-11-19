#!/bin/bash

# Summary: Add prefix and timestamp to photo
#
# Usage: rn_photo <prefix>
#

exiftool '-FileName<DateTimeOriginal' -d "%Y%m%dT%H%M%S%%-c$1.%%le" .
