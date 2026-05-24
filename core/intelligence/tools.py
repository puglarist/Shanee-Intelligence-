"""Tool Registry and Execution - Extensible function/tool system"""

import inspect
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Any, Callable, Optional
from enum import Enum

from pydantic import BaseModel, Field


class ToolStatus(str, Enum):
    """Tool execution status"""
    AVAILABLE = "available"
    DEPRECATED = "deprecated"
    EXPERIMENTAL = "experimental"
    DISABLED = "disabled"


@dataclass
class ToolParameter:
    """Parameter schema for a tool"""
    name: str
    type: str
    description: str = ""
    required: bool = True
    default: Any = None
    enum: Optional[list[str]] = None


@dataclass
class ToolSchema:
    """Schema definition for a tool"""
    id: str
    name: str
    description: str
    version: str = "1.0.0"
    parameters: list[ToolParameter] = None
    returns: dict[str, Any] = None
    tags: list[str] = None
    status: ToolStatus = ToolStatus.AVAILABLE

    def __post_init__(self):
        if self.parameters is None:
            self.parameters = []
        if self.returns is None:
            self.returns = {}
        if self.tags is None:
            self.tags = []

    def to_claude_format(self) -> dict:
        """Convert to Claude API tool format"""
        properties = {}
        required = []

        for param in self.parameters:
            properties[param.name] = {
                "type": param.type,
                "description": param.description,
            }
            if param.enum:
                properties[param.name]["enum"] = param.enum
            if param.required:
                required.append(param.name)

        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": properties,
                "required": required,
            }
        }


class Tool(ABC):
    """Base class for tools"""

    def __init__(self, schema: ToolSchema):
        self.schema = schema

    @abstractmethod
    async def execute(self, **kwargs) -> dict[str, Any]:
        """Execute tool with given parameters"""
        pass

    async def validate_input(self, **kwargs) -> bool:
        """Validate input parameters"""
        required_params = {p.name for p in self.schema.parameters if p.required}
        provided_params = set(kwargs.keys())
        return required_params.issubset(provided_params)


class SimpleTool(Tool):
    """Tool that wraps a simple async function"""

    def __init__(self, schema: ToolSchema, func: Callable):
        super().__init__(schema)
        self.func = func

    async def execute(self, **kwargs) -> dict[str, Any]:
        """Execute wrapped function"""
        try:
            result = await self.func(**kwargs) if inspect.iscoroutinefunction(self.func) else self.func(**kwargs)
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "error": str(e)}


class ToolRegistry:
    """
    Central registry of available tools.
    Manages discovery, versioning, and execution.
    """

    def __init__(self):
        self.tools: dict[str, Tool] = {}
        self.schemas: dict[str, ToolSchema] = {}

    def register(self, tool: Tool):
        """Register a tool"""
        tool_id = tool.schema.id
        self.tools[tool_id] = tool
        self.schemas[tool_id] = tool.schema

    def register_function(
        self,
        name: str,
        description: str,
        func: Callable,
        parameters: list[ToolParameter] = None,
        version: str = "1.0.0"
    ):
        """Register a simple function as a tool"""
        schema = ToolSchema(
            id=f"tool.{name}",
            name=name,
            description=description,
            version=version,
            parameters=parameters or []
        )
        tool = SimpleTool(schema, func)
        self.register(tool)

    def get(self, tool_id: str) -> Optional[Tool]:
        """Get tool by ID"""
        return self.tools.get(tool_id)

    def get_schema(self, tool_id: str) -> Optional[ToolSchema]:
        """Get schema by ID"""
        return self.schemas.get(tool_id)

    async def execute(self, tool_id: str, **kwargs) -> dict[str, Any]:
        """Execute tool by ID"""
        tool = self.get(tool_id)
        if not tool:
            return {"status": "error", "error": f"Tool not found: {tool_id}"}

        if not await tool.validate_input(**kwargs):
            return {"status": "error", "error": "Invalid input parameters"}

        return await tool.execute(**kwargs)

    def list(self, status: Optional[ToolStatus] = None) -> list[ToolSchema]:
        """List available tools"""
        schemas = list(self.schemas.values())
        if status:
            schemas = [s for s in schemas if s.status == status]
        return schemas

    def to_claude_format(self) -> list[dict]:
        """Get all tools in Claude API format"""
        return [
            schema.to_claude_format()
            for schema in self.list(status=ToolStatus.AVAILABLE)
        ]

    def search(self, query: str) -> list[ToolSchema]:
        """Search tools by name or description"""
        query_lower = query.lower()
        results = []
        for schema in self.schemas.values():
            if (query_lower in schema.name.lower() or
                query_lower in schema.description.lower() or
                any(query_lower in tag for tag in schema.tags)):
                results.append(schema)
        return results
