"""
Template for creating a new Temporal workflow.

Copy this file and modify it to create your own workflow.
Replace all instances of:
- YOUR_WORKFLOW -> Your workflow name
- your_workflow -> your workflow ID (lowercase, underscores)
- YourWorkflow -> Your workflow class name (PascalCase)
- your_activity -> Your activity name
- your_category -> Your category name
"""

# ============================================================================
# STEP 1: Create Activity
# File: temporal/activities/your_domain/your_activity.py
# ============================================================================

"""
import asyncio
from temporalio import activity


@activity.defn
async def your_activity(param1: str, param2: int = 10) -> str:
    \"\"\"Your activity description.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (default: 10)
        
    Returns:
        Result description
    \"\"\"
    # Your activity implementation
    await asyncio.sleep(1)  # Simulate work
    
    return f"Activity completed with {param1} and {param2}"
"""

# ============================================================================
# STEP 2: Register Activity
# File: temporal/activities/__init__.py
# ============================================================================

"""
from temporal.activities.your_domain.your_activity import your_activity

ACTIVITIES = [
    # ... existing activities ...
    your_activity,  # Add this line
]
"""

# ============================================================================
# STEP 3: Create Workflow
# File: temporal/workflows/your_domain/your_workflow.py
# ============================================================================

"""
from temporalio import workflow
from temporal.shared import (
    get_default_retry_policy,
    get_default_activity_timeout,
)
from temporal.workflow_metadata import register_workflow_metadata


@workflow.defn(sandboxed=False)
class YourWorkflow:
    \"\"\"Your workflow description.\"\"\"

    @workflow.run
    async def run(self, param1: str, param2: int = 10) -> str:
        \"\"\"Run the workflow.

        Args:
            param1: Description of param1
            param2: Description of param2 (default: 10)

        Returns:
            Result description
        \"\"\"
        # Execute activity using string reference
        result = await workflow.execute_activity(
            "your_activity",
            param1,
            param2,
            start_to_close_timeout=get_default_activity_timeout(),
            retry_policy=get_default_retry_policy(),
        )

        return result


# Register workflow metadata
register_workflow_metadata(
    workflow_id="your_workflow",
    name="Your Workflow Name",
    description="A description of what your workflow does",
    workflow_class=YourWorkflow,
    parameters=[
        {
            "name": "param1",
            "type": "string",
            "label": "Parameter 1",
            "default": "",
            "required": True,
            "description": "Description of parameter 1",
        },
        {
            "name": "param2",
            "type": "number",
            "label": "Parameter 2",
            "default": 10,
            "required": False,
            "description": "Description of parameter 2",
        },
    ],
    category="your_category",
)
"""

# ============================================================================
# STEP 4: Register Workflow
# File: temporal/workflows/__init__.py
# ============================================================================

"""
from temporal.workflows.your_domain.your_workflow import YourWorkflow

WORKFLOWS = [
    # ... existing workflows ...
    YourWorkflow,  # Add this line
]
"""

# ============================================================================
# STEP 5: Add Flask Route
# File: app/routes/main.py
# ============================================================================

"""
@bp.route('/workflows/your_workflow')
def your_workflow():
    \"\"\"Render the your workflow page.\"\"\"
    from temporal.workflows import WORKFLOWS  # noqa: F401
    from temporal.workflow_metadata import get_workflow_metadata
    
    workflow_meta = get_workflow_metadata('your_workflow')
    
    return render_template(
        'workflows/your_workflow.html',
        workflow=workflow_meta,
    )
"""

# ============================================================================
# STEP 6: Create HTML Template
# File: app/templates/workflows/your_workflow.html
# ============================================================================

"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Workflow - Temporal</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container">
        <div class="breadcrumb">
            <a href="{{ url_for('main.index') }}">← Back to Workflows</a>
        </div>
        
        <h1>🚀 Your Workflow Name</h1>
        <p class="subtitle">{{ workflow.description if workflow else 'Description' }}</p>

        <div class="workflow-details">
            <div class="workflow-info">
                <h2>Workflow Information</h2>
                <p><strong>Description:</strong> {{ workflow.description if workflow else 'Description' }}</p>
                <p><strong>Category:</strong> {{ workflow.category if workflow else 'general' }}</p>
            </div>

            <form id="yourWorkflowForm" class="workflow-form">
                {% if workflow and workflow.parameters %}
                    {% for param in workflow.parameters %}
                    <div class="form-group">
                        <label for="{{ param.name }}">
                            {{ param.label or param.name }}:
                            {% if param.required %}<span class="required">*</span>{% endif %}
                        </label>
                        <input
                            type="{{ param.type }}"
                            id="{{ param.name }}"
                            name="{{ param.name }}"
                            value="{{ param.default or '' }}"
                            placeholder="{{ param.description or param.name }}"
                            {% if param.required %}required{% endif %}
                        >
                        {% if param.description %}
                        <small class="param-description">{{ param.description }}</small>
                        {% endif %}
                    </div>
                    {% endfor %}
                {% endif %}
                
                <button type="submit" id="submitBtn" class="run-workflow-btn">
                    Run Your Workflow
                </button>
            </form>

            <div class="loading" id="loading" style="display: none;">⏳ Running workflow...</div>
            <div class="result" id="result"></div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const form = document.getElementById('yourWorkflowForm');
            const submitBtn = document.getElementById('submitBtn');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');

            form.addEventListener('submit', async function(e) {
                e.preventDefault();
                const formData = new FormData(form);
                const params = {};
                for (const [key, value] of formData.entries()) {
                    if (value.trim() !== '') params[key] = value.trim();
                }
                
                submitBtn.disabled = true;
                submitBtn.textContent = 'Running...';
                loading.style.display = 'block';
                result.className = 'result';
                result.style.display = 'none';

                try {
                    const response = await fetch('/api/workflows/your_workflow/run', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(params)
                    });
                    const data = await response.json();

                    if (response.ok) {
                        result.className = 'result success';
                        result.innerHTML = `<strong>✅ Success!</strong><br><div style="margin-top: 8px;">${escapeHtml(String(data.result))}</div>${data.workflow_id ? `<small style="display: block; margin-top: 8px; opacity: 0.7;">Workflow ID: ${data.workflow_id}</small>` : ''}`;
                    } else {
                        result.className = 'result error';
                        result.innerHTML = `<strong>❌ Error:</strong><br><div style="margin-top: 8px;">${escapeHtml(data.error || 'Unknown error')}</div>`;
                    }
                    result.style.display = 'block';
                } catch (error) {
                    result.className = 'result error';
                    result.innerHTML = `<strong>❌ Error:</strong><br><div style="margin-top: 8px;">${escapeHtml(error.message)}</div>`;
                    result.style.display = 'block';
                } finally {
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Run Your Workflow';
                    loading.style.display = 'none';
                }
            });
        });

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    </script>
</body>
</html>
"""

# ============================================================================
# STEP 7: Update Index (Optional)
# File: app/templates/index.html
# ============================================================================

"""
{% if workflow.id == 'your_workflow' %}
<div class="workflow-actions">
    <a href="{{ url_for('main.your_workflow') }}" class="view-workflow-btn">
        View & Run Workflow →
    </a>
</div>
{% else %}
<!-- Regular inline form -->
{% endif %}
"""

