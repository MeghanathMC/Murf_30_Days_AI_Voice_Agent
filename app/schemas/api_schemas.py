"""
API Schema definitions for the Voice Assistant application.

This module contains Pydantic models for request and response validation.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class MessageRole(str, Enum):
    """Enumeration for message roles in conversation history."""
    USER = "user"
    ASSISTANT = "assistant"


class ConversationMessage(BaseModel):
    """Model for individual conversation messages."""
    role: MessageRole = Field(..., description="The role of the message sender")
    content: str = Field(..., description="The content of the message")


class TTSRequest(BaseModel):
    """Request model for text-to-speech conversion."""
    text: str = Field(..., description="Text to convert to speech")
    voice_id: Optional[str] = Field(default="en-US-natalie", description="Voice ID for TTS")
    style: Optional[str] = Field(default="Conversational", description="Voice style")
    speed: Optional[float] = Field(default=1.0, ge=0.5, le=2.0, description="Speech speed")
    pitch: Optional[float] = Field(default=1.0, ge=0.5, le=2.0, description="Speech pitch")
    volume: Optional[float] = Field(default=1.0, ge=0.1, le=2.0, description="Speech volume")


class TTSResponse(BaseModel):
    """Response model for text-to-speech conversion."""
    audio_url: str = Field(..., description="URL to the generated audio file")
    success: bool = Field(default=True, description="Whether the operation was successful")
    error_message: Optional[str] = Field(default=None, description="Error message if any")


class TranscriptionResponse(BaseModel):
    """Response model for speech-to-text transcription."""
    transcription: str = Field(..., description="The transcribed text")
    confidence: Optional[float] = Field(default=None, description="Confidence score")
    success: bool = Field(default=True, description="Whether the operation was successful")
    error_message: Optional[str] = Field(default=None, description="Error message if any")


class LLMResponse(BaseModel):
    """Response model for LLM text generation."""
    response: str = Field(..., description="Generated response text")
    success: bool = Field(default=True, description="Whether the operation was successful")
    error_message: Optional[str] = Field(default=None, description="Error message if any")


class VoiceQueryResponse(BaseModel):
    """Response model for complete voice query processing."""
    session_id: Optional[str] = Field(default=None, description="Session identifier")
    audio_url: str = Field(..., description="URL to the generated audio response")
    transcription: str = Field(..., description="Transcribed user input")
    llm_response: str = Field(..., description="LLM generated response")
    history_length: Optional[int] = Field(default=None, description="Length of conversation history")
    error: Optional[str] = Field(default=None, description="Error type if any occurred")
    success: bool = Field(default=True, description="Overall operation success status")


class EchoTTSResponse(BaseModel):
    """Response model for echo TTS (transcribe and repeat back)."""
    audio_url: str = Field(..., description="URL to the generated audio")
    transcription: str = Field(..., description="Transcribed text")
    error: Optional[str] = Field(default=None, description="Error type if any")
    success: bool = Field(default=True, description="Whether the operation was successful")


class ErrorResponse(BaseModel):
    """Standard error response model."""
    error_type: str = Field(..., description="Type of error that occurred")
    error_message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional error details")
    timestamp: Optional[str] = Field(default=None, description="Error timestamp")


class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str = Field(default="healthy", description="Service health status")
    api_keys_configured: Dict[str, bool] = Field(..., description="Status of API key configuration")
    timestamp: str = Field(..., description="Health check timestamp")
    version: Optional[str] = Field(default=None, description="Application version")


class SessionInfo(BaseModel):
    """Model for session information."""
    session_id: str = Field(..., description="Unique session identifier")
    message_count: int = Field(default=0, description="Number of messages in session")
    created_at: Optional[str] = Field(default=None, description="Session creation timestamp")
    last_activity: Optional[str] = Field(default=None, description="Last activity timestamp")
