# Guide: Creating a New Temporal Workflow

This guide walks you through creating a new Temporal workflow, registering it, and adding it to the Flask app with a dedicated page.

## Step-by-Step Instructions

### Step 1: Create the Activity

First, create the activity that your workflow will execute.

**File:** `temporal/activities/your_domain/your_activity.py`

```python
"""Your activity implementation."""

import asyncio
from temporalio import activity


@activity.defn
async def your_activity(param1: str, param2: int = 10) -> str:
    """Your activity description.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (default: 10)
        
    Returns:
        Result description
    """
    # Your activity implementation
    await asyncio.sleep(1)  # Simulate work
    
    return f"Activity completed with {param1} and {param2}"
```

**Important Notes:**
- Activities can do non-deterministic operations (I/O, network calls, etc.)
- Use `@activity.defn` decorator
- Activities run outside the workflow sandbox

### Step 2: Register the Activity

**File:** `temporal/activities/__init__.py`

Add your activity to the registry:

```python
"""Activities package - auto-registers all activities."""

from temporal.activities.test import test_activity
from temporal.activities.your_domain.your_activity import your_activity

__all__ = ['test_activity', 'your_activity']

# List of all activities for worker registration
ACTIVITIES = [
    test_activity,
    your_activity,  # Add your activity here
]
```

### Step 3: Create the Workflow

**File:** `temporal/workflows/your_domain/your_workflow.py`

```python
"""Your workflow implementation."""

from temporalio import workflow
from temporal.shared import (
    get_default_retry_policy,
    get_default_activity_timeout,
)
from temporal.workflow_metadata import register_workflow_metadata


@workflow.defn(sandboxed=False)
class YourWorkflow:
    """Your workflow description."""

    @workflow.run
    async def run(self, param1: str, param2: int = 10) -> str:
        """Run the workflow.

        Args:
            param1: Description of param1
            param2: Description of param2 (default: 10)

        Returns:
            Result description
        """
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
    category="your_category",  # e.g., "automation", "deployment", etc.
)
```

**Important Notes:**
- Use `@workflow.defn(sandboxed=False)` for development (or `sandboxed=True` for production)
- Use string references for activities (e.g., `"your_activity"`) to avoid sandbox issues
- Register metadata using `register_workflow_metadata()`

### Step 4: Register the Workflow

**File:** `temporal/workflows/__init__.py`

Add your workflow to the registry:

```python
"""Workflows package - auto-registers all workflows."""

from temporal.workflows.test import TestWorkflow
from temporal.workflows.your_domain.your_workflow import YourWorkflow

__all__ = ['TestWorkflow', 'YourWorkflow']

# List of all workflows for worker registration
WORKFLOWS = [
    TestWorkflow,
    YourWorkflow,  # Add your workflow here
]
```

### Step 5: Create Flask Route for Workflow Page

**File:** `app/routes/main.py`

Add a route for your workflow page:

```python
@bp.route('/workflows/your_workflow')
def your_workflow():
    """Render the your workflow page."""
    # Import workflows to ensure metadata is registered
    from temporal.workflows import WORKFLOWS  # noqa: F401
    
    # Get workflow metadata
    from temporal.workflow_metadata import get_workflow_metadata
    
    workflow_meta = get_workflow_metadata('your_workflow')
    
    return render_template(
        'workflows/your_workflow.html',
        workflow=workflow_meta,
    )
```

### Step 6: Create HTML Template

**File:** `app/templates/workflows/your_workflow.html`

```html
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
        <p class="subtitle">
            {{ workflow.description if workflow else 'Your workflow description' }}
        </p>

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

            <div class="loading" id="loading" style="display: none;">
                ⏳ Running workflow...
            </div>

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

                // Collect form data
                const formData = new FormData(form);
                const params = {};
                for (const [key, value] of formData.entries()) {
                    if (value.trim() !== '') {
                        params[key] = value.trim();
                    }
                }
                
                // Reset UI
                submitBtn.disabled = true;
                submitBtn.textContent = 'Running...';
                loading.style.display = 'block';
                result.className = 'result';
                result.style.display = 'none';
                result.innerHTML = '';

                try {
                    const response = await fetch('/api/workflows/your_workflow/run', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(params)
                    });

                    const data = await response.json();

                    if (response.ok) {
                        result.className = 'result success';
                        result.innerHTML = `
                            <strong>✅ Success!</strong><br>
                            <div style="margin-top: 8px;">${escapeHtml(String(data.result))}</div>
                            ${data.workflow_id ? `<small style="display: block; margin-top: 8px; opacity: 0.7;">Workflow ID: ${data.workflow_id}</small>` : ''}
                        `;
                    } else {
                        result.className = 'result error';
                        result.innerHTML = `
                            <strong>❌ Error:</strong><br>
                            <div style="margin-top: 8px;">${escapeHtml(data.error || 'Unknown error')}</div>
                        `;
                    }
                    result.style.display = 'block';
                } catch (error) {
                    result.className = 'result error';
                    result.innerHTML = `
                        <strong>❌ Error:</strong><br>
                        <div style="margin-top: 8px;">${escapeHtml(error.message)}</div>
                    `;
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
```

