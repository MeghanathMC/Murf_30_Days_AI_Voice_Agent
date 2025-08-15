"""
Text-to-Speech Service using Murf AI.

This module handles all text-to-speech operations.
"""

import logging
from typing import Optional
import httpx
from ..schemas.api_schemas import TTSRequest, TTSResponse


logger = logging.getLogger(__name__)


class TTSService:
    """Service for handling text-to-speech operations."""
    
    def __init__(self, api_key: str):
        """Initialize the TTS service with API key."""
        self.api_key = api_key
        self.base_url = "https://api.murf.ai/v1/speech/generate"
        
        if api_key:
            logger.info("Murf AI TTS service initialized")
            logger.info(f"Using Murf API key: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else '[short]'}")
        else:
            logger.warning("TTS service initialized without API key")
    
    async def generate_speech(self, tts_request: TTSRequest) -> TTSResponse:
        """
        Generate speech from text using Murf AI.
        
        Args:
            tts_request: TTS request with text and voice parameters
            
        Returns:
            TTSResponse with audio URL or error information
        """
        if not self.api_key:
            logger.error("Murf API key not configured")
            return TTSResponse(
                audio_url="",
                success=False,
                error_message="TTS service not configured"
            )
        
        try:
            # Enforce Murf's character limit
            text = tts_request.text
            if len(text) > 3000:
                text = text[:2997] + "..."
                logger.warning(f"Text truncated from {len(tts_request.text)} to 3000 characters for Murf AI")
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "api-key": self.api_key
            }
            
            payload = {
                "text": text,
                "style": tts_request.style,
                "multiNativeLocale": "en-US",
                "speed": tts_request.speed,
                "pitch": tts_request.pitch,
                "volume": tts_request.volume,
                "language": "en-US",
                "voice_id": tts_request.voice_id
            }
            
            logger.info(f"Making Murf TTS request for text: {text[:100]}...")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                
                logger.info(f"Murf API response status: {response.status_code}")
                response.raise_for_status()
                
                data = response.json()
                logger.debug(f"Murf API response data: {data}")
                
                audio_url = data.get("audioFile")
                if not audio_url:
                    logger.error("No audio URL received from Murf API")
                    return TTSResponse(
                        audio_url="",
                        success=False,
                        error_message="No audio URL received from Murf API"
                    )
                
                logger.info(f"Successfully generated TTS audio: {audio_url}")
                return TTSResponse(
                    audio_url=audio_url,
                    success=True
                )
                
        except httpx.TimeoutException:
            error_msg = "TTS request timed out"
            logger.error(error_msg)
            return TTSResponse(
                audio_url="",
                success=False,
                error_message=error_msg
            )
        except httpx.HTTPStatusError as e:
            error_msg = f"TTS API error: {e.response.status_code} - {e.response.text}"
            logger.error(error_msg)
            return TTSResponse(
                audio_url="",
                success=False,
                error_message=error_msg
            )
        except Exception as e:
            error_msg = f"TTS generation failed: {str(e)}"
            logger.error(error_msg)
            return TTSResponse(
                audio_url="",
                success=False,
                error_message=error_msg
            )
    
    def generate_fallback_audio(self, message: str) -> str:
        """
        Generate fallback audio URL for error cases.
        
        Args:
            message: Error message to announce
            
        Returns:
            Fallback audio URL
        """
        logger.info(f"Generating fallback audio for message: {message}")
        # In a real implementation, you might use a simpler TTS service
        # or return a pre-recorded error message
        return "https://example.com/fallback-audio.mp3"
    
    def is_configured(self) -> bool:
        """Check if the service is properly configured."""
        return bool(self.api_key)
