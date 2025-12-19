"""Shared utilities and types for Temporal workflows."""

from datetime import timedelta
from temporalio.common import RetryPolicy

__all__ = ['get_default_retry_policy', 'get_default_activity_timeout']


def get_default_retry_policy(max_attempts: int = None) -> RetryPolicy:
    """Get default retry policy for activities.

    Args:
        max_attempts: Maximum retry attempts (defaults to config)

    Returns:
        RetryPolicy instance
    """
    from temporal.config import config

    return RetryPolicy(
        maximum_attempts=max_attempts or config.DEFAULT_RETRY_MAX_ATTEMPTS
    )


def get_default_activity_timeout() -> timedelta:
    """Get default activity timeout.

    Returns:
        timedelta for activity timeout
    """
    from temporal.config import config

    return timedelta(seconds=config.DEFAULT_ACTIVITY_TIMEOUT_SECONDS)

