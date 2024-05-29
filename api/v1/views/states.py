#!/usr/bin/python3
"""Create a new for State objects that handles all default RESTful API actions"""
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieve the list of all State objects"""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)

@app_views.route('/states/<state_id>', methods=['GET'],  strict_slashes=False)
def get_state(state_id):
    """Retrive a State object by ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'],  strict_slashes=False)
def delete_state(state_id):
    """Delete a State object by ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states', methods=['POST'],  strict_slashes=False)
def create_state():
    """Create a new State object"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dic()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],  strict_slashes=False)
def update_state(state_id):
    """Update a Stete object by ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    
    # Ignore keys: id, create_at, updated_at
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    
    storage.save()
    return jsonify(state.to_dict()), 200