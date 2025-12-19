"""Temporal client for starting workflows."""

import asyncio
import time
from temporalio.client import Client
from temporalio.service import RPCError
from temporal.config import config
from temporal.workflows.test import TestWorkflow


async def start_test_workflow(name: str = "World") -> str:
    """Start a test workflow.

    Args:
        name: Name to greet (default: "World")

    Returns:
        Workflow result message
    """
    try:
        # Connect to Temporal server
        client = await Client.connect(
            config.ADDRESS,
            namespace=config.NAMESPACE
        )

        # Generate unique workflow ID
        workflow_id = f"test-workflow-{int(time.time() * 1000)}"

        # Start the workflow
        handle = await client.start_workflow(
            TestWorkflow.run,
            name,
            id=workflow_id,
            task_queue=config.DEFAULT_TASK_QUEUE,
        )

        # Wait for the result
        result = await handle.result()

        return result
    except RPCError as e:
        raise Exception(f"Failed to connect to Temporal server: {e}")
    except Exception as e:
        raise Exception(f"Failed to start workflow: {e}")
