#!/usr/bin/python3
""" defines a module that Create a new view for State
objects that handles all default RESTFul API actions """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
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


@app_views.route('/states', strict_slashes=False, methods=['POST', 'GET'])
def get_states():
    """Gets the list of all State objects """
    if request.method == 'GET':
        states = list(storage.all(State).values())
        states_dict = [state.to_dict() for state in states]
        return jsonify(states_dict)
    if request.method == 'POST':
        req = get_json_file()
        if not req.get('name'):
            abort(400, description="Missing name")
        state = State(name=req.get('name'))
        state.save()
        return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """ Gets an individual state by id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE', 'PUT'])
def del_state(state_id):
    """ deletes an individual state by id """
    if request.method == 'DELETE':
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        storage.delete(state)
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        req = get_json_file()
        keys = ['id', 'created_at', 'updated_at']
        for key, value in req.items():
            if not key in keys:
                setattr(state, key, value)

        storage.save()

        return jsonify(state.to_dict()), 200
