#!/usr/bin/python3
""" defines a module that Create a new view for Amenity
objects that handles all default RESTFul API actions """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity
from models import storage


def get_class_obj_dict(cls):
    """ Returns a dictionary of Class objects"""
    objs = list(storage.all(cls).values())
    objs_dict = [obj.to_dict() for obj in objs]
    return objs_dict


@app_views.route('/places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
def get_post_place_amenities(place_id):
    """Gets or Posts the list of all Amenity objects by place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        amenities = get_class_obj_dict(Amenity)
        a_ids = [amenity.id for amenity in place.amenities]
        place_amenities = [amenity for amenity in amenities
                           if amenity.get('id') in a_ids]
        return jsonify(place_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'POST'])
def get_post_delete_place_amenity(place_id, amenity_id):
    """ Gets, Puts and Deletes an individual place amenity by id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({})

    if request.method == 'POST':
        a_id = [amenity.id for amenity in place.amenities
                if amenity.id == amenity_id]
        if a_id:
            return jsonify(amenity.to_dict()), 200

        place.amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_dict()), 201
