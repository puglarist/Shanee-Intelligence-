"""Tool management endpoints."""

from typing import Optional

from fastapi import APIRouter, HTTPException

from shanee.core.tools import ToolRegistry

router = APIRouter(prefix="/tools", tags=["tools"])
registry = ToolRegistry()


@router.get("")
async def list_tools(category: Optional[str] = None, enabled_only: bool = False):
    """List all tools."""
    tools = registry.list_tools(category, enabled_only)
    return [
        {
            "name": t.metadata.name,
            "version": t.metadata.version,
            "description": t.metadata.description,
            "permission": t.metadata.permission,
            "enabled": t.metadata.enabled,
            "tags": t.metadata.tags
        }
        for t in tools
    ]


@router.get("/{tool_name}")
async def get_tool(tool_name: str):
    """Get tool details."""
    tool = registry.get_tool(tool_name)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    return {
        "name": tool.metadata.name,
        "version": tool.metadata.version,
        "description": tool.metadata.description,
        "permission": tool.metadata.permission,
        "enabled": tool.metadata.enabled,
        "tags": tool.metadata.tags,
        "stats": registry.get_tool_stats(tool_name)
    }


@router.post("/{tool_name}/enable", status_code=204)
async def enable_tool(tool_name: str):
    """Enable a tool."""
    if not registry.enable_tool(tool_name):
        raise HTTPException(status_code=404, detail="Tool not found")
    return None


@router.post("/{tool_name}/disable", status_code=204)
async def disable_tool(tool_name: str):
    """Disable a tool."""
    if not registry.disable_tool(tool_name):
        raise HTTPException(status_code=404, detail="Tool not found")
    return None
