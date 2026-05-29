"""
HuggingFace Integration Module
Inference client, agent runtime, and intelligent routing for the 500-agent swarm
"""

from .hf_client import HFClient, InferenceRequest, InferenceResponse
from .agent_runtime import AgentRuntime, AgentContext, AgentAction
from .inference_router import InferenceRouter, EndpointType, RouteStrategy, EndpointHealth

__all__ = [
    "HFClient",
    "InferenceRequest",
    "InferenceResponse",
    "AgentRuntime",
    "AgentContext",
    "AgentAction",
    "InferenceRouter",
    "EndpointType",
    "RouteStrategy",
    "EndpointHealth",
]

__version__ = "0.1.0"
