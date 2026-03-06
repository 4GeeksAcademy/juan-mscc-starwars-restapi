"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from datetime import datetime
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, FavChar, FavPlanet
from sqlalchemy import select
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():

    all_users = User.query.all()
    list_of_users = list(map(lambda user: user.serialize(), all_users))
    print(list_of_users)

    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "results" : list_of_users
    }

    return jsonify(list_of_users), 200

@app.route('/character', methods=['GET'])
def get_characters():

    all_characters = Character.query.all()
    list_of_characters = list(map(lambda character: character.serialize(), all_characters))
    print(list_of_characters)

    return jsonify(list_of_characters), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character(character_id):

    character = Character.query.filter_by(id=character_id).first()
    if character is None:
        return ('Character does not exist')
    character_info = character.serialize()
    print(character_info)

    return jsonify(character_info), 200

@app.route('/planet', methods=['GET'])
def get_planets():

    all_planets = Planet.query.all()
    list_of_planets = list(map(lambda planet: planet.serialize(), all_planets))


    return jsonify(list_of_planets), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):

    planet = Planet.query.filter_by(id=planet_id).first()
    if planet is None:
        return ('Planet does not exist')
    planet_info = planet.serialize()

    return jsonify(planet_info), 200


@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    first_user_id = User.query.first().serialize()['id']
  
    
    all_fav_chars_ids = list(map(lambda fav_character:  fav_character.serialize()['id'] , FavChar.query.filter_by(id_user=first_user_id).all()))
    all_fav_planets_ids = list(map(lambda fav_planet: fav_planet.serialize()['id'] , FavPlanet.query.filter_by(id_user=first_user_id).all()))

    all_fav_chars = list(map(lambda character: Character.query.get(character) , all_fav_chars_ids))
    all_fav_planets = list(map(lambda planet: Planet.query.get(planet) , all_fav_planets_ids))

    print(all_fav_chars)
    print('###########')

    all_fav_chars_details = list(map(lambda character: character.serialize(), all_fav_chars))
    all_fav_planets_details = list(map(lambda planet: planet.serialize(), all_fav_planets))

    print(all_fav_chars_details)
    response_body = {
        "characters": all_fav_chars_details,
        "planets" : all_fav_planets_details
    }

    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST', 'DELETE'])
def manage_fav_planet(planet_id):
    first_user_id = User.query.first().serialize()['id']
    
    all_fav_planets_ids = list(map(lambda fav_planet: fav_planet.serialize()['id_planet'] , FavPlanet.query.filter_by(id_user=first_user_id).all()))
    
    if (request.method == 'POST'):
        if (planet_id in all_fav_planets_ids):
            return ('planet already in favorites', 400)
        else:
            fav_planet = FavPlanet(id_user=first_user_id, id_planet= planet_id, date='today')
            db.session.add(fav_planet)
            db.session.commit()
            return (f'{planet_id} added to favorites', 200)
    else:
        if (planet_id not in all_fav_planets_ids):
            return ('planet is not in favorites', 400)
        else:
            fav_planet = db.session.execute(select(FavPlanet).where(FavPlanet.id_planet == planet_id)).scalar_one_or_none()
            db.session.delete(fav_planet)
            db.session.commit()
            return (f'{planet_id} erased from favorites', 200)



@app.route('/favorite/character/<int:character_id>', methods=['POST', 'DELETE'])
def manage_fav_character(character_id):
    first_user_id = User.query.first().serialize()['id']
    
    all_fav_chars_ids = list(map(lambda fav_character:  fav_character.serialize()['id_char'] , FavChar.query.filter_by(id_user=first_user_id).all()))
    
    if (request.method == 'POST'):
        if (character_id in all_fav_chars_ids):
            return ('character already in favorites', 400)
        else:
            fav_character = FavChar(id_user=first_user_id, id_char= character_id, date='today')
            db.session.add(fav_character)
            db.session.commit()
            return (f'{character_id} added to favorites', 200)
    else:
        if (character_id not in all_fav_chars_ids):
            return ('character is not in favorites', 400)
        else:
            fav_character = db.session.execute(select(FavChar).where(FavChar.id_char == character_id)).scalar_one_or_none()
            db.session.delete(fav_character)
            db.session.commit()
            return (f'{character_id} erased from favorites', 200)




######
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
