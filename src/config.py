import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration from environment variables."""
    
    WHISPER_MODEL_SIZE: str = os.getenv("WHISPER_MODEL_SIZE", "tiny")
    WHISPER_LANGUAGE: str = os.getenv("WHISPER_LANGUAGE", "es")
    WHISPER_DEVICE: str = os.getenv("WHISPER_DEVICE", "auto")
    WHISPER_COMPUTE_TYPE: str = os.getenv("WHISPER_COMPUTE_TYPE", "auto")
    
    @classmethod
    def validate(cls) -> None:
        """Validate configuration values."""
        valid_sizes = ["tiny", "base", "small", "medium", "large"]
        if cls.WHISPER_MODEL_SIZE not in valid_sizes:
            raise ValueError(f"Invalid model size. Must be one of: {valid_sizes}")
        
        valid_devices = ["auto", "cpu", "cuda"]
        if cls.WHISPER_DEVICE not in valid_devices:
            raise ValueError(f"Invalid device. Must be one of: {valid_devices}")
        
        valid_compute_types = ["auto", "int8", "int8_float16", "int16", "float16", "float32"]
        if cls.WHISPER_COMPUTE_TYPE not in valid_compute_types:
            raise ValueError(f"Invalid compute type. Must be one of: {valid_compute_types}")

