# Faster Whisper Hardware Requirements

This document outlines the hardware requirements for running the different faster-whisper model sizes. The requirements can vary based on the quantization used.

## Model Sizes and VRAM Requirements

The following table summarizes the approximate VRAM (Video RAM) required for each model size with different quantization levels.

| Model | `float16` | `int8` |
|---|---|---|
| large-v3 | ~4.9 GB | ~2.5 GB |
| large-v2 | ~4.9 GB | ~2.5 GB |
| large | ~4.9 GB | ~2.5 GB |
| medium | ~2.6 GB | ~1.3 GB |
| small | ~1.1 GB | ~0.6 GB |
| base | ~0.4 GB | ~0.2 GB |
| tiny | ~0.2 GB | ~0.1 GB |

### Notes

- The values above are estimates. Actual VRAM usage can be slightly higher.
- Using a GPU is highly recommended for better performance, especially for medium and larger models.
- When a GPU is not available, the models will run on the CPU, which will be significantly slower. RAM requirements will depend on the model size.

## Official Documentation

For more detailed information, please refer to the official faster-whisper documentation:

- **GitHub Repository:** [https://github.com/SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper)
