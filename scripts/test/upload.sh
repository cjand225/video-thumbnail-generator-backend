#!/bin/bash

# Read video file path from the first command-line argument or from piped input
if [ -n "$1" ]; then
  # If an argument is provided, use it as the video file path
  video_file="$1"
elif [ ! -t 0 ]; then
  # If input is piped into the script, read from stdin
  read -r video_file
else
  # If neither is provided, show an error message and exit
  echo "Error: You must provide a video file path as an argument or through piped input." >&2
  exit 1
fi

# Get the MIME type of the video file
mime_type=$(file --brief --mime-type "$video_file")

# Make a POST request to upload the video
curl -X 'POST' \
  'http://127.0.0.1:8000/video/v1/upload' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F "file=@$video_file;type=$mime_type"
