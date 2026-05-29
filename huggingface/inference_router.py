"""
Inference Router
Routes inference requests to appropriate HF endpoints based on task type
Handles load balancing, fallbacks, and endpoint health
"""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import asyncio

from .hf_client import HFClient, InferenceRequest, InferenceResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EndpointType(Enum):
    """Types of HF endpoints"""
    CODE_GENERATION = "code-generation"
    TEXT_GENERATION = "text-generation"
    ANALYSIS = "analysis"
    DEBUGGING = "debugging"
    TESTING = "testing"
    REVIEW = "review"


@dataclass
class EndpointHealth:
    """Health metrics for an endpoint"""
    endpoint_type: EndpointType
    url: str
    success_count: int = 0
    error_count: int = 0
    avg_latency: float = 0.0
    last_check: str = ""
    is_healthy: bool = True
    last_error: Optional[str] = None

    def get_success_rate(self) -> float:
        """Get success rate for this endpoint"""
        total = self.success_count + self.error_count
        return (self.success_count / total * 100) if total > 0 else 0.0

    def update_metrics(self, success: bool, latency: float):
        """Update endpoint metrics"""
        if success:
            self.success_count += 1
        else:
            self.error_count += 1

        # Update average latency (exponential moving average)
        if self.avg_latency == 0:
            self.avg_latency = latency
        else:
            self.avg_latency = (self.avg_latency * 0.7) + (latency * 0.3)

        self.last_check = datetime.utcnow().isoformat()


@dataclass
class RouteStrategy:
    """Strategy for routing a specific task type"""
    task_type: str
    preferred_endpoint: EndpointType
    fallback_endpoints: List[EndpointType] = field(default_factory=list)
    model: str = "meta-llama/Llama-2-70b-chat"
    temperature: float = 0.7
    max_tokens: int = 2048


