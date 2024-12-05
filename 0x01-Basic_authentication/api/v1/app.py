#!/usr/bin/env python3
"""
Route module for the API.

This module defines the main entry point for the Flask API application.
It initializes the Flask app, registers blueprints, configures CORS,
and provides custom error handlers for 401 and 404 HTTP errors.
The API serves as the backend for the application, enabling interactions
with various services.
"""

from os import getenv
from flask import Flask, jsonify, Response
from flask_cors import CORS
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.errorhandler(401)
def unauthorized(error) -> Response:
    """
    Handle 401 Unauthorized HTTP errors.

    This function provides a JSON response with an appropriate
    error message when a 401 error is raised. It is used to signal
    that the client is not authorized to access the requested resource.

    Args:
        error: The error object containing details about the 401 error.

    Returns:
        A tuple containing a JSON response with an error message and
        the HTTP status code 401.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(404)
def not_found(error) -> Response:
    """
    Handle 404 Not Found HTTP errors.

    This function provides a JSON response with an appropriate
    error message when a 404 error is raised. It is used to signal
    that the requested resource was not found on the server.

    Args:
        error: The error object containing details about the 404 error.

    Returns:
        A tuple containing a JSON response with an error message and
        the HTTP status code 404.
    """
    return jsonify({"error": "Not found"}), 404


def _get_data_for_json(self):
    """
    Retrieves data for JSON serialization.

    This method is used internally to process and return
    data formatted for JSON responses.

    Returns:
        dict: The data prepared for JSON serialization.
    """
    if self.is_json:
        return self.get_json()
    else:
        try:
            return {"data": self.data.decode("utf-8")}
        except Exception:
            return {"error": "Response data is not JSON serializable"}


if __name__ == "__main__":
    """
    Main entry point of the application.

    This block retrieves the host and port from environment variables
    (with default values of 0.0.0.0 and 5000, respectively), and starts
    the Flask application to listen for incoming requests.
    """
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
