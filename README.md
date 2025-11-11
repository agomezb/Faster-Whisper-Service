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
export WHISPER_MODEL_SIZE=tiny       # Options: tiny, base, small, medium, large
export WHISPER_LANGUAGE=es           # Language code (es for Spanish)
export WHISPER_DEVICE=auto           # Options: auto, cpu, cuda
export WHISPER_COMPUTE_TYPE=auto     # Options: auto, int8, float16, float32
```

Or create a `.env` file:
```env
WHISPER_MODEL_SIZE=tiny
WHISPER_LANGUAGE=es
WHISPER_DEVICE=auto           # Auto-detects GPU, falls back to CPU
WHISPER_COMPUTE_TYPE=auto     # Uses float16 for GPU, int8 for CPU
```

### Device Configuration

- **`auto`** (default): Automatically detects GPU availability
  - Uses CUDA GPU if available
  - Falls back to CPU if no GPU is detected
- **`cpu`**: Forces CPU usage
- **`cuda`**: Forces GPU usage (requires NVIDIA GPU with CUDA support)

### Compute Type

- **`auto`** (default): Automatically selects based on device
  - GPU: `float16` (faster, good accuracy)
  - CPU: `int8` (faster on CPU, slight accuracy trade-off)
- **`float16`**: Best for GPU (requires CUDA)
- **`int8`**: Best for CPU, faster with minimal accuracy loss
- **`float32`**: Highest accuracy, slower performance

## Running for Production/Use

The easiest way to use this service is with the pre-built Docker image from GitHub Container Registry.

### Using Docker Compose (Recommended)

The single `docker-compose.yml` file supports multiple profiles:

```bash
# Use pre-built image from GitHub Container Registry (fastest to start)
docker compose --profile ghcr up -d

# Stop the service
docker compose --profile ghcr down

# View logs
docker compose --profile ghcr logs -f
```

Override environment variables by creating a `.env` file:
```env
WHISPER_MODEL_SIZE=base
WHISPER_LANGUAGE=en
```

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

The API will be available at `http://localhost:8000`

## Running for Development

### Option 1: Local Development (Python + uv)

Start the server with hot reload:
```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 2: Docker Compose (Local Build)

Build and run locally (CPU version - default):
```bash
# Build and start (no profile needed for default CPU)
docker compose up -d

# Or explicitly use CPU profile
docker compose --profile cpu up -d

# Stop the service
docker compose down

# View logs
docker compose logs -f

# Rebuild after code changes
docker compose up -d --build
```

### Option 3: Docker Build & Run

Build the Docker image manually:
```bash
docker build -t fast-whisper:latest .
```

Run the container:
```bash
docker run -d -p 8000:8000 \
  -e WHISPER_MODEL_SIZE=base \
  -e WHISPER_LANGUAGE=en \
  --name fast-whisper \
  fast-whisper:latest
```

Stop the container:
```bash
docker stop fast-whisper && docker rm fast-whisper
```

The API will be available at `http://localhost:8000`

## Quick Reference: Docker Compose Profiles

The single `docker-compose.yml` file provides three profiles:

| Profile | Command | Use Case |
|---------|---------|----------|
| **default/cpu** | `docker compose up -d` | Local build, CPU only (development) |
| **gpu** | `docker compose --profile gpu up -d` | Local build, GPU acceleration (development) |
| **ghcr** | `docker compose --profile ghcr up -d` | Pre-built image from registry (production) |

## GPU Support

### Using GPU with Docker Compose (Recommended)

Use the GPU profile for automatic GPU acceleration:

```bash
# Start service with GPU support
docker compose --profile gpu up -d

# View logs
docker compose --profile gpu logs -f

# Stop service
docker compose --profile gpu down
```

**Requirements:**
- NVIDIA GPU with CUDA support
- [NVIDIA Docker runtime](https://github.com/NVIDIA/nvidia-docker) installed
- CUDA 12.1+ drivers

### Using GPU with Docker Run

Build and run GPU-enabled container:

```bash
# Build GPU image
docker build -f Dockerfile.gpu -t fast-whisper:gpu .

# Run with NVIDIA runtime
docker run -d -p 8000:8000 \
  --gpus all \
  -e WHISPER_DEVICE=cuda \
  -e WHISPER_COMPUTE_TYPE=float16 \
  --name fast-whisper-gpu \
  fast-whisper:gpu
```

### Check GPU Status

After starting the service, check if GPU is being used:
```bash
curl http://localhost:8000/
```

Look for `"device": "cuda"` in the response.

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
  "language": "es",
  "device": "cpu",
  "compute_type": "int8"
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
├── Dockerfile                     # Docker configuration (CPU)
├── Dockerfile.gpu                 # Docker configuration (GPU/CUDA)
├── docker-compose.yml             # Docker Compose with profiles (cpu/gpu/ghcr)
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

