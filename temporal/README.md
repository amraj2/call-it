# Temporal Workflows Structure

This directory contains all Temporal workflows and activities, organized for scalability.

## Directory Structure

```
temporal/
├── __init__.py           # Package initialization
├── config.py             # Temporal configuration
├── registry.py           # Workflow/activity registration
├── workflows/            # All workflows
│   ├── __init__.py       # Workflow registry
│   ├── test.py           # Test workflow
│   └── [domain]/         # Domain-specific workflows (future)
│       └── *.py
├── activities/           # All activities
│   ├── __init__.py       # Activity registry
│   ├── test.py           # Test activities
│   └── [domain]/         # Domain-specific activities (future)
│       └── *.py
└── shared/               # Shared utilities
    ├── __init__.py       # Shared functions
    └── [utilities].py    # Common utilities
```

## Adding New Workflows

1. **Create workflow file** in `temporal/workflows/`:
   ```python
   # temporal/workflows/my_domain/my_workflow.py
   from temporalio import workflow
   from temporal.shared import get_default_retry_policy

   @workflow.defn(sandboxed=False)
   class MyWorkflow:
       @workflow.run
       async def run(self, input: str) -> str:
           result = await workflow.execute_activity(
               "my_activity",
               input,
               retry_policy=get_default_retry_policy(),
           )
           return result
   ```

2. **Create activity file** in `temporal/activities/`:
   ```python
   # temporal/activities/my_domain/my_activity.py
   from temporalio import activity

   @activity.defn
   async def my_activity(input: str) -> str:
       # Activity implementation
       return f"Processed: {input}"
   ```

3. **Register in `__init__.py`**:
   ```python
   # temporal/workflows/__init__.py
   from temporal.workflows.my_domain.my_workflow import MyWorkflow
   WORKFLOWS.append(MyWorkflow)

   # temporal/activities/__init__.py
   from temporal.activities.my_domain.my_activity import my_activity
   ACTIVITIES.append(my_activity)
   ```

## Organization by Domain

As the project grows, organize workflows and activities by domain:

```
temporal/
├── workflows/
│   ├── automation/       # Server provisioning, etc.
│   ├── deployment/       # Application deployment
│   ├── monitoring/       # Monitoring setup
│   └── backup/           # Backup operations
└── activities/
    ├── automation/       # Automation activities
    ├── deployment/       # Deployment activities
    ├── monitoring/       # Monitoring activities
    └── backup/           # Backup activities
```

## Configuration

Configuration is managed in `temporal/config.py` and can be overridden via environment variables:

- `TEMPORAL_ADDRESS`: Server address (default: localhost:7233)
- `TEMPORAL_NAMESPACE`: Namespace (default: default)
- `TEMPORAL_TASK_QUEUE`: Default task queue (default: test-task-queue)

## Best Practices

1. **Keep workflows deterministic** - No random values, file I/O, or network calls
2. **Use activities for non-deterministic operations** - All I/O, network, etc.
3. **Use shared utilities** - Common retry policies, timeouts, etc.
4. **Register everything** - Add workflows/activities to `__init__.py`
5. **Organize by domain** - Group related workflows/activities together

