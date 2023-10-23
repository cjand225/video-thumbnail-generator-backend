#!/bin/bash

# Read thumbnail_id from the first command-line argument or from piped input
if [ -n "$1" ]; then
  # If an argument is provided, use it as the thumbnail_id
  thumbnail_id="$1"
elif [ ! -t 0 ]; then
  # If input is piped into the script, read from stdin
  read -r thumbnail_id
else
  # If neither is provided, show an error message and exit
  echo "Error: You must provide a thumbnail_id as an argument or through piped input." >&2
  exit 1
fi

# Make a GET request to retrieve the thumbnail
curl -X 'GET' \
  "http://127.0.0.1:8000/video/v1/get-thumbnail/$thumbnail_id" \
  -H 'accept: application/json' \
  -OJ
