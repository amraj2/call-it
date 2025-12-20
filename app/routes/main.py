"""Main routes blueprint."""

from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Render the main page with all available workflows."""
    # Import workflows to ensure metadata is registered
    from temporal.workflows import WORKFLOWS  # noqa: F401
    
    # Get all workflow metadata
    from temporal.workflow_metadata import get_all_workflow_metadata

    workflows = get_all_workflow_metadata()
    
    # Group workflows by category
    workflows_by_category = {}
    for workflow in workflows:
        category = workflow.category or "general"
        if category not in workflows_by_category:
            workflows_by_category[category] = []
        workflows_by_category[category].append(workflow)

    return render_template(
        'index.html',
        workflows=workflows,
        workflows_by_category=workflows_by_category,
    )


@bp.route('/workflows/test')
def test_workflow():
    """Render the test workflow page."""
    # Import workflows to ensure metadata is registered
    from temporal.workflows import WORKFLOWS  # noqa: F401
    
    # Get test workflow metadata
    from temporal.workflow_metadata import get_workflow_metadata
    
    workflow_meta = get_workflow_metadata('test')
    
    return render_template(
        'workflows/test.html',
        workflow=workflow_meta,
    )
