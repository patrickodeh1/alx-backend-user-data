#!/usr/bin/env python3
"""
Module of Index views.

This module defines Flask routes related to the API status, statistics,
and an endpoint to test unauthorized access handling. It provides
routes for checking the API health, fetching statistics of objects,
and raising a 401 error for testing purposes.
"""

from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """
    GET /api/v1/status

    Returns:
        A JSON response indicating the status of the API.

    This endpoint serves as a health check to verify that the API
    is up and running. A successful call returns {"status": "OK"}.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """
    GET /api/v1/stats

    Returns:
        A JSON response containing the number of each object type.

    This endpoint fetches the counts of various objects managed by
    the API. For example, it can return the number of users or other
    entities as a dictionary. Currently, it only counts users.
    """
    from models.user import User  # Import User model dynamically to avoid circular imports
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized/', methods=['GET'], strict_slashes=False)
def unauthorized():
    """
    GET /api/v1/unauthorized

    Raises:
        HTTPException: Raises a 401 Unauthorized error.

    This endpoint is used to simulate an unauthorized access scenario.
    It intentionally triggers a 401 error to test how the application
    handles unauthorized requests.
    """
    abort(401)
