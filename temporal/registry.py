"""Workflow and activity registry for auto-discovery."""

from typing import List, Type, Any


def get_all_workflows() -> List[Type]:
    """Get all registered workflows.

    Returns:
        List of workflow classes
    """
    from temporal.workflows import WORKFLOWS
    return WORKFLOWS


def get_all_activities() -> List:
    """Get all registered activities.

    Returns:
        List of activity functions
    """
    from temporal.activities import ACTIVITIES
    return ACTIVITIES


def register_workflow(workflow_class: Type) -> None:
    """Register a workflow class.

    Args:
        workflow_class: Workflow class to register
    """
    from temporal.workflows import WORKFLOWS
    if workflow_class not in WORKFLOWS:
        WORKFLOWS.append(workflow_class)


def register_activity(activity_func) -> None:
    """Register an activity function.

    Args:
        activity_func: Activity function to register
    """
    from temporal.activities import ACTIVITIES
    if activity_func not in ACTIVITIES:
        ACTIVITIES.append(activity_func)

