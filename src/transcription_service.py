from faster_whisper import WhisperModel
from typing import Dict, List
import torch


class TranscriptionService:
    """Service responsible for audio transcription using faster-whisper."""
    
    def __init__(self, model_size: str, language: str, device: str = "auto", compute_type: str = "auto"):
        """
        Initialize the transcription service.
        
        Args:
            model_size: Size of the Whisper model (tiny, base, small, medium, large)
            language: Language code for transcription (e.g., 'es' for Spanish)
            device: Device to use ('auto', 'cpu', 'cuda')
            compute_type: Compute type ('auto', 'int8', 'float16', 'float32', etc.)
        """
        self.model_size = model_size
        self.language = language
        self.device = self._resolve_device(device)
        self.compute_type = self._resolve_compute_type(compute_type, self.device)
        
        print(f"Initializing Whisper model: size={model_size}, device={self.device}, compute_type={self.compute_type}")
        self.model = WhisperModel(model_size, device=self.device, compute_type=self.compute_type)
    
    def _resolve_device(self, device: str) -> str:
        """Resolve device configuration."""
        if device == "auto":
            return "cuda" if torch.cuda.is_available() else "cpu"
        return device
    
    def _resolve_compute_type(self, compute_type: str, device: str) -> str:
        """Resolve compute type based on device."""
        if compute_type == "auto":
            # Use float16 for GPU, int8 for CPU
            return "float16" if device == "cuda" else "int8"
        return compute_type
    
    def transcribe(self, audio_path: str) -> Dict[str, any]:
        """
        Transcribe an audio file.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Dictionary containing transcription results
        """
        segments, info = self.model.transcribe(
            audio_path,
            language=self.language,
            beam_size=5
        )
        
        transcription_segments: List[Dict[str, any]] = []
        full_text = []
        
        for segment in segments:
            transcription_segments.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            })
            full_text.append(segment.text.strip())
        
        return {
            "language": info.language,
            "language_probability": info.language_probability,
            "duration": info.duration,
            "text": " ".join(full_text),
            "segments": transcription_segments
        }

