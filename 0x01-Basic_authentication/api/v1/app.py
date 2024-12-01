#!/usr/bin/env python3
"""
Route module for the API

This module sets up the Flask application, registers blueprints,
handles CORS configuration, and includes custom error handlers
for the API. The application listens on a host and port defined
via environment variables or defaults to 0.0.0.0:5000.
"""
from os import getenv
from flask import Flask, jsonify, Response
from flask_cors import CORS
from api.v1.views import app_views

# Initialize Flask application
app = Flask(__name__)

# Register the app_views blueprint with a URL prefix
app.register_blueprint(app_views, url_prefix='/api/v1')

# Configure Cross-Origin Resource Sharing (CORS) for the API
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


# Error handler for 401 Unauthorized
@app.errorhandler(401)
def unauthorized(error) -> Response:
    """
    Custom handler for 401 Unauthorized errors.
    Returns:
        JSON response with error message and 401 status code.
    """
    return jsonify({"error": "Unauthorized"}), 401


# Error handler for 404 Not Found
@app.errorhandler(404)
def not_found(error) -> Response:
    """
    Custom handler for 404 Not Found errors.
    Returns:
        JSON response with error message and 404 status code.
    """
    return jsonify({"error": "Not found"}), 404


# Main entry point for running the Flask application
if __name__ == "__main__":
    # Get host and port from environment variables, with defaults
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    # Run the Flask application
    app.run(host=host, port=port)
