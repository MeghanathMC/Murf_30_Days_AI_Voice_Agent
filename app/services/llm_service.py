"""
Large Language Model Service using Google Gemini.

This module handles all LLM operations and conversation management.
"""

import logging
from typing import List, Dict
import google.generativeai as genai
from ..schemas.api_schemas import LLMResponse, ConversationMessage


logger = logging.getLogger(__name__)


class LLMService:
    """Service for handling large language model operations."""
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash"):
        """Initialize the LLM service with API key and model."""
        self.api_key = api_key
        self.model_name = model_name
        
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name)
            logger.info(f"Gemini LLM service initialized with model: {model_name}")
        else:
            self.model = None
            logger.warning("LLM service initialized without API key")
    
    def generate_response(self, prompt: str, history: List[ConversationMessage] = None) -> LLMResponse:
        """
        Generate a response using the LLM.
        
        Args:
            prompt: The user's input prompt
            history: Previous conversation history
            
        Returns:
            LLMResponse with generated text
        """
        if not self.api_key or not self.model:
            logger.error("Gemini API key not configured")
            return LLMResponse(
                response="I'm sorry, but I'm not properly configured to generate responses.",
                success=False,
                error_message="LLM service not configured"
            )
        
        try:
            logger.info(f"Generating response for prompt: {prompt[:100]}...")
            
            # Prepare conversation history for Gemini
            gemini_history = []
            if history:
                for message in history:
                    role = "user" if message.role == "user" else "model"
                    gemini_history.append({
                        "role": role,
                        "parts": [message.content]
                    })
            
            # Add instruction for concise responses
            enhanced_prompt = f"{prompt}\n\n(Please provide a concise response under 2500 characters)"
            
            # Start chat with history and send message
            chat = self.model.start_chat(history=gemini_history)
            response = chat.send_message(enhanced_prompt)
            
            response_text = response.text or ""
            logger.info(f"Response generated successfully. Length: {len(response_text)} characters")
            
            return LLMResponse(
                response=response_text,
                success=True
            )
            
        except Exception as e:
            error_msg = f"LLM request failed: {str(e)}"
            logger.error(error_msg)
            return LLMResponse(
                response="I'm experiencing technical difficulties. Please try again.",
                success=False,
                error_message=error_msg
            )
    
    def is_configured(self) -> bool:
        """Check if the service is properly configured."""
        return bool(self.api_key and self.model)
