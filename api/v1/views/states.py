#!/usr/bin/python3
""" defines a module that Create a new view for State
objects that handles all default RESTFul API actions """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False, methods=['POST', 'GET'])
def get_states():
    """Gets the list of all State objects """
    if request.method == 'GET':
        states = list(storage.all(State).values())
        states_dict = [state.to_dict() for state in states]

        return states_dict
    else:
        if not request.is_json:
            return jsonify({'error', 'Not a JSON'}), 400
        req = request.json
        if not req.get('name'):
            return jsonify({'error', 'Missing name'}), 400
        state = State(name=req.get('name'))
        state.save()

        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """ Gets an individual state by id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def del_state(state_id):
    """ deletes an individual state by id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()

    return jsonify({})
