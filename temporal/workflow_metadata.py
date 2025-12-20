"""Workflow metadata for UI display and execution."""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from temporal.registry import get_all_workflows


@dataclass
class WorkflowMetadata:
    """Metadata for a workflow."""

    id: str
    name: str
    description: str
    workflow_class: type
    parameters: List[Dict[str, Any]]
    category: str = "general"


# Registry of workflow metadata
WORKFLOW_METADATA: Dict[str, WorkflowMetadata] = {}


def register_workflow_metadata(
    workflow_id: str,
    name: str,
    description: str,
    workflow_class: type,
    parameters: Optional[List[Dict[str, Any]]] = None,
    category: str = "general",
) -> None:
    """Register metadata for a workflow.

    Args:
        workflow_id: Unique identifier for the workflow
        name: Display name
        description: Description of what the workflow does
        workflow_class: The workflow class
        parameters: List of parameter definitions
        category: Category/domain of the workflow
    """
    WORKFLOW_METADATA[workflow_id] = WorkflowMetadata(
        id=workflow_id,
        name=name,
        description=description,
        workflow_class=workflow_class,
        parameters=parameters or [],
        category=category,
    )


def get_all_workflow_metadata() -> List[WorkflowMetadata]:
    """Get metadata for all registered workflows.

    Returns:
        List of workflow metadata
    """
    return list(WORKFLOW_METADATA.values())


def get_workflow_metadata(workflow_id: str) -> Optional[WorkflowMetadata]:
    """Get metadata for a specific workflow.

    Args:
        workflow_id: Workflow identifier

    Returns:
        Workflow metadata or None if not found
    """
    return WORKFLOW_METADATA.get(workflow_id)

