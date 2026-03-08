"""
app/__init__.py
Flask application factory
"""

import os
from flask import Flask
from config.settings import get_config


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Load config
    config = get_config()
    app.config.from_object(config)

    # Ensure upload folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
