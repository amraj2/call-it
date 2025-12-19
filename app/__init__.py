"""Flask application factory."""

import os
from flask import Flask
from flask_cors import CORS

from app.config import Config


def create_app(config_class=Config):
    """Create and configure the Flask application.

    Args:
        config_class: Configuration class to use

    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS
    CORS(app)

    # Register blueprints
    from app.routes import main, api
    app.register_blueprint(main.bp)
    app.register_blueprint(api.bp, url_prefix='/api')

    return app

