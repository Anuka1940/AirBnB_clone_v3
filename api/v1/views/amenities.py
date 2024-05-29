#!/usr/bin/python3
"""Create a new City objects that handles all default RESTful API actions"""
from flask import jsonify, request, abort
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amen/', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Retrive a city object by ID"""
    datas = storage.all(Amenity).values()
    if data is None:
        abort(404)
    return jsonify([data.to_dict() for data in datas])


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieve a amenity with a particular id from database"""
    amenity= storage.get(amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete a City object by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],  strict_slashes=False)
def create_amenity():
    """Create a new State object"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],  strict_slashes=False)
def update_amenity(amenity_id):
    """Update a Amenity object by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    
    # Ignore keys: id, create_at, updated_at
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    
    storage.save(amenity)
    return jsonify(amenity.to_dict()), 200
