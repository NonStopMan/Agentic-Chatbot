from abc import ABC, abstractmethod
from typing import AsyncIterator, Optional
from app.core.config import settings


class BaseAIProvider(ABC):
    """Base class for AI providers."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.provider_name = self.__class__.__name__
    
    @abstractmethod
    async def chat(
        self,
        messages: list[dict],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stream: bool = True,
    ) -> AsyncIterator[str]:
        """
        Send chat request to AI provider.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model name to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            
        Yields:
            String chunks of the response
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available (has API key)."""
        pass
    
    @abstractmethod
    def get_default_model(self) -> str:
        """Get the default model for this provider."""
        pass
    
    def validate_messages(self, messages: list[dict]) -> bool:
        """Validate message format."""
        if not messages:
            return False
        
        for msg in messages:
            if "role" not in msg or "content" not in msg:
                return False
            if msg["role"] not in ["user", "assistant", "system"]:
                return False
        
        return True
