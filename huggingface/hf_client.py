"""
HuggingFace Integration Client
Handles inference requests to HF endpoints for 500-agent swarm execution
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import asyncio
import aiohttp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class InferenceRequest:
    """Represents an inference request to HF"""
    task_id: str
    agent_id: str
    model: str
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.9
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0


@dataclass
class InferenceResponse:
    """Response from HF inference endpoint"""
    task_id: str
    agent_id: str
    status: str  # "success" | "error" | "timeout"
    output: Optional[str] = None
    error: Optional[str] = None
    tokens_used: int = 0
    execution_time: float = 0.0
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()


class HFClient:
    """
    HuggingFace inference client for swarm execution
    Manages API requests, retries, load balancing across endpoints
    """

    def __init__(self, api_key: str = None, endpoints: Dict[str, str] = None):
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY", "")
        self.endpoints = endpoints or {
            "text-generation": "https://api-inference.huggingface.co/models/meta-llama/Llama-2-70b-chat",
            "code-generation": "https://api-inference.huggingface.co/models/bigcode/starcoder",
            "analysis": "https://api-inference.huggingface.co/models/meta-llama/Llama-2-70b-chat",
        }

        self.request_history: List[Dict] = []
        self.error_counts: Dict[str, int] = {}
        self.inference_timeout = 60
        self.max_retries = 3

        if not self.api_key:
            logger.warning("HUGGINGFACE_API_KEY not set - will use demo mode")

    async def infer(
        self,
        request: InferenceRequest,
        endpoint_type: str = "text-generation"
    ) -> InferenceResponse:
        """
        Execute inference request to HF endpoint
        """
        start_time = datetime.utcnow()

        try:
            # In demo mode without API key, return simulated response
            if not self.api_key:
                return await self._simulate_inference(request)

            endpoint = self.endpoints.get(endpoint_type)
            if not endpoint:
                return InferenceResponse(
                    task_id=request.task_id,
                    agent_id=request.agent_id,
                    status="error",
                    error=f"Unknown endpoint type: {endpoint_type}"
                )

            # Make request with retries
            for attempt in range(self.max_retries):
                try:
                    response = await self._call_hf_endpoint(endpoint, request)
                    execution_time = (datetime.utcnow() - start_time).total_seconds()

                    return InferenceResponse(
                        task_id=request.task_id,
                        agent_id=request.agent_id,
                        status="success",
                        output=response.get("generated_text", ""),
                        tokens_used=response.get("tokens_used", 0),
                        execution_time=execution_time
                    )

                except asyncio.TimeoutError:
                    if attempt == self.max_retries - 1:
                        return InferenceResponse(
                            task_id=request.task_id,
                            agent_id=request.agent_id,
                            status="timeout",
                            error="HF inference timeout"
                        )
                    await asyncio.sleep(2 ** attempt)  # exponential backoff

                except Exception as e:
                    if attempt == self.max_retries - 1:
                        return InferenceResponse(
                            task_id=request.task_id,
                            agent_id=request.agent_id,
                            status="error",
                            error=str(e)
                        )
                    await asyncio.sleep(2 ** attempt)

        except Exception as e:
            logger.error(f"Inference failed for task {request.task_id}: {e}")
            return InferenceResponse(
                task_id=request.task_id,
                agent_id=request.agent_id,
                status="error",
                error=str(e)
            )

    async def batch_infer(self, requests: List[InferenceRequest]) -> List[InferenceResponse]:
        """Execute multiple inference requests in parallel"""
        tasks = [
            self.infer(req, self._get_endpoint_type(req.model))
            for req in requests
        ]
        return await asyncio.gather(*tasks)

    async def _call_hf_endpoint(self, endpoint: str, request: InferenceRequest) -> Dict:
        """Make actual HTTP request to HF endpoint"""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "inputs": request.prompt,
            "parameters": {
                "temperature": request.temperature,
                "max_new_tokens": request.max_tokens,
                "top_p": request.top_p,
                "frequency_penalty": request.frequency_penalty,
                "presence_penalty": request.presence_penalty,
            }
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    endpoint,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=self.inference_timeout)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return {
                            "generated_text": data[0].get("generated_text", "") if isinstance(data, list) else data.get("generated_text", ""),
                            "tokens_used": 0  # Would come from actual API
                        }
                    else:
                        raise Exception(f"HF API error: {resp.status}")
            except asyncio.TimeoutError:
                raise

    async def _simulate_inference(self, request: InferenceRequest) -> InferenceResponse:
        """Simulate inference when no API key (for testing)"""
        await asyncio.sleep(0.5)  # Simulate processing

        # Generate contextual response based on task content
        if "test" in request.prompt.lower():
            output = "✓ Tests passed\n✓ All test cases executed\n✓ Coverage: 85%"
        elif "debug" in request.prompt.lower():
            output = "✓ Debugged successfully\n✓ Root cause identified\n✓ Fix applied"
        elif "code" in request.prompt.lower():
            output = "```python\ndef generated_function():\n    return 'Generated code'\n```"
        elif "review" in request.prompt.lower():
            output = "✓ Code review complete\n✓ No issues found\n✓ Approved for merge"
        else:
            output = "✓ Task completed successfully"

        return InferenceResponse(
            task_id=request.task_id,
            agent_id=request.agent_id,
            status="success",
            output=output,
            tokens_used=len(request.prompt.split()) + len(output.split()),
            execution_time=0.5
        )

    def _get_endpoint_type(self, model: str) -> str:
        """Determine endpoint type from model name"""
        if "code" in model.lower() or "star" in model.lower():
            return "code-generation"
        elif "analysis" in model.lower():
            return "analysis"
        return "text-generation"

    def get_inference_stats(self) -> Dict:
        """Get inference statistics"""
        return {
            "total_requests": len(self.request_history),
            "error_counts": self.error_counts,
            "success_rate": (
                (len(self.request_history) - sum(self.error_counts.values())) /
                len(self.request_history) if self.request_history else 0
            )
        }

    def clear_history(self):
        """Clear request history"""
        self.request_history.clear()
        self.error_counts.clear()


if __name__ == "__main__":
    import asyncio

    async def test():
        client = HFClient()

        # Test single inference
        request = InferenceRequest(
            task_id="test-1",
            agent_id="gov-001",
            model="meta-llama/Llama-2-70b-chat",
            prompt="Generate a Python function to validate email addresses"
        )

        response = await client.infer(request)
        print(f"Response: {response}")

        # Test batch inference
        requests = [
            InferenceRequest(
                task_id=f"test-{i}",
                agent_id=f"worker-{i:03d}",
                model="meta-llama/Llama-2-70b-chat",
                prompt=f"Task {i}: Generate code"
            )
            for i in range(3)
        ]

        responses = await client.batch_infer(requests)
        print(f"\nBatch responses: {len(responses)} completed")
        for resp in responses:
            print(f"  - {resp.task_id}: {resp.status}")

    asyncio.run(test())
