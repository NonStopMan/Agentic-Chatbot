from typing import AsyncIterator, Optional
from openai import AsyncOpenAI
from app.services.ai.base import BaseAIProvider
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseAIProvider):
    """OpenAI provider implementation."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key or settings.openai_api_key)
        self.client = AsyncOpenAI(api_key=self.api_key) if self.api_key else None
    
    def is_available(self) -> bool:
        """Check if OpenAI is available."""
        return self.api_key is not None and self.client is not None
    
    def get_default_model(self) -> str:
        """Get default OpenAI model."""
        return "gpt-4"
    
    async def chat(
        self,
        messages: list[dict],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stream: bool = True,
    ) -> AsyncIterator[str]:
        """Send chat request to OpenAI."""
        if not self.is_available():
            raise ValueError("OpenAI provider is not available. Please set OPENAI_API_KEY.")
        
        if not self.validate_messages(messages):
            raise ValueError("Invalid message format")
        
        model = model or self.get_default_model()
        
        try:
            if stream:
                response = await self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True,
                )
                
                async for chunk in response:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            else:
                response = await self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=False,
                )
                yield response.choices[0].message.content
                
        except Exception as e:
            logger.error(f"OpenAI error: {str(e)}")
            raise Exception(f"OpenAI API error: {str(e)}")
