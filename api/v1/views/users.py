#!/usr/bin/python3
"""Create a new City objects that handles all default RESTful API actions"""
from flask import jsonify, request, abort
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users/', methods=['GET'], strict_slashes=False)
def get_all_user():
    """Retrive a city object by ID"""
    datas = storage.all(User).values()
    if data is None:
        abort(404)
    return jsonify([data.to_dict() for data in datas])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieve a user with a particular id from database"""
    user= storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a User object by ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'],  strict_slashes=False)
def create_user():
    """Create a new User object"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    new_user = user(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],  strict_slashes=False)
def update_user(user_id):
    """Update a User object by ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    
    # Ignore keys: id, create_at, updated_at
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    
    storage.save(user)
    return jsonify(user.to_dict()), 200
