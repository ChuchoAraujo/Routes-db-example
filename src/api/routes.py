"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, People, Planet
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)

############################# TABLA USER ############################################

@api.route('/user', methods=['POST'])
def create_user():
    body = request.get_json()
    new_user = User(body['user_name'], body['email'], body['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'user': new_user.serialize()}), 200

@api.route('/user', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    all_users_serializable = list(map(lambda user: user.serialize(), all_users))
    return jsonify(all_users_serializable)

@api.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    one_user = User.query.get(user_id)
    if one_user:
        return jsonify({'user': one_user.serialize()}), 200
    else:
        return jsonify({'msg': 'Id not exist'})

@api.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": user.serialize()}), 200
    else:
        return jsonify({"error": "User not found"}), 404

############################# TABLA USER ############################################
@api.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all()
    all_people_serializable = list(map(lambda people: people.serialize(), all_people))
    return jsonify({'people': all_people_serializable})

@api.route('/people', methods=['POST'])
def create_people():
    body = request.get_json()
    new_people = People(body['name'], body['description'])
    db.session.add(new_people)
    db.session.commit()
    return jsonify({'people': new_people.serialize()})

@api.route('/people/<int:people_id>', methods=['GET'])
def get_one_people(people_id):
    one_people = People.query.get(people_id)
    if one_people:
        return jsonify({'people': one_people.serialize()}), 200
    else:
        return jsonify({'msg': 'Id not exist!'})

api.route('/people/<int:people_id>', methods=['DELETE'])
def delete_people(people_id):
    one_people = People.query.get(people_id)
    if one_people:
        db.session.delete(one_people)
        db.session.commit()
        return jsonify({'people': one_people.serialize()})
    else:
        return jsonify({"error": "User not found"}), 404

############################# TABLA PLANET ############################################

@api.route('/planet', methods=['GET'])
def get_planet():
    all_planet = Planet.query.all()
    all_planet_serializable = list(map(lambda planet: planet.serialize(), all_planet))
    return jsonify({'planet': all_planet_serializable})

@api.route('/planet', methods=['POST'])
def create_planet():
    body = request.get_json()
    new_planet = Planet(body['name'], body['climate'])
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({'people': new_planet.serialize()})

@api.route('/planet/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    one_planet = Planet.query.get(planet_id)
    if one_planet:
        return jsonify({'planet': one_planet.serialize()}), 200
    else:
        return jsonify({'msg': 'Id not exist!'})

@api.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    one_planet = Planet.query.get(planet_id)
    if one_planet:
        db.session.delete(one_planet)
        db.session.commit()
        return jsonify({'planet': one_planet.serialize()})
    else:
        return jsonify({"error": "Planet not found"}), 404