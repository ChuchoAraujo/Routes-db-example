"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, People, Planet, Favorites
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)

############################# TABLA USER ############################################
## GET USERS
@api.route('/user', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    all_users_serializable = list(map(lambda user: user.serialize(), all_users))
    return jsonify(all_users_serializable)

## POST USERS
@api.route('/user', methods=['POST'])
def create_user():
    body = request.get_json()
    new_user = User(body['user_name'], body['email'], body['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'user': new_user.serialize()}), 200

## GET USER ID
@api.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    one_user = User.query.get(user_id)
    if one_user:
        return jsonify({'user': one_user.serialize()}), 200
    else:
        return jsonify({'msg': 'Id not exist'})

## DELETE USERS
@api.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": user.serialize()}), 200
    else:
        return jsonify({"error": "User not found"}), 404


############################# TABLA PEOPLE ############################################
## GET PEOPLE
@api.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all()
    all_people_serializable = list(map(lambda people: people.serialize(), all_people))
    return jsonify({'people': all_people_serializable})

## POST PEOPLE
@api.route('/people', methods=['POST'])
def create_people():
    body = request.get_json()
    new_people = People(body['name'], body['description'])
    db.session.add(new_people)
    db.session.commit()
    return jsonify({'people': new_people.serialize()})

## GET PEOPLE ID
@api.route('/people/<int:people_id>', methods=['GET'])
def get_one_people(people_id):
    one_people = People.query.get(people_id)
    if one_people:
        return jsonify({'people': one_people.serialize()}), 200
    else:
        return jsonify({'msg': 'Id not exist!'})

## DELETE PEOPLE
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
## GET PLANET
@api.route('/planet', methods=['GET'])
def get_planet():
    all_planet = Planet.query.all()
    all_planet_serializable = list(map(lambda planet: planet.serialize(), all_planet))
    return jsonify({'planet': all_planet_serializable})

## POST PLANET
@api.route('/planet', methods=['POST'])
def create_planet():
    body = request.get_json()
    new_planet = Planet(body['name'], body['climate'])
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({'people': new_planet.serialize()})

## GET PLANET ID
@api.route('/planet/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    one_planet = Planet.query.get(planet_id)
    if one_planet:
        return jsonify({'planet': one_planet.serialize()}), 200
    else:
        return jsonify({'msg': 'Id not exist!'})

## DELETE PLANET
@api.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    one_planet = Planet.query.get(planet_id)
    if one_planet:
        db.session.delete(one_planet)
        db.session.commit()
        return jsonify({'planet': one_planet.serialize()})
    else:
        return jsonify({"error": "Planet not found"}), 404

############################# TABLA FAVORITES ############################################
## GET FAVORITES
@api.route('/favorites', methods=['GET'])
def get_all_favorites():
    favorites = Favorites.query.all()
    serialized_favorites = [f.serialize() for f in favorites]
    return jsonify(serialized_favorites), 200

## GET USERS FAVORITES
@api.route('/users/favorites', methods=['GET'])
def get_favorites():
    user_id = request.json.get('user_id')

    if not user_id:
        return jsonify({'msg': 'User ID is required.'}), 400

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'msg': 'User not found.'}), 404

    favorites = list(map(lambda f: f.serialize(), user.favorites))

    if not favorites:
        return jsonify({'msg': 'No favorites found for the specified user.'}), 404

    return jsonify({'favorites': favorites}), 200


## POST PLANET FAVORITES
@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'message': 'User ID is required.'}), 400
        
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found.'}), 404
    
    favorite = Favorites(user_id=user_id, planet_id=planet_id)
    
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({'favorite': favorite.serialize()}), 201

## POST PEOPLE FAVORITES
@api.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'message': 'User ID is required.'}), 400
        
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found.'}), 404
    
    favorite = Favorites(user_id=user_id, people_id=people_id)
    
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({'favorite': favorite.serialize()}), 201

## DELETE PLANET FAVORITES
@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    # Obtener el id del usuario desde el cuerpo de la solicitud
    user_id = request.get_json().get('user_id')
    
    if not user_id:
        return jsonify({'message': 'User ID is required.'}), 400
    
    # Verificar si el usuario ha marcado este planeta como favorito
    favorite = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({'message': 'This planet is not in your favorites list.'}), 404
    
    # Eliminar el planeta favorito de la lista de favoritos del usuario
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({'message': favorite.serialize()}), 200

## DELETE PEOPLE FAVORITES
@api.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    # Obtener el id del usuario desde el cuerpo de la solicitud
    user_id = request.get_json().get('user_id')
    
    if not user_id:
        return jsonify({'message': 'User ID is required.'}), 400
    
    # Verificar si el usuario ha marcado este planeta como favorito
    favorite = Favorites.query.filter_by(user_id=user_id, people_id=people_id).first()
    if not favorite:
        return jsonify({'message': 'This planet is not in your favorites list.'}), 404
    
    # Eliminar el planeta favorito de la lista de favoritos del usuario
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({'message': favorite.serialize()}), 200
























# @api.route('/users/<int:user_id>/favorites', methods=['GET'])
# def get_favorites(user_id):
#     user = User.query.get(user_id)

#     if not user:
#         return jsonify({'message': 'User not found.'}), 404

#     favorites = [f.serialize() for f in user.favorites]

#     if not favorites:
#         return jsonify({'message': 'No favorites found for the specified user.'}), 404

#     return jsonify({'favorites': favorites}), 200




# @api.route('/users/favorites', methods=['POST'])
# def add_favorite():
#     data = request.get_json()
#     user_id = data.get('user_id')
#     planet_id = data.get('planet_id')
#     people_id = data.get('people_id')
    
#     favorite = Favorites(user_id=user_id, planet_id=planet_id, people_id=people_id)
    
#     db.session.add(favorite)
#     db.session.commit()
    
#     return jsonify({'message': favorite.serialize() }), 201