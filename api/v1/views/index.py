#!/usr/bin/python3
""" Index """

from flask import jsonify, request
from api.v1.views import app_views
from models import storage


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def status():
    """
    function for status route that returns the status
    """
    if request.method == 'GET':
        resp = {"status": "OK"}
        return jsonify(resp)


def get_stats():
    """Retrieve the number of each object type"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
