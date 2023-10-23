#!/bin/bash

# Read file_id from the first command-line argument or from piped input
if [ -n "$1" ]; then
  # If an argument is provided, use it as the file_id
  file_id="$1"
elif [ ! -t 0 ]; then
  # If input is piped into the script, read from stdin
  read -r file_id
else
  # If neither is provided, show an error message and exit
  echo "Error: You must provide a file_id as an argument or through piped input." >&2
  exit 1
fi

# Make a POST request to generate a thumbnail
curl -X 'POST' \
  'http://127.0.0.1:8000/video/v1/generate-thumbnail' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "file_id": "'$file_id'",
    "timestamp": 5,
    "resolution": "1920x1080"
  }'
