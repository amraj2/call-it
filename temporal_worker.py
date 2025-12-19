"""Temporal worker that executes workflows and activities."""

import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from temporal.config import config
from temporal.registry import get_all_workflows, get_all_activities


async def main():
    """Start the Temporal worker."""
    # Connect to Temporal server
    client = await Client.connect(
        config.ADDRESS,
        namespace=config.NAMESPACE
    )

    # Get all registered workflows and activities
    workflows = get_all_workflows()
    activities = get_all_activities()

    # Create a worker that listens on the configured task queue
    worker = Worker(
        client,
        task_queue=config.DEFAULT_TASK_QUEUE,
        workflows=workflows,
        activities=activities,
    )

    print("🚀 Temporal worker started. Listening for workflows...")
    print(f"   Task Queue: {config.DEFAULT_TASK_QUEUE}")
    print(f"   Server: {config.ADDRESS}")
    print(f"   Namespace: {config.NAMESPACE}")
    print(f"   Workflows registered: {len(workflows)}")
    print(f"   Activities registered: {len(activities)}")
    print("\nPress Ctrl+C to stop the worker.\n")

    # Run the worker
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
