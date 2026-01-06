from typing import Optional
from app.services.ai.base import BaseAIProvider
from app.services.ai.openai_provider import OpenAIProvider
from app.services.ai.anthropic_provider import AnthropicProvider
from app.services.ai.google_provider import GoogleProvider
import logging

logger = logging.getLogger(__name__)


class AIProviderManager:
    """Manager for AI providers."""
    
    def __init__(self):
        self.providers: dict[str, BaseAIProvider] = {
            "openai": OpenAIProvider(),
            "anthropic": AnthropicProvider(),
            "google": GoogleProvider(),
        }
    
    def get_provider(self, provider_name: str) -> Optional[BaseAIProvider]:
        """Get AI provider by name."""
        provider = self.providers.get(provider_name.lower())
        
        if provider is None:
            logger.error(f"Provider '{provider_name}' not found")
            return None
        
        if not provider.is_available():
            logger.warning(f"Provider '{provider_name}' is not available (missing API key)")
            return None
        
        return provider
    
    def get_available_providers(self) -> dict[str, bool]:
        """Get list of available providers."""
        return {
            name: provider.is_available()
            for name, provider in self.providers.items()
        }
    
    def add_provider(self, name: str, provider: BaseAIProvider):
        """Add a new provider."""
        self.providers[name.lower()] = provider
        logger.info(f"Added provider: {name}")


# Global provider manager instance
provider_manager = AIProviderManager()
