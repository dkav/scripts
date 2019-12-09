#!/bin/sh
find . -type f -a \(  -name '*.py' -o -name '*.xsl' -o -name '*.bat' -o -name '*.txt' \) -exec dos2unix -k -s -o {} ';'