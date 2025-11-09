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
- uv package manager

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

## Running the Service

### Option 1: Local Development

Start the server:
```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 2: Docker

Build the Docker image:
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

You can override environment variables:
```bash
docker run -d -p 8000:8000 \
  -e WHISPER_MODEL_SIZE=base \
  -e WHISPER_LANGUAGE=en \
  --name fast-whisper \
  fast-whisper:latest
```

### Option 3: Docker Compose (Recommended)

Start the service:
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

Override environment variables:
```bash
WHISPER_MODEL_SIZE=base WHISPER_LANGUAGE=en docker compose up -d
```

Or create a `.env` file in the project root:
```env
WHISPER_MODEL_SIZE=base
WHISPER_LANGUAGE=en
```

Then simply run:
```bash
docker compose up -d
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

## Project Structure

```
fast-whisper/
├── src/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── config.py                  # Configuration management
│   └── transcription_service.py   # Transcription service (single responsibility)
├── Dockerfile                     # Docker configuration
├── docker-compose.yml             # Docker Compose configuration
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

