"""API routes blueprint."""

import asyncio
from flask import Blueprint, jsonify, request

bp = Blueprint('api', __name__)


@bp.route('/run-test', methods=['POST'])
def run_test():
    """API endpoint to run the test workflow."""
    try:
        data = request.get_json() or {}
        name = data.get('name', 'World')

        # Import here to avoid circular imports
        from temporal_client import start_test_workflow

        # Run the async workflow
        result = asyncio.run(start_test_workflow(name))

        return jsonify({
            'success': True,
            'result': result,
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})

