"""Test workflow for Temporal."""

from datetime import timedelta
from temporalio import workflow
from temporal.shared import get_default_retry_policy, get_default_activity_timeout
from temporal.workflow_metadata import register_workflow_metadata


@workflow.defn(sandboxed=False)
class TestWorkflow:
    """A simple test workflow for Temporal."""

    @workflow.run
    async def run(self, name: str = "World") -> str:
        """Run the test workflow.

        Args:
            name: Name to greet (default: "World")

        Returns:
            A greeting message
        """
        # Execute activity using string reference to avoid sandbox restrictions
        result = await workflow.execute_activity(
            "test_activity",
            name,
            start_to_close_timeout=get_default_activity_timeout(),
            retry_policy=get_default_retry_policy(),
        )

        return result


# Register workflow metadata
register_workflow_metadata(
    workflow_id="test",
    name="Test Workflow",
    description="A simple test workflow that greets a user",
    workflow_class=TestWorkflow,
    parameters=[
        {
            "name": "name",
            "type": "string",
            "label": "Your Name",
            "default": "World",
            "required": False,
            "description": "Name to greet",
        }
    ],
    category="testing",
)
