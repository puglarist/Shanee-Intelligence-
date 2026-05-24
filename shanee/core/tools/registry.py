"""Tool registry and management."""

from typing import Any, Callable, Dict, List, Optional
from enum import Enum
from datetime import datetime

from pydantic import BaseModel


class ToolPermission(str, Enum):
    """Tool permission levels."""
    PUBLIC = "public"
    RESTRICTED = "restricted"
    PRIVATE = "private"


class ToolMetadata(BaseModel):
    """Tool metadata."""
    name: str
    version: str
    description: str
    author: str
    permission: ToolPermission = ToolPermission.PUBLIC
    tags: List[str] = []
    enabled: bool = True
    created_at: datetime = None
    updated_at: datetime = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()


class Tool:
    """Core Tool class."""

    def __init__(self, metadata: ToolMetadata, func: Callable):
        self.metadata = metadata
        self.func = func
        self.execution_count = 0
        self.last_executed = None

    async def execute(self, *args, **kwargs) -> Any:
        """Execute the tool."""
        if not self.metadata.enabled:
            raise RuntimeError(f"Tool {self.metadata.name} is disabled")

        self.execution_count += 1
        self.last_executed = datetime.utcnow()
        return await self.func(*args, **kwargs) if hasattr(self.func, '__await__') else self.func(*args, **kwargs)


class ToolRegistry:
    """Registry for managing tools."""

    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self.categories: Dict[str, List[str]] = {}

    def register_tool(self, metadata: ToolMetadata, func: Callable) -> Tool:
        """Register a new tool."""
        tool = Tool(metadata, func)
        self.tools[metadata.name] = tool

        for tag in metadata.tags:
            if tag not in self.categories:
                self.categories[tag] = []
            self.categories[tag].append(metadata.name)

        return tool

    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        return self.tools.get(name)

    def list_tools(self, category: Optional[str] = None,
                   enabled_only: bool = False) -> List[Tool]:
        """List all tools, optionally filtered."""
        tools = list(self.tools.values())

        if category:
            tool_names = self.categories.get(category, [])
            tools = [self.tools[name] for name in tool_names if name in self.tools]

        if enabled_only:
            tools = [t for t in tools if t.metadata.enabled]

        return tools

    def enable_tool(self, name: str) -> bool:
        """Enable a tool."""
        tool = self.tools.get(name)
        if tool:
            tool.metadata.enabled = True
            tool.metadata.updated_at = datetime.utcnow()
            return True
        return False

    def disable_tool(self, name: str) -> bool:
        """Disable a tool."""
        tool = self.tools.get(name)
        if tool:
            tool.metadata.enabled = False
            tool.metadata.updated_at = datetime.utcnow()
            return True
        return False

    def get_tool_stats(self, name: str) -> Optional[Dict[str, Any]]:
        """Get execution statistics for a tool."""
        tool = self.tools.get(name)
        if not tool:
            return None

        return {
            "name": tool.metadata.name,
            "execution_count": tool.execution_count,
            "last_executed": tool.last_executed,
            "enabled": tool.metadata.enabled,
            "version": tool.metadata.version
        }
