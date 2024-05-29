#!/usr/bin/python3
"""Create a new City objects that handles all default RESTful API actions"""
from flask import jsonify, request, abort
from models.place import Place
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews_by_place(place_id):
    """Retrive the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if data is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/review/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieve a review with a particular id from database"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/review/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a Review object by ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],  strict_slashes=False)
def create_review(place_id):
    """Create a new Review """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(400,)
    if 'text' not in data:
        abort(400, 'Missing text')

    new_review = Review(**data)
    new_review.place_id = place.id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],  strict_slashes=False)
def update_review(review_id):
    """Update a Place object by ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    
    # Ignore keys: id, create_at, updated_at
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    
    storage.save(review)
    return jsonify(review.to_dict()), 200
