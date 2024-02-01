#!/usr/bin/python3
"""Places view for API"""

from flask import Flask, jsonify, request, abort
from models import storage
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """Retrieves list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    req_data = request.get_json()
    if req_data is None:
        abort(400, "Not a JSON")
    if 'user_id' not in req_data:
        abort(400, "Missing user_id")
    user = storage.get(User, req_data['user_id'])
    if not user:
        abort(404)
    if 'name' not in req_data:
        abort(400, "Missing name")

    req_data['city_id'] = city_id
    new_place = Place(**req_data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    req_data = request.get_json()
    if req_data is None:
        abort(400, "Not a JSON")

    ignore_keys = ['id', 'user_id', 'city_id',
                   'created_at', 'updated_at']
    for key, value in req_data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """Searches for places based on JSON in request body"""
    body = request.get_json()
    if body is None:
        abort(400, description="Not a JSON")

    states = body.get('states', [])
    cities = body.get('cities', [])
    amenities = body.get('amenities', [])

    places = []
    if not states and not cities and not amenities:
        places = storage.all(Place).values()
    else:
        if states:
            for state_id in states:
                state = storage.get(State, state_id)
                if state:
                    for city in state.cities:
                        places.extend(city.places)
        if cities:
            for city_id in cities:
                city = storage.get(City, city_id)
                if city:
                    places.extend(city.places)
        if amenities:
            places = [place for place in places
                      if all(amenity.id in amenities
                             for amenity in place.amenities)]

    places = [place.to_dict() for place in places]
    return jsonify(places)
