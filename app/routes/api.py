"""API routes blueprint."""

import asyncio
import time
from flask import Blueprint, jsonify, request
from temporalio.client import Client
from temporalio.service import RPCError
from temporal.config import config
from temporal.workflow_metadata import (
    get_all_workflow_metadata,
    get_workflow_metadata,
)


bp = Blueprint('api', __name__)


@bp.route('/workflows', methods=['GET'])
def list_workflows():
    """Get list of all available workflows."""
    try:
        workflows = get_all_workflow_metadata()
        workflows_data = []

        for workflow in workflows:
            workflows_data.append({
                'id': workflow.id,
                'name': workflow.name,
                'description': workflow.description,
                'category': workflow.category,
                'parameters': workflow.parameters,
            })
        
            return jsonify({
                'success': True,
                'workflows': workflows_data,
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/workflows/<workflow_id>/run', methods=['POST'])
def run_workflow(workflow_id: str):
    """Run a specific workflow.

    Args:
        workflow_id: ID of the workflow to run
    """
    async def _run_workflow():
        try:
            # Get workflow metadata
            workflow_meta = get_workflow_metadata(workflow_id)
            if not workflow_meta:
                return jsonify({
                    'success': False,
                    'error': f'Workflow "{workflow_id}" not found'
                }), 404

            # Get parameters from request
            data = request.get_json() or {}

            # Build workflow arguments from parameters
            # Parameters are passed as positional args to workflow function
            workflow_args = []

            # Extract parameters based on metadata
            # Sort parameters to maintain consistent order
            sorted_params = sorted(
                workflow_meta.parameters,
                key=lambda p: (p.get('required', False), p['name'])
            )

            for param in sorted_params:
                param_name = param['name']
                param_value = data.get(param_name)

                # Use default if value not provided
                if param_value is None or param_value == '':
                    param_value = param.get('default')

                if param.get('required', False) and param_value is None:
                    return jsonify({
                        'success': False,
                        'error': (
                            f'Required parameter "{param_name}" is missing'
                        )
                    }), 400

                # Add parameter value to args list (only if not None)
                if param_value is not None:
                    workflow_args.append(param_value)

            # Connect to Temporal server
            client = await Client.connect(
                config.ADDRESS,
                namespace=config.NAMESPACE
            )

            # Generate unique workflow ID
            workflow_run_id = f"{workflow_id}-{int(time.time() * 1000)}"

            # Start the workflow
            # Note: workflow arguments are passed as positional args
            handle = await client.start_workflow(
                workflow_meta.workflow_class.run,
                *workflow_args,
                id=workflow_run_id,
                task_queue=config.DEFAULT_TASK_QUEUE,
            )

            # Wait for the result
            result = await handle.result()

            return jsonify({
                'success': True,
                'result': result,
                'workflow_id': workflow_run_id,
                'workflow_name': workflow_meta.name,
            })
        except RPCError as e:
            return jsonify({
                'success': False,
                'error': f'Failed to connect to Temporal server: {e}'
            }), 500
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    return asyncio.run(_run_workflow())


# Keep the old endpoint for backward compatibility
@bp.route('/run-test', methods=['POST'])
def run_test():
    """API endpoint to run the test workflow (backward compatibility)."""
    return run_workflow('test')


@bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})
