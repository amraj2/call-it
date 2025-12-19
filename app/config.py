"""Application configuration."""

import os


class Config:
    """Base configuration class."""

    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

    # Server configuration
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FLASK_PORT', 8000))

    # Temporal configuration
    TEMPORAL_ADDRESS = os.environ.get('TEMPORAL_ADDRESS', 'localhost:7233')
    TEMPORAL_TASK_QUEUE = os.environ.get('TEMPORAL_TASK_QUEUE', 'test-task-queue')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}

