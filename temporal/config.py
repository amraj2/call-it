"""Temporal configuration."""

import os
from typing import Optional


class TemporalConfig:
    """Temporal server configuration."""

    # Server connection
    ADDRESS: str = os.environ.get('TEMPORAL_ADDRESS', 'localhost:7233')
    NAMESPACE: str = os.environ.get('TEMPORAL_NAMESPACE', 'default')

    # Task queues
    DEFAULT_TASK_QUEUE: str = os.environ.get(
        'TEMPORAL_TASK_QUEUE',
        'test-task-queue'
    )

    # Worker configuration
    # Note: These are kept for future use if needed
    # The Worker class handles concurrency automatically

    # Retry configuration
    DEFAULT_RETRY_MAX_ATTEMPTS: int = 3
    DEFAULT_ACTIVITY_TIMEOUT_SECONDS: int = 30
    DEFAULT_WORKFLOW_TIMEOUT_SECONDS: int = 300


# Global config instance
config = TemporalConfig()

