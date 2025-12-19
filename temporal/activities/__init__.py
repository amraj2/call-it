"""Activities package - auto-registers all activities."""

from temporal.activities.test import test_activity

# Import all activities here for auto-registration
# As the project grows, organize activities by domain:
# from temporal.activities.automation import provision_server
# from temporal.activities.deployment import deploy_application
# etc.

__all__ = ['test_activity']

# List of all activities for worker registration
ACTIVITIES = [
    test_activity,
]

