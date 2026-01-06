from typing import AsyncIterator, Optional
import google.generativeai as genai
from app.services.ai.base import BaseAIProvider
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class GoogleProvider(BaseAIProvider):
    """Google (Gemini) provider implementation."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key or settings.google_api_key)
        if self.api_key:
            genai.configure(api_key=self.api_key)
    
    def is_available(self) -> bool:
        """Check if Google is available."""
        return self.api_key is not None
    
    def get_default_model(self) -> str:
        """Get default Google model."""
        return "gemini-pro"
    
    def _convert_messages(self, messages: list[dict]) -> list[dict]:
        """
        Convert messages to Google format.
        Google uses 'user' and 'model' roles instead of 'assistant'.
        """
        converted_messages = []
        
        for msg in messages:
            role = msg["role"]
            if role == "assistant":
                role = "model"
            elif role == "system":
                # Google doesn't have system role, prepend to first user message
                continue
            
            converted_messages.append({
                "role": role,
                "parts": [msg["content"]]
            })
        
        return converted_messages
    
    async def chat(
        self,
        messages: list[dict],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stream: bool = True,
    ) -> AsyncIterator[str]:
        """Send chat request to Google."""
        if not self.is_available():
            raise ValueError("Google provider is not available. Please set GOOGLE_API_KEY.")
        
        if not self.validate_messages(messages):
            raise ValueError("Invalid message format")
        
        model_name = model or self.get_default_model()
        
        try:
            model = genai.GenerativeModel(model_name)
            converted_messages = self._convert_messages(messages)
            
            # Create chat session
            chat = model.start_chat(history=converted_messages[:-1] if len(converted_messages) > 1 else [])
            
            # Get the last message
            last_message = messages[-1]["content"]
            
            if stream:
                response = await chat.send_message_async(
                    last_message,
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens,
                    ),
                    stream=True,
                )
                
                async for chunk in response:
                    if chunk.text:
                        yield chunk.text
            else:
                response = await chat.send_message_async(
                    last_message,
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens,
                    ),
                )
                yield response.text
                
        except Exception as e:
            logger.error(f"Google error: {str(e)}")
            raise Exception(f"Google API error: {str(e)}")
