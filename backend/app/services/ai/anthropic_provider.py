from typing import AsyncIterator, Optional
from anthropic import AsyncAnthropic
from app.services.ai.base import BaseAIProvider
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class AnthropicProvider(BaseAIProvider):
    """Anthropic (Claude) provider implementation."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key or settings.anthropic_api_key)
        self.client = AsyncAnthropic(api_key=self.api_key) if self.api_key else None
    
    def is_available(self) -> bool:
        """Check if Anthropic is available."""
        return self.api_key is not None and self.client is not None
    
    def get_default_model(self) -> str:
        """Get default Anthropic model."""
        return "claude-3-sonnet-20240229"
    
    def _convert_messages(self, messages: list[dict]) -> tuple[str, list[dict]]:
        """
        Convert messages to Anthropic format.
        Anthropic requires system messages to be separate.
        """
        system_message = ""
        converted_messages = []
        
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                converted_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        return system_message, converted_messages
    
    async def chat(
        self,
        messages: list[dict],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stream: bool = True,
    ) -> AsyncIterator[str]:
        """Send chat request to Anthropic."""
        if not self.is_available():
            raise ValueError("Anthropic provider is not available. Please set ANTHROPIC_API_KEY.")
        
        if not self.validate_messages(messages):
            raise ValueError("Invalid message format")
        
        model = model or self.get_default_model()
        system_message, converted_messages = self._convert_messages(messages)
        
        try:
            if stream:
                async with self.client.messages.stream(
                    model=model,
                    messages=converted_messages,
                    system=system_message if system_message else None,
                    temperature=temperature,
                    max_tokens=max_tokens,
                ) as stream:
                    async for text in stream.text_stream:
                        yield text
            else:
                response = await self.client.messages.create(
                    model=model,
                    messages=converted_messages,
                    system=system_message if system_message else None,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                yield response.content[0].text
                
        except Exception as e:
            logger.error(f"Anthropic error: {str(e)}")
            raise Exception(f"Anthropic API error: {str(e)}")
