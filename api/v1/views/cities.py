#!/usr/bin/python3
"""
Flask route that returns json status response
"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def state_all_cities(state_id):
    """Example endpoint returning a list of all the cities of a state
    Retrieves all the cities of a given state_id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    all_cities = [city.to_dict() for city in state.cities]
    return jsonify(all_cities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def one_city(city_id):
    """Example endpoint returning one city
    Retrieves one city of a given city_id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_json())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_one_city(city_id):
    """Example endpoint deleting one city
    Deletes a state based on the city_id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    return jsonify({})


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_one_city(state_id):
    """Example endpoint creating one city
    Creates one city tied with the given state_id based on the JSON body
    """
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    if 'name' not in r.keys():
        return "Missing name", 400
    s = storage.get(State, state_id)
    if s is None:
        abort(404)
    # creates the dictionary r as kwargs to create a city object
    c = City(**r)
    c.state_id = state_id
    c.save()
    return jsonify(c.to_json()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_one_city(city_id):
    """Example endpoint updates one city
    Updates one city tied with the given state_id based on the JSON body
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    for k in ("id", "created_at", "updated_at", "state_id"):
        r.pop(k, None)
    for k, v in r.items():
        setattr(city, k, v)
    city.save()
    return jsonify(city.to_json()), 200
