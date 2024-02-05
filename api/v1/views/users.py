#!/usr/bin/python3
""" defines a module that Create a new view for User
objects that handles all default RESTFul API actions """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
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


@app_views.route('/users', strict_slashes=False, methods=['POST', 'GET'])
def get_post_users():
    """Gets or Posts the list of all User objects """
    if request.method == 'GET':
        users = list(storage.all(User).values())
        users_dict = [user.to_dict() for user in users]
        return jsonify(users_dict)

    if request.method == 'POST':
        req = get_json_file()
        if not req.get('email'):
            abort(400, description="Missing email")
        if not req.get('password'):
            abort(400, description="Missing password")
        user = User(**req)
        user.save()
        return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def get_put_delete_user(user_id):
    """ Gets, Puts and Deletes an individual user by id """
    if request.method == 'GET':
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        storage.delete(user)
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        req = get_json_file()
        keys = ['id', 'email', 'created_at', 'updated_at']
        for key, value in req.items():
            if key not in keys:
                setattr(user, key, value)

        storage.save()

        return jsonify(user.to_dict()), 200
