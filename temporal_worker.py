"""Temporal worker that executes workflows and activities."""

import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from test_workflow import TestWorkflow
from test_activities import test_activity


async def main():
    """Start the Temporal worker."""
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")
    
    # Create a worker that listens on the "test-task-queue" task queue
    worker = Worker(
        client,
        task_queue="test-task-queue",
        workflows=[TestWorkflow],
        activities=[test_activity],
    )
    
    print("🚀 Temporal worker started. Listening for workflows...")
    print("   Task Queue: test-task-queue")
    print("   Server: localhost:7233")
    print("   ⚠️  Sandbox disabled for TestWorkflow (development only)")
    print("\nPress Ctrl+C to stop the worker.\n")
    
    # Run the worker
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

