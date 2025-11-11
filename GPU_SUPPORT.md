# GPU Support Documentation

## Overview

The Fast Whisper service now supports automatic GPU detection and acceleration using CUDA. By default, it will automatically detect and use an available GPU, falling back to CPU if none is available.

## Configuration

### Environment Variables

- **WHISPER_DEVICE**: `auto` (default), `cpu`, or `cuda`
  - `auto`: Automatically detects GPU availability
  - `cpu`: Forces CPU usage
  - `cuda`: Forces GPU usage (requires NVIDIA GPU)

- **WHISPER_COMPUTE_TYPE**: `auto` (default), `int8`, `float16`, `float32`
  - `auto`: Selects optimal type based on device (float16 for GPU, int8 for CPU)
  - `float16`: Best for GPU performance
  - `int8`: Best for CPU performance
  - `float32`: Highest accuracy, slower

## Performance Comparison

### CPU (int8)
- **Speed**: Baseline
- **Memory**: ~500MB for tiny model
- **Accuracy**: Good (minor quantization effects)

### GPU (float16)
- **Speed**: 5-10x faster than CPU (model-dependent)
- **Memory**: ~1-2GB VRAM for tiny model
- **Accuracy**: Excellent

## Deployment Options

### 1. Local Development with GPU

```bash
export WHISPER_DEVICE=auto
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Docker with GPU

```bash
docker build -f Dockerfile.gpu -t fast-whisper:gpu .
docker run -d -p 8000:8000 --gpus all fast-whisper:gpu
```

### 3. Docker Compose with GPU

```bash
docker compose --profile gpu up -d
```

## Requirements for GPU Support

### Software
- NVIDIA GPU drivers (CUDA 12.1+)
- [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker)
- Docker with GPU support

### Hardware
- NVIDIA GPU with CUDA compute capability 7.0+
- Recommended: 4GB+ VRAM

## Verification

Check if GPU is being used:

```bash
curl http://localhost:8000/
```

Response should show:
```json
{
  "status": "ok",
  "model_size": "tiny",
  "language": "es",
  "device": "cuda",
  "compute_type": "float16"
}
```

## Troubleshooting

### GPU Not Detected

1. **Check CUDA availability**:
   ```python
   import torch
   print(torch.cuda.is_available())
   ```

2. **Verify Docker GPU support**:
   ```bash
   docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
   ```

3. **Check container logs**:
   ```bash
   docker logs fast-whisper-gpu
   ```

### Out of Memory Errors

- Use smaller model size (tiny, base)
- Reduce batch size in transcription
- Set `WHISPER_COMPUTE_TYPE=int8` even on GPU

## Model Performance by Size

| Model  | CPU (int8) | GPU (float16) | VRAM Usage |
|--------|-----------|---------------|------------|
| tiny   | 1x        | 5-8x faster   | ~1GB       |
| base   | 1x        | 6-10x faster  | ~1.5GB     |
| small  | 1x        | 8-12x faster  | ~2GB       |
| medium | 1x        | 10-15x faster | ~5GB       |
| large  | 1x        | 12-20x faster | ~10GB      |

*Performance varies based on audio length and GPU model*

## Best Practices

1. **Auto mode is recommended** - Let the service detect available hardware
2. **Use float16 for GPU** - Best balance of speed and accuracy
3. **Monitor VRAM usage** - Adjust model size based on available memory
4. **CPU fallback** - Service gracefully falls back to CPU if GPU fails

## Production Deployment

For production with GPU, use the GPU profile:

```bash
# Using pre-built image with GPU auto-detection
docker compose --profile ghcr up -d
# Set WHISPER_DEVICE=cuda in .env for forced GPU usage

# Or using local GPU build
docker compose --profile gpu up -d
```

Example `.env` file for GPU:
```env
WHISPER_MODEL_SIZE=base
WHISPER_LANGUAGE=es
WHISPER_DEVICE=cuda
WHISPER_COMPUTE_TYPE=float16
```

