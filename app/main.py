"""
Refactored Voice Assistant Application.

A modern, maintainable FastAPI application for voice-based AI interactions.
"""

import os
import shutil
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .config.settings import settings, fallback_responses
from .schemas.api_schemas import (
    TTSRequest, TTSResponse, TranscriptionResponse, VoiceQueryResponse,
    EchoTTSResponse, ErrorResponse, HealthCheckResponse,
    ConversationMessage, MessageRole
)
from .services.stt_service import STTService
from .services.llm_service import LLMService
from .services.tts_service import TTSService


# Setup logging
settings.setup_logging()
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A sophisticated voice-powered conversational AI assistant"
)

# Initialize services
stt_service = STTService(settings.assemblyai_api_key)
llm_service = LLMService(settings.gemini_api_key, settings.llm_model)
tts_service = TTSService(settings.murf_api_key)

# In-memory conversation storage (consider using Redis for production)
chat_history: Dict[str, List[ConversationMessage]] = {}

# Create necessary directories
temp_upload_dir = Path(settings.temp_upload_dir)
temp_upload_dir.mkdir(exist_ok=True)


@app.on_event("startup")
async def startup_event():
    """Application startup event handler."""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"API Key Status: {settings.get_api_key_status()}")
    
    if not settings.all_apis_configured():
        logger.warning("Not all API keys are configured. Some features may not work.")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event handler."""
    logger.info("Shutting down Voice Assistant application")


# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def get_home():
    """Serve the main application page."""
    return FileResponse(os.path.join("static", "index.html"))


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint."""
    return HealthCheckResponse(
        status="healthy",
        api_keys_configured=settings.get_api_key_status(),
        timestamp=datetime.utcnow().isoformat(),
        version=settings.app_version
    )


