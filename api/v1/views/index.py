#!/usr/bin/python3
""" Index """

from flask import jsonify , Flask
# Import the blueprint from the local package context
from . import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    return jsonify({"status": "OK"})