### Step 7: Update Index Page (Optional)

**File:** `app/templates/index.html`

If you want the workflow to have a dedicated page link (like the test workflow), update the index template:

```html
{% if workflow.id == 'your_workflow' %}
<div class="workflow-actions">
    <a href="{{ url_for('main.your_workflow') }}" class="view-workflow-btn">
        View & Run Workflow →
    </a>
</div>
{% else %}
<!-- Regular inline form -->
{% endif %}
```

## Complete Example: "Greeting Workflow"

Here's a complete example to follow:

### Activity: `temporal/activities/greeting/greet.py`

```python
"""Greeting activity."""

import asyncio
from temporalio import activity


@activity.defn
async def greet_activity(name: str, language: str = "en") -> str:
    """Greet a person in their preferred language.
    
    Args:
        name: Person's name
        language: Language code (default: "en")
        
    Returns:
        Greeting message
    """
    await asyncio.sleep(1)
    
    greetings = {
        "en": f"Hello, {name}!",
        "es": f"¡Hola, {name}!",
        "fr": f"Bonjour, {name}!",
    }
    
    return greetings.get(language, greetings["en"])
```

### Workflow: `temporal/workflows/greeting/greet_workflow.py`

```python
"""Greeting workflow."""

from temporalio import workflow
from temporal.shared import (
    get_default_retry_policy,
    get_default_activity_timeout,
)
from temporal.workflow_metadata import register_workflow_metadata


@workflow.defn(sandboxed=False)
class GreetWorkflow:
    """A workflow that greets a person."""

    @workflow.run
    async def run(self, name: str, language: str = "en") -> str:
        """Run the greeting workflow.

        Args:
            name: Person's name
            language: Language code (default: "en")

        Returns:
            Greeting message
        """
        result = await workflow.execute_activity(
            "greet_activity",
            name,
            language,
            start_to_close_timeout=get_default_activity_timeout(),
            retry_policy=get_default_retry_policy(),
        )

        return result


# Register workflow metadata
register_workflow_metadata(
    workflow_id="greet",
    name="Greeting Workflow",
    description="Greet a person in their preferred language",
    workflow_class=GreetWorkflow,
    parameters=[
        {
            "name": "name",
            "type": "string",
            "label": "Name",
            "default": "",
            "required": True,
            "description": "Person's name to greet",
        },
        {
            "name": "language",
            "type": "string",
            "label": "Language",
            "default": "en",
            "required": False,
            "description": "Language code (en, es, fr)",
        },
    ],
    category="examples",
)
```

## Parameter Types

Supported parameter types in metadata:
- `"string"` - Text input
- `"number"` - Number input
- `"integer"` - Integer input
- `"boolean"` - Checkbox
- `"email"` - Email input
- `"url"` - URL input

## Checklist

- [ ] Activity created in `temporal/activities/`
- [ ] Activity registered in `temporal/activities/__init__.py`
- [ ] Workflow created in `temporal/workflows/`
- [ ] Workflow metadata registered with `register_workflow_metadata()`
- [ ] Workflow registered in `temporal/workflows/__init__.py`
- [ ] Flask route added in `app/routes/main.py`
- [ ] HTML template created in `app/templates/workflows/`
- [ ] Index page updated (if using dedicated page)
- [ ] Test the workflow via Flask app
- [ ] Verify workflow appears in index page

## Testing Your Workflow

1. **Start all services:**
   ```bash
   ./start_all.sh
   ```

2. **Access the Flask app:**
   - Index: http://localhost:8000
   - Your workflow: http://localhost:8000/workflows/your_workflow

3. **Test execution:**
   - Fill in the form parameters
   - Click "Run Your Workflow"
   - Check the result

4. **Verify in Temporal UI:**
   - Open http://localhost:8088
   - Check "Workflows" tab to see your workflow executions

## Troubleshooting

**Workflow not appearing in index:**
- Ensure workflow metadata is registered
- Check that workflow is imported in `temporal/workflows/__init__.py`
- Restart Flask app

**Workflow execution fails:**
- Check worker logs: `tail -f worker.log`
- Verify activity is registered in `temporal/activities/__init__.py`
- Ensure activity name matches string reference in workflow

**Page not found:**
- Verify route is added to `app/routes/main.py`
- Check template exists in `app/templates/workflows/`
- Restart Flask app

## Best Practices

1. **Organize by domain**: Group related workflows/activities in subdirectories
2. **Use descriptive names**: Clear workflow and activity names
3. **Document parameters**: Always include descriptions in metadata
4. **Handle errors**: Activities should handle and report errors gracefully
5. **Use appropriate timeouts**: Set reasonable timeouts for activities
6. **Test thoroughly**: Test workflows before deploying

## Next Steps

Once your workflow is working:
- Add more complex logic
- Chain multiple activities
- Add error handling and retries
- Create workflows that call other workflows
- Add workflow versioning for production

