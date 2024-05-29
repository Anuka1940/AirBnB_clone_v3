#!/usr/bin/python3
"""Create a new City objects that handles all default RESTful API actions"""
from flask import jsonify, request, abort
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """Retrive a city object by ID"""
    city = storage.get(City, state_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieve a city with a particular id from database"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete a City object by ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],  strict_slashes=False)
def create_city(state_id):
    """Create a new State object"""
    city = request.get_json()
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if city is None:
        abort(400, 'Not a JSON')
    if 'name' not in city:
        abort(400, 'Missing name')
    new_city = City(**city)
    setattr(new_city, 'state_id', state.id)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],  strict_slashes=False)
def update_city(city_id):
    """Update a City object by ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    
    # Ignore keys: id, create_at, updated_at
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    
    storage.save(city)
    return jsonify(city.to_dict()), 200
