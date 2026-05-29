"""Secure Hugging Face API client wrapper.

This module handles all communication with Hugging Face APIs.
Implements security best practices:
- No logging of API keys
- Bearer token authentication
- Mock mode support for testing
"""
import json
from typing import Any, Dict, Optional

import requests

from orchestrator.config import config


class HFClient:
    """Secure client for Hugging Face API interactions."""

    def __init__(self):
        """Initialize the HF client."""
        self.endpoint = config.hf_model_endpoint or "https://api-inference.huggingface.co"
        self.api_key = config.hf_api_key
        self.mock_mode = config.mock_mode

    def query(
        self,
        model: str,
        prompt: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Query a Hugging Face model.

        Args:
            model: Model identifier (e.g., 'gpt2')
            prompt: Input prompt for the model
            **kwargs: Additional parameters to pass to the model

        Returns:
            Dictionary containing the model's response
        """
        if self.mock_mode:
            return self._mock_response(model, prompt, **kwargs)

        return self._real_query(model, prompt, **kwargs)

    def _mock_response(
        self,
        model: str,
        prompt: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Generate a mock response for testing.

        Args:
            model: Model identifier
            prompt: Input prompt
            **kwargs: Additional parameters

        Returns:
            Mock response dictionary
        """
        return {
            "status": "success",
            "mock": True,
            "model": model,
            "prompt": prompt,
            "generated_text": f"[Mock response from {model}] {prompt[:20]}...",
            "confidence": 0.95,
        }

    def _real_query(
        self,
        model: str,
        prompt: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Execute a real query against Hugging Face API.

        Args:
            model: Model identifier
            prompt: Input prompt
            **kwargs: Additional parameters

        Returns:
            Response from Hugging Face API

        Raises:
            requests.RequestException: If the API request fails
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "inputs": prompt,
            **kwargs,
        }

        url = f"{self.endpoint}/models/{model}"

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {
                "status": "error",
                "error": str(e),
                "model": model,
            }

    def embed(self, text: str) -> Optional[list]:
        """Get embeddings for text.

        Args:
            text: Text to embed

        Returns:
            List of embedding values or None if failed
        """
        if self.mock_mode:
            return [0.5] * 768  # Mock 768-dimensional embedding

        model = "sentence-transformers/all-MiniLM-L6-v2"
        response = self.query(model, text)

        if "error" in response:
            return None

        return response.get("generated_text", None)


# Global HF client instance
hf_client = HFClient()
