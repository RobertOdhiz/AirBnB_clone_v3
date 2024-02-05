#!/usr/bin/python3
""" defines a module that Create a new view for Place
objects that handles all default RESTFul API actions """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.city import City
from models.user import User
from models.place import Place
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


def get_class_obj_dict(cls):
    """ Returns a dictionary of Class objects"""
    objs = list(storage.all(cls).values())
    objs_dict = [obj.to_dict() for obj in objs]
    return objs_dict


@app_views.route('/places', strict_slashes=False, methods=['GET'])
def get_post_places():
    """Gets or Posts the list of all Place objects """
    if request.method == 'GET':
        places_dict = get_class_obj_dict(Place)
        return jsonify(places_dict)


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST', 'GET'])
def get_post_places_by_city(city_id):
    """Gets or Posts the list of all Place objects by city """
    cities = get_class_obj_dict(City)
    s_id = [city_id for city in cities if city.get('id') == city_id]
    if not s_id:
        abort(404)

    if request.method == 'GET':
        places = get_class_obj_dict(Place)
        city_places = [place for place in places
                       if place.get('city_id') == s_id[0]]
        return jsonify(city_places)

    if request.method == 'POST':
        req = get_json_file()
        if not req.get('name'):
            abort(400, description="Missing name")
        if not req.get('user_id'):
            abort(400, description="Missing user_id")

        users = get_class_obj_dict(User)
        user_id = req.get('user_id')
        u_id = [user_id for user in users if user.get('id') == user_id]
        if not u_id:
            abort(404)

        place = Place(city_id=s_id[0], **req)
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def get_put_delete_place(place_id):
    """ Gets, Puts and Deletes an individual place by id """
    if request.method == 'GET':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        storage.delete(place)
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        req = get_json_file()
        keys = ['city_id', 'user_id', 'id', 'created_at', 'updated_at']
        for key, value in req.items():
            if key not in keys:
                setattr(place, key, value)

        storage.save()

        return jsonify(place.to_dict()), 200
