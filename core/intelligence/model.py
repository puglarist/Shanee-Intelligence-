"""Model Management - Interface to LLMs and reasoning engines"""

from dataclasses import dataclass
from typing import Optional, Any
from enum import Enum

from anthropic import Anthropic, AsyncAnthropic


class ModelProvider(str, Enum):
    """Supported model providers"""
    ANTHROPIC = "anthropic"
    LOCAL = "local"
    OPENAI = "openai"
    CUSTOM = "custom"


@dataclass
class ModelConfig:
    """Configuration for model selection and behavior"""
    provider: ModelProvider = ModelProvider.ANTHROPIC
    model_id: str = "claude-opus-4-7"
    temperature: float = 0.7
    max_tokens: int = 4096
    timeout_seconds: float = 60.0
    retry_count: int = 3
    cache_responses: bool = True
    api_key: Optional[str] = None
    base_url: Optional[str] = None


class ModelManager:
    """
    Manages model selection, routing, and caching.
    Abstracts away provider-specific details.
    """

    def __init__(self, config: ModelConfig):
        self.config = config
        self.client = self._init_client()
        self.response_cache: dict[str, Any] = {}

    def _init_client(self):
        """Initialize appropriate client based on provider"""
        if self.config.provider == ModelProvider.ANTHROPIC:
            return AsyncAnthropic(api_key=self.config.api_key)
        elif self.config.provider == ModelProvider.LOCAL:
            return None  # Local model integration TBD
        elif self.config.provider == ModelProvider.OPENAI:
            return None  # OpenAI integration TBD
        else:
            return None

    async def complete(
        self,
        messages: list[dict[str, str]],
        system_prompt: Optional[str] = None,
        tools: Optional[list[dict]] = None,
        **kwargs
    ) -> str:
        """
        Get completion from model.
        Supports both chat and tool-use patterns.
        """
        if not self.client:
            raise RuntimeError(f"No client for provider: {self.config.provider}")

        # Build request
        request_params = {
            "model": self.config.model_id,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "messages": messages,
            **kwargs
        }

        if system_prompt:
            request_params["system"] = system_prompt

        if tools:
            request_params["tools"] = tools

        # Get completion
        response = await self.client.messages.create(**request_params)
        return response.content[0].text if response.content else ""

    async def stream_complete(
        self,
        messages: list[dict[str, str]],
        system_prompt: Optional[str] = None,
        tools: Optional[list[dict]] = None,
        **kwargs
    ):
        """Stream completion for real-time responses"""
        if not self.client:
            raise RuntimeError(f"No client for provider: {self.config.provider}")

        request_params = {
            "model": self.config.model_id,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "messages": messages,
            **kwargs
        }

        if system_prompt:
            request_params["system"] = system_prompt

        if tools:
            request_params["tools"] = tools

        async with self.client.messages.stream(**request_params) as stream:
            async for text in stream.text_stream:
                yield text

    def clear_cache(self):
        """Clear response cache"""
        self.response_cache.clear()

    def get_model_info(self) -> dict:
        """Get current model configuration"""
        return {
            "provider": self.config.provider.value,
            "model_id": self.config.model_id,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
        }


class ModelRouter:
    """Route different request types to optimal models"""

    def __init__(self):
        self.models: dict[str, ModelManager] = {}
        self.default_model: Optional[ModelManager] = None

    def register(self, name: str, manager: ModelManager):
        """Register a model for specific use case"""
        self.models[name] = manager
        if not self.default_model:
            self.default_model = manager

    def get_model(self, use_case: str = "default") -> ModelManager:
        """Get appropriate model for use case"""
        return self.models.get(use_case, self.default_model)

    def route(self, request: dict) -> ModelManager:
        """Route request to optimal model"""
        request_type = request.get("type", "default")
        return self.get_model(request_type)
