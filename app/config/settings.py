"""
Configuration settings for the Voice Assistant application.

This module handles environment variables and application settings.
"""

import os
import logging
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    assemblyai_api_key: Optional[str] = Field(default=None, alias="ASSEMBLYAI_API_KEY")
    gemini_api_key: Optional[str] = Field(default=None, alias="GEMINI_API_KEY")
    murf_api_key: Optional[str] = Field(default=None, alias="MURF_API_KEY")
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    debug: bool = Field(default=False, alias="DEBUG")
    
    # Application Configuration
    app_name: str = Field(default="AI Voice Assistant")
    app_version: str = Field(default="1.0.0")
    
    # LLM Configuration
    llm_model: str = Field(default="gemini-2.5-flash", alias="LLM_MODEL")
    max_history_length: int = Field(default=50, alias="MAX_HISTORY_LENGTH")
    
    # TTS Configuration
    default_voice_id: str = Field(default="en-US-natalie", alias="DEFAULT_VOICE_ID")
    default_voice_style: str = Field(default="Conversational", alias="DEFAULT_VOICE_STYLE")
    max_text_length: int = Field(default=3000, alias="MAX_TEXT_LENGTH")
    
    # File handling
    temp_upload_dir: str = Field(default="temp_uploads", alias="TEMP_UPLOAD_DIR")
    max_file_size: int = Field(default=50 * 1024 * 1024, alias="MAX_FILE_SIZE")  # 50MB
    
    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        alias="LOG_FORMAT"
    )
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def get_api_key_status(self) -> dict:
        """Get the status of all API keys."""
        return {
            "assemblyai": bool(self.assemblyai_api_key),
            "gemini": bool(self.gemini_api_key),
            "murf": bool(self.murf_api_key)
        }
    
    def all_apis_configured(self) -> bool:
        """Check if all required API keys are configured."""
        status = self.get_api_key_status()
        return all(status.values())
    
    def setup_logging(self) -> None:
        """Setup application logging configuration."""
        logging.basicConfig(
            level=getattr(logging, self.log_level.upper()),
            format=self.log_format,
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler("voice_assistant.log")
            ]
        )
        
        # Set specific logger levels
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("httpcore").setLevel(logging.WARNING)


# Global settings instance
settings = Settings()


class FallbackResponses:
    """Predefined fallback responses for various error scenarios."""
    
    STT_FAILURE = "I'm having trouble understanding your voice right now. Please try again."
    LLM_FAILURE = "I'm having trouble processing your request. Please try again."
    TTS_FAILURE = "I'm having trouble speaking right now. Please try again."
    GENERAL_FAILURE = "I'm experiencing technical difficulties. Please try again later."
    API_KEYS_MISSING = "I'm not properly configured. Please check the server setup."
    
    @classmethod
    def get_fallback(cls, error_type: str) -> str:
        """Get fallback response for a specific error type."""
        fallback_map = {
            "stt_failure": cls.STT_FAILURE,
            "llm_failure": cls.LLM_FAILURE,
            "tts_failure": cls.TTS_FAILURE,
            "general_failure": cls.GENERAL_FAILURE,
            "api_keys_missing": cls.API_KEYS_MISSING,
        }
        return fallback_map.get(error_type, cls.GENERAL_FAILURE)


# Global fallback responses instance
fallback_responses = FallbackResponses()
