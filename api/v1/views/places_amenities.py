#!/usr/bin/python3
"""
View for reviews that handles all RESTful API actions
"""
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def all_place_amenities(place_id):
    """Returns a list of all amenities in a given place"""
    data = []
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    amenities = places.amenities
    for amenity in amenities:
        data.append(amenity.to_dict())
    return jsonify(data)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes a single amenity"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for _amenity in place.amenities:
        if _amenity.id == amenity_id:
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['Post'], strict_slashes=False)
def update_place_amenity(place_id, amenity_id):
    """Link an amenity to a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for _amenity in place.amenities:
        if _amenity.id == amenity_id:
            return jsonify(_amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