class InferenceRouter:
    """
    Routes inference requests to appropriate endpoints
    Handles: task classification, endpoint selection, load balancing, health monitoring
    """

    def __init__(self, hf_client: HFClient = None):
        self.hf_client = hf_client or HFClient()
        self.endpoints: Dict[EndpointType, EndpointHealth] = {}
        self.routes: Dict[str, RouteStrategy] = {}
        self.request_queue: List[InferenceRequest] = []
        self.load_tracking: Dict[EndpointType, int] = {}

        self._initialize_endpoints()
        self._initialize_routes()

    def _initialize_endpoints(self):
        """Initialize endpoint health tracking"""
        endpoint_configs = {
            EndpointType.CODE_GENERATION: "https://api-inference.huggingface.co/models/bigcode/starcoder",
            EndpointType.TEXT_GENERATION: "https://api-inference.huggingface.co/models/meta-llama/Llama-2-70b-chat",
            EndpointType.ANALYSIS: "https://api-inference.huggingface.co/models/meta-llama/Llama-2-70b-chat",
            EndpointType.DEBUGGING: "https://api-inference.huggingface.co/models/bigcode/starcoder",
            EndpointType.TESTING: "https://api-inference.huggingface.co/models/meta-llama/Llama-2-70b-chat",
            EndpointType.REVIEW: "https://api-inference.huggingface.co/models/meta-llama/Llama-2-70b-chat",
        }

        for endpoint_type, url in endpoint_configs.items():
            self.endpoints[endpoint_type] = EndpointHealth(
                endpoint_type=endpoint_type,
                url=url
            )
            self.load_tracking[endpoint_type] = 0

    def _initialize_routes(self):
        """Initialize routing strategies for task types"""
        self.routes = {
            "code_generation": RouteStrategy(
                task_type="code_generation",
                preferred_endpoint=EndpointType.CODE_GENERATION,
                fallback_endpoints=[EndpointType.TEXT_GENERATION],
                model="bigcode/starcoder",
                temperature=0.3,
                max_tokens=4096
            ),
            "debugging": RouteStrategy(
                task_type="debugging",
                preferred_endpoint=EndpointType.DEBUGGING,
                fallback_endpoints=[EndpointType.ANALYSIS, EndpointType.TEXT_GENERATION],
                temperature=0.5,
                max_tokens=2048
            ),
            "testing": RouteStrategy(
                task_type="testing",
                preferred_endpoint=EndpointType.TESTING,
                fallback_endpoints=[EndpointType.TEXT_GENERATION],
                temperature=0.2,
                max_tokens=2048
            ),
            "review": RouteStrategy(
                task_type="review",
                preferred_endpoint=EndpointType.REVIEW,
                fallback_endpoints=[EndpointType.ANALYSIS, EndpointType.TEXT_GENERATION],
                temperature=0.3,
                max_tokens=1024
            ),
            "analysis": RouteStrategy(
                task_type="analysis",
                preferred_endpoint=EndpointType.ANALYSIS,
                fallback_endpoints=[EndpointType.TEXT_GENERATION],
                temperature=0.5,
                max_tokens=2048
            ),
            "documentation": RouteStrategy(
                task_type="documentation",
                preferred_endpoint=EndpointType.TEXT_GENERATION,
                fallback_endpoints=[EndpointType.ANALYSIS],
                temperature=0.5,
                max_tokens=2048
            ),
        }

    def route_request(
        self,
        task_id: str,
        agent_id: str,
        task_type: str,
        prompt: str
    ) -> Tuple[InferenceRequest, EndpointType]:
        """
        Route a request to appropriate endpoint
        Returns: (InferenceRequest, selected EndpointType)
        """
        strategy = self.routes.get(task_type, self._get_default_strategy(task_type))

        # Select endpoint (prefer healthy, less loaded endpoints)
        endpoint_type = self._select_endpoint(
            strategy.preferred_endpoint,
            strategy.fallback_endpoints
        )

        # Create inference request
        request = InferenceRequest(
            task_id=task_id,
            agent_id=agent_id,
            model=strategy.model,
            prompt=prompt,
            temperature=strategy.temperature,
            max_tokens=strategy.max_tokens
        )

        # Track load
        self.load_tracking[endpoint_type] = self.load_tracking.get(endpoint_type, 0) + 1

        logger.info(f"Routed {task_type} to {endpoint_type.value}")

        return request, endpoint_type

    async def execute_routed_request(
        self,
        task_id: str,
        agent_id: str,
        task_type: str,
        prompt: str
    ) -> InferenceResponse:
        """
        Execute a routed request and update endpoint health
        """
        request, endpoint_type = self.route_request(
            task_id, agent_id, task_type, prompt
        )

        try:
            response = await self.hf_client.infer(request, endpoint_type.value)

            # Update health metrics
            success = response.status == "success"
            self.endpoints[endpoint_type].update_metrics(
                success=success,
                latency=response.execution_time
            )

            return response

        finally:
            # Decrement load counter
            self.load_tracking[endpoint_type] = max(0, self.load_tracking.get(endpoint_type, 1) - 1)

    def _select_endpoint(
        self,
        preferred: EndpointType,
        fallbacks: List[EndpointType]
    ) -> EndpointType:
        """
        Select best endpoint considering: health, load, success rate
        """
        candidates = [preferred] + fallbacks

        # Filter healthy endpoints
        healthy = [
            ep for ep in candidates
            if self.endpoints[ep].is_healthy
        ]

        if not healthy:
            healthy = candidates  # Use all if none healthy

        # Sort by: load (ascending), success rate (descending)
        sorted_endpoints = sorted(
            healthy,
            key=lambda ep: (
                self.load_tracking.get(ep, 0),
                -self.endpoints[ep].get_success_rate()
            )
        )

        return sorted_endpoints[0]

    def _get_default_strategy(self, task_type: str) -> RouteStrategy:
        """Get default strategy for unknown task types"""
        return RouteStrategy(
            task_type=task_type,
            preferred_endpoint=EndpointType.TEXT_GENERATION,
            fallback_endpoints=[],
            temperature=0.5
        )

    def mark_endpoint_unhealthy(
        self,
        endpoint_type: EndpointType,
        error: str = None
    ):
        """Mark an endpoint as unhealthy"""
        health = self.endpoints.get(endpoint_type)
        if health:
            health.is_healthy = False
            health.last_error = error
            logger.warning(f"Marked {endpoint_type.value} as unhealthy: {error}")

    def mark_endpoint_healthy(self, endpoint_type: EndpointType):
        """Mark an endpoint as healthy again"""
        health = self.endpoints.get(endpoint_type)
        if health:
            health.is_healthy = True
            health.error_count = 0
            logger.info(f"Marked {endpoint_type.value} as healthy")

    def get_router_status(self) -> Dict:
        """Get current router status"""
        return {
            "endpoints": {
                ep.endpoint_type.value: {
                    "healthy": ep.is_healthy,
                    "success_rate": ep.get_success_rate(),
                    "avg_latency": round(ep.avg_latency, 3),
                    "current_load": self.load_tracking.get(ep.endpoint_type, 0),
                    "total_requests": ep.success_count + ep.error_count
                }
                for ep in self.endpoints.values()
            },
            "routes_configured": len(self.routes),
            "queue_size": len(self.request_queue)
        }

    def reset_metrics(self):
        """Reset all endpoint metrics"""
        for endpoint in self.endpoints.values():
            endpoint.success_count = 0
            endpoint.error_count = 0
            endpoint.avg_latency = 0.0
        self.load_tracking = {ep_type: 0 for ep_type in self.load_tracking}


if __name__ == "__main__":
    import asyncio

    async def test():
        router = InferenceRouter()

        # Test routing different task types
        test_tasks = [
            ("task-1", "agent-1", "code_generation", "Generate a Python function to sort a list"),
            ("task-2", "agent-2", "debugging", "Debug this Python error: IndexError at line 42"),
            ("task-3", "agent-3", "testing", "Write unit tests for user authentication"),
            ("task-4", "agent-4", "review", "Review this pull request for code quality"),
        ]

        print("Testing inference routing...\n")

        for task_id, agent_id, task_type, prompt in test_tasks:
            print(f"Routing: {task_type}")
            request, endpoint = router.route_request(task_id, agent_id, task_type, prompt)
            print(f"  Endpoint: {endpoint.value}\n")

        # Show router status
        status = router.get_router_status()
        print(f"Router Status: {status}")

    asyncio.run(test())
