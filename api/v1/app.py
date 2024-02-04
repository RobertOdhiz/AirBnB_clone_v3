#!/usr/bin/python3
""" Defines a module that calls app.py """
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def clear_resource(exception=None):
    """Frees resources and close sessions"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Handles 404 not found"""
    return jsonify({"error": "Not found"})


if __name__ == "__main__":
    """ """
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(debug=True, host=host, port=port, threaded=True)
