# Video Thumbnail Generator Backend

[![CI/CD Pipeline](https://github.com/cjand225/video-thumbnail-generator-backend/actions/workflows/main.yml/badge.svg?event=push)](https://github.com/cjand225/video-thumbnail-generator-backend/actions/workflows/main.yml)

## Description

This backend server is designed to generate thumbnails from videos, providing functionalities like uploading videos, generating thumbnails and receiving thumbnails. Built with FastAPI, it leverages asynchronous programming for improved performance, and utilizes FFmpeg for video processing tasks.

## Installation

### Prerequisites

- Python 3.11+
- Docker (optional)

### Installation Steps

1. Clone the repository:

```
git clone <repository-url>
cd <repository-name>
```

2. Install the required packages:

```
pip install -r requirements.txt
```

3. Run the application:

```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

If you are using Docker, you can build the image and run the container using:

```
make up
```

## Usage

### Endpoints

All endpoints need to be prepended with `/video/v1/`.

- `POST /upload`: Upload a video file.
- `POST /generate-thumbnail`: Generate a thumbnail from a video file.
- `GET /get-thumbnail/{thumbnail_id}`: Retrieve a generated thumbnail.

### Uploading a Video

To upload a video, send a POST request to `/upload` with the video file included in the form data.

```bash
curl -X 'POST' \
'http://127.0.0.1:8000/video/v1/upload' \
-H 'accept: application/json' \
-H 'Content-Type: multipart/form-data' \
-F 'file=@<path-to-your-video-file>;type=video/mp4'

```

### Generating a Thumbnail

To generate a thumbnail, send a POST request to /generate-thumbnail with the required information in the JSON body.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/video/v1/generate-thumbnail' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "file_id": "<your-uploaded-file-id>",
  "timestamp": "05",
  "resolution" : "320x240"
}'
```

### Retrieving a Thumbnail

To Retrieve a thumbnail, send a GET request to /get-thumbnail with the required information in the url.

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/video/v1/get-thumbnail/thumbnail_id_goes_here' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -OJ
```

## Development

### Running Tests

To run the tests, use the following command:

```
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue for any changes or additional features you'd like to suggest.
