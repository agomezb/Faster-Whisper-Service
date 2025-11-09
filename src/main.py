from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
from pathlib import Path

from src.config import Config
from src.transcription_service import TranscriptionService


Config.validate()

app = FastAPI(
    title="Audio Transcription Service",
    description="Transcribe audio files using faster-whisper",
    version="0.1.0"
)

transcription_service = TranscriptionService(
    model_size=Config.WHISPER_MODEL_SIZE,
    language=Config.WHISPER_LANGUAGE
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "model_size": Config.WHISPER_MODEL_SIZE,
        "language": Config.WHISPER_LANGUAGE
    }


@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Transcribe an audio file.
    
    Args:
        file: Audio file to transcribe (supported formats: mp3, wav, m4a, etc.)
        
    Returns:
        Transcription results including text and segments with timestamps
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Create a temporary file to store the uploaded audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
        try:
            # Write uploaded file to temporary file
            content = await file.read()
            temp_file.write(content)
            temp_file.flush()
            
            # Transcribe the audio
            result = transcription_service.transcribe(temp_file.name)
            
            return JSONResponse(content=result)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
        
        finally:
            # Clean up temporary file
            os.unlink(temp_file.name)

