#!/usr/bin/python3
""" defines a module that Create a new view for Review
objects that handles all default RESTFul API actions """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.user import User
from models.review import Review
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


@app_views.route('/reviews', strict_slashes=False, methods=['GET'])
def get_post_reviews():
    """Gets or Posts the list of all Review objects """
    if request.method == 'GET':
        reviews_dict = get_class_obj_dict(Review)
        return jsonify(reviews_dict)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST', 'GET'])
def get_post_reviews_by_place(place_id):
    """Gets or Posts the list of all Review objects by place """
    places = get_class_obj_dict(Place)
    s_id = [place_id for place in places if place.get('id') == place_id]
    if not s_id:
        abort(404)

    if request.method == 'GET':
        reviews = get_class_obj_dict(Review)
        place_reviews = [review for review in reviews
                         if review.get('place_id') == s_id[0]]
        return jsonify(place_reviews)

    if request.method == 'POST':
        req = get_json_file()
        if not req.get('text'):
            abort(400, description="Missing text")
        if not req.get('user_id'):
            abort(400, description="Missing user_id")

        users = get_class_obj_dict(User)
        user_id = req.get('user_id')
        u_id = [user_id for user in users if user.get('id') == user_id]
        if not u_id:
            abort(404)

        review = Review(place_id=s_id[0], **req)
        review.save()
        return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def get_put_delete_review(review_id):
    """ Gets, Puts and Deletes an individual review by id """
    if request.method == 'GET':
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        storage.delete(review)
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        req = get_json_file()
        keys = ['place_id', 'user_id', 'id', 'created_at', 'updated_at']
        for key, value in req.items():
            if key not in keys:
                setattr(review, key, value)

        storage.save()

        return jsonify(review.to_dict()), 200
