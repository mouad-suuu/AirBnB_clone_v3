#!/usr/bin/python3
"""Users view functions"""
from flask import jsonify, abort, request
from models import storage
from models.user import User

from api.v1.views import app_views


@app_views.route('/users', methods=['GET'])
def get_users():
    """Retrieves the list of all User objects"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates a User"""
    request_data = request.get_json()
    if not request_data:
        abort(400, description="Not a JSON")
    if 'email' not in request_data:
        abort(400, description="Missing email")
    if 'password' not in request_data:
        abort(400, description="Missing password")
    new_user = User(**request_data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, description="Not a JSON")
    for key, value in request_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
