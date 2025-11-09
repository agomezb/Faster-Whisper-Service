# Fast Whisper - Audio Transcription Service

A FastAPI-based audio transcription service using faster-whisper.

## Features

- 🎤 Audio transcription via REST API
- ⚡ Fast inference using faster-whisper
- 🌍 Configurable language and model size
- 📝 Detailed transcription with timestamps
- 🔧 Simple configuration via environment variables

## Prerequisites

- Python 3.9 or higher
- uv package manager (for local development)
- Docker (for containerized deployment)

## Installation

1. Install uv (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install dependencies:
```bash
uv sync
```

## Configuration

Set environment variables (or use defaults):

```bash
export WHISPER_MODEL_SIZE=tiny  # Options: tiny, base, small, medium, large
export WHISPER_LANGUAGE=es      # Language code (es for Spanish)
```

Or create a `.env` file:
```
WHISPER_MODEL_SIZE=tiny
WHISPER_LANGUAGE=es
```

## Running for Production/Use

The easiest way to use this service is with the pre-built Docker image from GitHub Container Registry.

### Using Docker Run

Pull and run the latest image:
```bash
# Pull the latest image
docker pull ghcr.io/agomezb/faster-whisper-service:latest

# Run the container
docker run -d -p 8000:8000 \
  -e WHISPER_MODEL_SIZE=tiny \
  -e WHISPER_LANGUAGE=es \
  --name fast-whisper \
  ghcr.io/agomezb/faster-whisper-service:latest
```

Stop the container:
```bash
docker stop fast-whisper && docker rm fast-whisper
```

### Using Docker Compose

Use the provided compose file for pre-built images:
```bash
docker compose -f docker-compose.ghcr.yml up -d
```

Stop the service:
```bash
docker compose -f docker-compose.ghcr.yml down
```

View logs:
```bash
docker compose -f docker-compose.ghcr.yml logs -f
```

Override environment variables by creating a `.env` file:
```env
WHISPER_MODEL_SIZE=base
WHISPER_LANGUAGE=en
```

The API will be available at `http://localhost:8000`

## Running for Development

### Option 1: Local Development (Python + uv)

Start the server with hot reload:
```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 2: Docker Build & Run

Build the Docker image locally:
```bash
docker build -t fast-whisper:latest .
```

Run the container:
```bash
docker run -d -p 8000:8000 --name fast-whisper fast-whisper:latest
```

Stop the container:
```bash
docker stop fast-whisper && docker rm fast-whisper
```

Override environment variables:
```bash
docker run -d -p 8000:8000 \
  -e WHISPER_MODEL_SIZE=base \
  -e WHISPER_LANGUAGE=en \
  --name fast-whisper \
  fast-whisper:latest
```

### Option 3: Docker Compose (Local Build)

Start the service (builds locally):
```bash
docker compose up -d
```

Stop the service:
```bash
docker compose down
```

View logs:
```bash
docker compose logs -f
```

Rebuild after code changes:
```bash
docker compose up -d --build
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
```bash
GET /
```

Response:
```json
{
  "status": "ok",
  "model_size": "tiny",
  "language": "es"
}
```

### Transcribe Audio
```bash
POST /transcribe
```

Upload an audio file (supports mp3, wav, m4a, etc.):

```bash
curl -X POST "http://localhost:8000/transcribe" \
  -F "file=@/path/to/audio.mp3"
```

Response:
```json
{
  "language": "es",
  "language_probability": 0.99,
  "duration": 10.5,
  "text": "Full transcription text here",
  "segments": [
    {
      "start": 0.0,
      "end": 3.5,
      "text": "First segment text"
    },
    {
      "start": 3.5,
      "end": 7.2,
      "text": "Second segment text"
    }
  ]
}
```

## Interactive API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## CI/CD

This project includes a GitHub Actions workflow that automatically builds and pushes Docker images to GitHub Container Registry on every push to the `main` branch.

### Image Tags

The workflow creates the following tags:
- `latest` - Always points to the latest main branch build
- `main-{sha}` - Specific commit SHA for version tracking
- `main` - Latest main branch build

### Setup

1. The workflow uses `GITHUB_TOKEN` which is automatically provided by GitHub Actions
2. To make your images public, go to your package settings on GitHub and change the visibility
3. No additional secrets are required for basic functionality

## Project Structure

```
fast-whisper/
├── .github/
│   └── workflows/
│       └── deploy.yml             # CI/CD pipeline
├── src/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── config.py                  # Configuration management
│   └── transcription_service.py   # Transcription service (single responsibility)
├── Dockerfile                     # Docker configuration
├── docker-compose.yml             # Docker Compose configuration (local build)
├── docker-compose.ghcr.yml        # Docker Compose configuration (pre-built image)
├── .dockerignore                  # Docker ignore patterns
├── pyproject.toml                 # Project dependencies (uv)
├── .gitignore                     # Git ignore patterns
└── README.md                      # Documentation
```

## Model Sizes

| Model  | Parameters | Speed  | Accuracy |
|--------|-----------|--------|----------|
| tiny   | 39M       | Fastest| Basic    |
| base   | 74M       | Fast   | Good     |
| small  | 244M      | Medium | Better   |
| medium | 769M      | Slow   | Great    |
| large  | 1550M     | Slowest| Best     |

## License

MIT