@app.post("/transcribe/file", response_model=TranscriptionResponse)
async def transcribe_audio_file(file: UploadFile = File(...)):
    """Transcribe an audio file to text."""
    if not stt_service.is_configured():
        raise HTTPException(
            status_code=500,
            detail="Speech-to-text service not configured"
        )
    
    file_path = None
    try:
        # Save uploaded file temporarily
        file_path = temp_upload_dir / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Transcribe audio
        result = stt_service.transcribe_audio(str(file_path))
        
        if not result.success:
            raise HTTPException(status_code=500, detail=result.error_message)
        
        return result
        
    except Exception as e:
        logger.error(f"Transcription endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Cleanup temporary file
        if file_path and file_path.exists():
            os.remove(file_path)


@app.post("/tts", response_model=TTSResponse)
async def generate_tts(request: TTSRequest):
    """Generate speech from text."""
    if not tts_service.is_configured():
        raise HTTPException(
            status_code=500,
            detail="Text-to-speech service not configured"
        )
    
    try:
        result = await tts_service.generate_speech(request)
        
        if not result.success:
            raise HTTPException(status_code=500, detail=result.error_message)
        
        return result
        
    except Exception as e:
        logger.error(f"TTS endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tts/echo", response_model=EchoTTSResponse)
async def echo_tts(file: UploadFile = File(...)):
    """Transcribe audio and echo it back using TTS."""
    if not (stt_service.is_configured() and tts_service.is_configured()):
        raise HTTPException(
            status_code=500,
            detail="Required services not configured"
        )
    
    file_path = None
    try:
        # Save uploaded file temporarily
        file_path = temp_upload_dir / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Transcribe audio
        transcription_result = stt_service.transcribe_audio(str(file_path))
        if not transcription_result.success:
            return EchoTTSResponse(
                audio_url=tts_service.generate_fallback_audio(
                    fallback_responses.get_fallback("stt_failure")
                ),
                transcription="Could not transcribe audio",
                error="stt_failure",
                success=False
            )
        
        # Generate TTS from transcription
        tts_request = TTSRequest(
            text=transcription_result.transcription,
            voice_id=settings.default_voice_id,
            style=settings.default_voice_style
        )
        tts_result = await tts_service.generate_speech(tts_request)
        
        return EchoTTSResponse(
            audio_url=tts_result.audio_url if tts_result.success else tts_service.generate_fallback_audio(
                fallback_responses.get_fallback("tts_failure")
            ),
            transcription=transcription_result.transcription,
            error="tts_failure" if not tts_result.success else None,
            success=tts_result.success
        )
        
    except Exception as e:
        logger.error(f"Echo TTS error: {str(e)}")
        return EchoTTSResponse(
            audio_url=tts_service.generate_fallback_audio(
                fallback_responses.get_fallback("general_failure")
            ),
            transcription="Error occurred",
            error="general_failure",
            success=False
        )
    
    finally:
        if file_path and file_path.exists():
            os.remove(file_path)


@app.post("/llm/query", response_model=VoiceQueryResponse)
async def query_llm(file: UploadFile = File(...)):
    """Process voice input through the complete AI pipeline."""
    if not settings.all_apis_configured():
        logger.error("Missing API keys")
        return VoiceQueryResponse(
            audio_url=tts_service.generate_fallback_audio(
                fallback_responses.get_fallback("api_keys_missing")
            ),
            transcription="API keys not configured",
            llm_response=fallback_responses.get_fallback("api_keys_missing"),
            error="api_keys_missing",
            success=False
        )
    
    file_path = None
    try:
        # Save uploaded file temporarily
        file_path = temp_upload_dir / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Step 1: Transcribe audio
        transcription_result = stt_service.transcribe_audio(str(file_path))
        if not transcription_result.success:
            return VoiceQueryResponse(
                audio_url=tts_service.generate_fallback_audio(
                    fallback_responses.get_fallback("stt_failure")
                ),
                transcription="Could not transcribe audio",
                llm_response=fallback_responses.get_fallback("stt_failure"),
                error="stt_failure",
                success=False
            )
        
        # Step 2: Get LLM response
        llm_result = llm_service.generate_response(transcription_result.transcription)
        if not llm_result.success:
            return VoiceQueryResponse(
                audio_url=tts_service.generate_fallback_audio(
                    fallback_responses.get_fallback("llm_failure")
                ),
                transcription=transcription_result.transcription,
                llm_response=llm_result.response,
                error="llm_failure",
                success=False
            )
        
        # Step 3: Generate TTS
        tts_request = TTSRequest(
            text=llm_result.response,
            voice_id=settings.default_voice_id,
            style=settings.default_voice_style
        )
        tts_result = await tts_service.generate_speech(tts_request)
        
        return VoiceQueryResponse(
            audio_url=tts_result.audio_url if tts_result.success else tts_service.generate_fallback_audio(
                fallback_responses.get_fallback("tts_failure")
            ),
            transcription=transcription_result.transcription,
            llm_response=llm_result.response,
            error="tts_failure" if not tts_result.success else None,
            success=tts_result.success
        )
        
    except Exception as e:
        logger.error(f"Unexpected error in query_llm: {str(e)}")
        return VoiceQueryResponse(
            audio_url=tts_service.generate_fallback_audio(
                fallback_responses.get_fallback("general_failure")
            ),
            transcription="Error occurred",
            llm_response=fallback_responses.get_fallback("general_failure"),
            error="general_failure",
            success=False
        )
    
    finally:
        if file_path and file_path.exists():
            os.remove(file_path)


@app.post("/agent/chat/{session_id}", response_model=VoiceQueryResponse)
async def agent_chat(session_id: str, file: UploadFile = File(...)):
    """Conversational agent with session-based history."""
    if not settings.all_apis_configured():
        logger.error("Missing API keys for agent chat")
        return VoiceQueryResponse(
            session_id=session_id,
            audio_url=tts_service.generate_fallback_audio(
                fallback_responses.get_fallback("api_keys_missing")
            ),
            transcription="API keys not configured",
            llm_response=fallback_responses.get_fallback("api_keys_missing"),
            history_length=0,
            error="api_keys_missing",
            success=False
        )
    
    file_path = None
    try:
        # Save uploaded file temporarily
        file_path = temp_upload_dir / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Initialize or retrieve session history
        history = chat_history.setdefault(session_id, [])
        
        # Step 1: Transcribe audio
        transcription_result = stt_service.transcribe_audio(str(file_path))
        if not transcription_result.success:
            return VoiceQueryResponse(
                session_id=session_id,
                audio_url=tts_service.generate_fallback_audio(
                    fallback_responses.get_fallback("stt_failure")
                ),
                transcription="Could not transcribe audio",
                llm_response=fallback_responses.get_fallback("stt_failure"),
                history_length=len(history),
                error="stt_failure",
                success=False
            )
        
        # Add user message to history
        user_message = ConversationMessage(
            role=MessageRole.USER,
            content=transcription_result.transcription
        )
        history.append(user_message)
        
        # Maintain history length limit
        if len(history) > settings.max_history_length:
            history = history[-settings.max_history_length:]
            chat_history[session_id] = history
        
        # Step 2: Get LLM response with context
        llm_result = llm_service.generate_response(
            transcription_result.transcription,
            history[:-1]  # Exclude the current message
        )
        
        if not llm_result.success:
            return VoiceQueryResponse(
                session_id=session_id,
                audio_url=tts_service.generate_fallback_audio(
                    fallback_responses.get_fallback("llm_failure")
                ),
                transcription=transcription_result.transcription,
                llm_response=llm_result.response,
                history_length=len(history),
                error="llm_failure",
                success=False
            )
        
        # Add assistant response to history
        assistant_message = ConversationMessage(
            role=MessageRole.ASSISTANT,
            content=llm_result.response
        )
        history.append(assistant_message)
        
        # Step 3: Generate TTS
        tts_request = TTSRequest(
            text=llm_result.response,
            voice_id=settings.default_voice_id,
            style=settings.default_voice_style
        )
        tts_result = await tts_service.generate_speech(tts_request)
        
        return VoiceQueryResponse(
            session_id=session_id,
            audio_url=tts_result.audio_url if tts_result.success else tts_service.generate_fallback_audio(
                fallback_responses.get_fallback("tts_failure")
            ),
            transcription=transcription_result.transcription,
            llm_response=llm_result.response,
            history_length=len(history),
            error="tts_failure" if not tts_result.success else None,
            success=tts_result.success
        )
        
    except Exception as e:
        logger.error(f"Agent chat error: {str(e)}")
        return VoiceQueryResponse(
            session_id=session_id,
            audio_url=tts_service.generate_fallback_audio(
                fallback_responses.get_fallback("general_failure")
            ),
            transcription="Error occurred",
            llm_response=fallback_responses.get_fallback("general_failure"),
            history_length=len(chat_history.get(session_id, [])),
            error="general_failure",
            success=False
        )
    
    finally:
        if file_path and file_path.exists():
            os.remove(file_path)


@app.delete("/agent/chat/{session_id}")
async def clear_session(session_id: str):
    """Clear conversation history for a session."""
    if session_id in chat_history:
        del chat_history[session_id]
        logger.info(f"Cleared session history for session: {session_id}")
    
    return {"message": f"Session {session_id} cleared"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
