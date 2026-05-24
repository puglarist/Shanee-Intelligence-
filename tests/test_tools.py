"""Tests for tool registry."""

import pytest

from shanee.core.tools import ToolRegistry, ToolMetadata, ToolPermission


def test_tool_registration():
    """Test tool registration."""
    registry = ToolRegistry()

    def dummy_tool(x):
        return x * 2

    metadata = ToolMetadata(
        name="double",
        version="1.0.0",
        description="Doubles a number",
        author="test"
    )

    tool = registry.register_tool(metadata, dummy_tool)
    assert tool.metadata.name == "double"
    assert registry.get_tool("double") == tool


def test_tool_execution():
    """Test tool execution."""
    registry = ToolRegistry()

    def add(a, b):
        return a + b

    metadata = ToolMetadata(
        name="add",
        version="1.0.0",
        description="Adds two numbers",
        author="test"
    )

    tool = registry.register_tool(metadata, add)

    import asyncio
    result = asyncio.run(tool.execute(2, 3))
    assert result == 5


def test_tool_categories():
    """Test tool categorization."""
    registry = ToolRegistry()

    def func1():
        pass

    def func2():
        pass

    metadata1 = ToolMetadata(
        name="math_add",
        version="1.0.0",
        description="",
        author="test",
        tags=["math", "arithmetic"]
    )
    metadata2 = ToolMetadata(
        name="math_sub",
        version="1.0.0",
        description="",
        author="test",
        tags=["math", "arithmetic"]
    )

    registry.register_tool(metadata1, func1)
    registry.register_tool(metadata2, func2)

    math_tools = registry.list_tools(category="math")
    assert len(math_tools) == 2


def test_tool_enable_disable():
    """Test enabling/disabling tools."""
    registry = ToolRegistry()

    def dummy():
        pass

    metadata = ToolMetadata(
        name="test",
        version="1.0.0",
        description="",
        author="test"
    )

    registry.register_tool(metadata, dummy)

    assert registry.disable_tool("test")
    tool = registry.get_tool("test")
    assert not tool.metadata.enabled

    assert registry.enable_tool("test")
    tool = registry.get_tool("test")
    assert tool.metadata.enabled


def test_tool_stats():
    """Test tool statistics."""
    registry = ToolRegistry()

    def dummy():
        pass

    metadata = ToolMetadata(
        name="test",
        version="1.0.0",
        description="",
        author="test"
    )

    registry.register_tool(metadata, dummy)
    stats = registry.get_tool_stats("test")

    assert stats["name"] == "test"
    assert stats["version"] == "1.0.0"
    assert stats["execution_count"] == 0
    assert stats["enabled"]
