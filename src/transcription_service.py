from faster_whisper import WhisperModel
from typing import Dict, List


class TranscriptionService:
    """Service responsible for audio transcription using faster-whisper."""
    
    def __init__(self, model_size: str, language: str):
        """
        Initialize the transcription service.
        
        Args:
            model_size: Size of the Whisper model (tiny, base, small, medium, large)
            language: Language code for transcription (e.g., 'es' for Spanish)
        """
        self.model_size = model_size
        self.language = language
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
    
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

