import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration from environment variables."""
    
    WHISPER_MODEL_SIZE: str = os.getenv("WHISPER_MODEL_SIZE", "tiny")
    WHISPER_LANGUAGE: str = os.getenv("WHISPER_LANGUAGE", "es")
    
    @classmethod
    def validate(cls) -> None:
        """Validate configuration values."""
        valid_sizes = ["tiny", "base", "small", "medium", "large"]
        if cls.WHISPER_MODEL_SIZE not in valid_sizes:
            raise ValueError(f"Invalid model size. Must be one of: {valid_sizes}")

