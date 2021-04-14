#!/bin/zsh

# Based on code by Sergey Nikishkin and Jonathan Melly
# https://medium.com/acronis-design/ffmpeg-imagemagick-convert-video-to-gif-using-the-terminal-app-in-macos-657948adf900
# https://gist.github.com/anonymous/0c42267a13bce44aa7e5f077584a0012#file-vid-to-gif-sh
# https://gist.github.com/jonathanMelly/14d8da3f1a1b5fcbd6bb0353bd04fdc9#file-vid-to-gif-sh

# Usage function, displays valid arguments
usage() { echo "Usage: $0 [-f <fps, defaults to 15>] [-w <width, defaults to 480] inputfile" 1>&2; exit 1; }

# Default fps
fps=15

# getopts to process the command line arguments
while getopts ":f:w:" opt; do
    case "${opt}" in
        f) fps=${OPTARG};;
        w) width=${OPTARG};;
        *) usage;;
    esac
done

if (( $# == 0 )); then
    printf >&2 'Missing input file\n'
    usage >&2
else
	input=${(P)OPTIND}
fi

if [ -z "$width" ]; then
	width=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "${input}" | awk -F'x' '{print $1 }')
fi

# Extract filename from input file without the extension
filename=$(basename "${input}")
filename="${filename%.*}.gif"

# Debug display to show what the script is using as inputs
echo "Input: ${input}"
echo "Output: ${filename}"
echo "FPS: $fps"
echo "Width: $width"

# temporary file to store the first pass pallete
palette="/tmp/palette.png"

# options to pass to ffmpeg
filters="fps=$fps,scale=$width:-1:flags=lanczos"

# ffmpeg first pass
ffmpeg -v warning -i "${input}" -vf "$filters,palettegen" -y $palette
# ffmpeg second pass
ffmpeg -v warning -i "${input}" -i $palette -lavfi "$filters [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=3" -y "${filename}"

# display output file size
filesize=$(du -h "${filename}" | cut -f1)
echo "Output File Name: ${filename}"
echo "Output File Size: ${filesize}"
