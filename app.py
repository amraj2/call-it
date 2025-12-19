"""Flask application entry point."""

import os
import sys
import socket
from app import create_app
from app.config import config

# Get environment or default to development
env = os.environ.get('FLASK_ENV', 'development')
app = create_app(config.get(env, config['default']))


def is_port_in_use(port: int) -> bool:
    """Check if a port is already in use.

    Args:
        port: Port number to check

    Returns:
        True if port is in use, False otherwise
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


if __name__ == '__main__':
    port = app.config['PORT']
    host = app.config['HOST']
    debug = app.config['DEBUG']

    # Check if port is already in use
    if is_port_in_use(port):
        print(f'❌ Error: Port {port} is already in use.')
        print('   Another Flask app may be running on this port.')
        print('   To fix this:')
        print('   1. Stop the existing Flask app')
        print('   2. Or set FLASK_PORT to a different port')
        print(f'   3. Or run: lsof -ti:{port} | xargs kill')
        sys.exit(1)

    print(f'🌐 Flask app starting on http://localhost:{port}')
    print('📋 Make sure the Temporal worker is running:')
    print('   python3 temporal_worker.py')
    print(f'📊 Environment: {env}')
    print(f'🐛 Debug mode: {debug}')

    try:
        app.run(host=host, port=port, debug=debug, use_reloader=False)
    except OSError as e:
        if 'Address already in use' in str(e):
            print(f'\n❌ Error: Port {port} is already in use.')
            print('   Another process is using this port.')
            print(f'   To fix: lsof -ti:{port} | xargs kill')
            sys.exit(1)
        raise
