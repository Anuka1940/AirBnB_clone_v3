#!/usr/bin/python3
"""Create a new City objects that handles all default RESTful API actions"""
from flask import jsonify, request, abort
from models.place import Place
from models import storage
from models.city import City
from models.user import User
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    """Retrive a city object by ID"""
    places = storage.get(City, city_id)
    if data is None:
        abort(404)
    return jsonify([place.to_dict() for place in places])


@app_views.route('/place/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieve a place with a particular id from database"""
    place= storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/place/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete a Place object by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],  strict_slashes=False)
def create_place(city_id):
    """Create a new place """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(400,)
    if 'name' not in data:
        abort(400, 'Missing name')
    new_place = Place(**data)
    new_place.city_id = city.id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],  strict_slashes=False)
def update_place(place_id):
    """Update a Place object by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    
    # Ignore keys: id, create_at, updated_at
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    
    storage.save(place)
    return jsonify(place.to_dict()), 200
