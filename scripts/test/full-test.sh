#!/bin/bash

# Script: End-to-End Test

# Path to the video file, should be provided as the first command-line argument
video_file="$1"

if [ -z "$video_file" ]; then
  echo "Error: You must provide a video file path as the first argument." >&2
  exit 1
fi

# Step 1: Upload Video and Extract file_id
upload_response=$(./upload.sh "$video_file")
file_id=$(echo "$upload_response" | grep -o '"file_id":"[^"]*"' | awk -F '"' '{print $4}')

if [ -z "$file_id" ]; then
  echo "Error: Failed to extract file_id from the upload response." >&2
  echo "Upload Response: $upload_response"
  exit 1
fi

echo "Extracted file_id: $file_id"

# Step 2: Generate Thumbnail and Extract thumbnail_id
generate_response=$(echo "$file_id" | ./generate-thumbnail.sh)
thumbnail_id=$(echo "$generate_response" | grep -o '"thumbnail_id":"[^"]*"' | awk -F '"' '{print $4}')

if [ -z "$thumbnail_id" ]; then
  echo "Error: Failed to extract thumbnail_id from the generate thumbnail response." >&2
  echo "Generate Thumbnail Response: $generate_response"
  exit 1
fi

echo "Extracted thumbnail_id: $thumbnail_id"

# Step 3: Get Thumbnail
get_thumbnail_response=$(echo "$thumbnail_id" | ./get-thumbnail.sh)

echo "Get Thumbnail Response: $get_thumbnail_response"
echo "End-to-end test completed successfully."
