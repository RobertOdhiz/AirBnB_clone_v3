#!/usr/bin/python3
""" defines a module that Create a new view for Amenity
objects that handles all default RESTFul API actions """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


def get_json_file():
    """Returns a json file"""
    try:
        if not request.is_json:
            abort(400, description="Not a JSON")
        req = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")
    return req


@app_views.route('/amenities', strict_slashes=False, methods=['POST', 'GET'])
def get_post_amenities():
    """Gets or Posts the list of all Amenity objects """
    if request.method == 'GET':
        amenities = list(storage.all(Amenity).values())
        amenities_dict = [amenity.to_dict() for amenity in amenities]
        return jsonify(amenities_dict)

    if request.method == 'POST':
        req = get_json_file()
        if not req.get('name'):
            abort(400, description="Missing name")
        amenity = Amenity(**req)
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def get_put_delete_amenity(amenity_id):
    """ Gets, Puts and Deletes an individual amenity by id """
    if request.method == 'GET':
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        storage.delete(amenity)
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        req = get_json_file()
        keys = ['id', 'created_at', 'updated_at']
        for key, value in req.items():
            if key not in keys:
                setattr(amenity, key, value)

        storage.save()

        return jsonify(amenity.to_dict()), 200
