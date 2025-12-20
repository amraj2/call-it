# Quick Start: Adding a New Workflow

This is a condensed version. See `WORKFLOW_GUIDE.md` for detailed instructions.

## 7 Steps to Add a Workflow

### 1. Create Activity
**File:** `temporal/activities/your_domain/your_activity.py`
```python
from temporalio import activity

@activity.defn
async def your_activity(param: str) -> str:
    return f"Result: {param}"
```

### 2. Register Activity
**File:** `temporal/activities/__init__.py`
```python
from temporal.activities.your_domain.your_activity import your_activity
ACTIVITIES = [..., your_activity]
```

### 3. Create Workflow
**File:** `temporal/workflows/your_domain/your_workflow.py`
```python
from temporalio import workflow
from temporal.workflow_metadata import register_workflow_metadata

@workflow.defn(sandboxed=False)
class YourWorkflow:
    @workflow.run
    async def run(self, param: str) -> str:
        result = await workflow.execute_activity(
            "your_activity", param,
            start_to_close_timeout=get_default_activity_timeout(),
            retry_policy=get_default_retry_policy(),
        )
        return result

register_workflow_metadata(
    workflow_id="your_workflow",
    name="Your Workflow",
    description="Description",
    workflow_class=YourWorkflow,
    parameters=[{
        "name": "param",
        "type": "string",
        "label": "Parameter",
        "default": "",
        "required": True,
    }],
    category="your_category",
)
```

### 4. Register Workflow
**File:** `temporal/workflows/__init__.py`
```python
from temporal.workflows.your_domain.your_workflow import YourWorkflow
WORKFLOWS = [..., YourWorkflow]
```

### 5. Add Flask Route
**File:** `app/routes/main.py`
```python
@bp.route('/workflows/your_workflow')
def your_workflow():
    from temporal.workflows import WORKFLOWS  # noqa: F401
    from temporal.workflow_metadata import get_workflow_metadata
    workflow_meta = get_workflow_metadata('your_workflow')
    return render_template('workflows/your_workflow.html', workflow=workflow_meta)
```

### 6. Create Template
**File:** `app/templates/workflows/your_workflow.html`
Copy from `app/templates/workflows/test.html` and modify:
- Change form ID to `yourWorkflowForm`
- Change API endpoint to `/api/workflows/your_workflow/run`
- Update button text

### 7. Update Index (Optional)
**File:** `app/templates/index.html`
Add link for dedicated page:
```html
{% if workflow.id == 'your_workflow' %}
<div class="workflow-actions">
    <a href="{{ url_for('main.your_workflow') }}" class="view-workflow-btn">
        View & Run Workflow →
    </a>
</div>
{% endif %}
```

## Testing

1. Restart Flask app
2. Visit http://localhost:8000/workflows/your_workflow
3. Fill form and run workflow
4. Check result

## Common Issues

- **Workflow not appearing**: Ensure registered in `__init__.py` files
- **Import errors**: Check all imports are correct
- **Activity not found**: Verify activity name matches string reference
- **Page 404**: Check route is added and Flask restarted

