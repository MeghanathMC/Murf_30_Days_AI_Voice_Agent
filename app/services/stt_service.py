"""
Speech-to-Text Service using AssemblyAI.

This module handles all speech-to-text operations.
"""

import logging
from typing import Tuple
import assemblyai as aai
from ..schemas.api_schemas import TranscriptionResponse


logger = logging.getLogger(__name__)


class STTService:
    """Service for handling speech-to-text operations."""
    
    def __init__(self, api_key: str):
        """Initialize the STT service with API key."""
        self.api_key = api_key
        if api_key:
            aai.settings.api_key = api_key
            logger.info("AssemblyAI STT service initialized")
        else:
            logger.warning("STT service initialized without API key")
    
    def transcribe_audio(self, file_path: str) -> TranscriptionResponse:
        """
        Transcribe audio file to text.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            TranscriptionResponse with transcription result
        """
        if not self.api_key:
            logger.error("AssemblyAI API key not configured")
            return TranscriptionResponse(
                transcription="",
                success=False,
                error_message="STT service not configured"
            )
        
        try:
            logger.info(f"Starting transcription for file: {file_path}")
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(file_path)
            
            if transcript.status == aai.TranscriptStatus.error:
                error_msg = f"Transcription error: {transcript.error}"
                logger.error(error_msg)
                return TranscriptionResponse(
                    transcription="",
                    success=False,
                    error_message=error_msg
                )
            
            transcribed_text = transcript.text or ""
            confidence = getattr(transcript, 'confidence', None)
            
            logger.info(f"Transcription completed successfully. Length: {len(transcribed_text)} characters")
            
            return TranscriptionResponse(
                transcription=transcribed_text,
                confidence=confidence,
                success=True
            )
            
        except Exception as e:
            error_msg = f"Transcription failed: {str(e)}"
            logger.error(error_msg)
            return TranscriptionResponse(
                transcription="",
                success=False,
                error_message=error_msg
            )
    
    def is_configured(self) -> bool:
        """Check if the service is properly configured."""
        return bool(self.api_key)
