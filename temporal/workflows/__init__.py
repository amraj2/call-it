"""Workflows package - auto-registers all workflows."""

from temporal.workflows.test import TestWorkflow

# Import all workflows here for auto-registration
# As the project grows, organize workflows by domain:
# from temporal.workflows.automation import ServerProvisioningWorkflow
# from temporal.workflows.deployment import ApplicationDeploymentWorkflow
# etc.

__all__ = ['TestWorkflow']

# List of all workflows for worker registration
WORKFLOWS = [
    TestWorkflow,
]

