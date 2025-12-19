"""Test activities for Temporal workflows."""

import asyncio
from temporalio import activity


@activity.defn
async def test_activity(name: str) -> str:
    """A simple test activity that greets the user.

    Args:
        name: Name to greet

    Returns:
        A greeting message
    """
    # Simulate some work
    await asyncio.sleep(1)

    return f"Hello, {name}! This is a test workflow execution. ✅"

