"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)

############################# TABLA USER ############################################

@api.route('/user', methods=['POST'])
def create_user():
    body = request.get_json()
    new_user = User(body['user_name'], body['email'], body['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 200

@api.route('/user', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    all_users_serializable = list(map(lambda user: user.serialize(), all_users))
    return jsonify(all_users_serializable)

@api.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    one_user = User.query.get(user_id)
    return jsonify(one_user.serialize()), 200

@api.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": user.serialize()}), 200
    else:
        return jsonify({"error": "User not found"}), 404
