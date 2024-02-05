#!/usr/bin/python3
""" defines a module that Create a new view for City
objects that handles all default RESTFul API actions """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models.city import City
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


@app_views.route('/cities', strict_slashes=False, methods=['GET'])
def get_post_cities():
    """Gets or Posts the list of all City objects """
    if request.method == 'GET':
        cities_dict = get_class_obj_dict(City)
        return jsonify(cities_dict)


@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=['POST', 'GET'])
def get_post_cities_by_state(state_id):
    """Gets or Posts the list of all City objects by state """
    states = get_class_obj_dict(State)
    s_id = [state_id for state in states if state.get('id') == state_id]
    if not s_id:
        abort(404)

    if request.method == 'GET':
        cities = get_class_obj_dict(City)
        state_cities = [city for city in cities if city.get('state_id') == s_id[0]]
        return jsonify(state_cities)

    if request.method == 'POST':
        req = get_json_file()
        if not req.get('name'):
            abort(400, description="Missing name")
        city = City(name=req.get('name'), state_id=s_id[0])
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def get_put_delete_city(city_id):
    """ Gets, Puts and Deletes an individual city by id """
    if request.method == 'GET':
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        storage.delete(city)
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        req = get_json_file()
        keys = ['state_id', 'id', 'created_at', 'updated_at']
        for key, value in req.items():
            if not key in keys:
                setattr(city, key, value)

        storage.save()

        return jsonify(city.to_dict()), 200
