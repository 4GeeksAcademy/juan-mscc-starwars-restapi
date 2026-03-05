"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, FavChar, FavPlanet
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
    planet_info = planet.serialize()

    return jsonify(planet_info), 200


@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    first_user_id = User.query.first().serialize()['id']
    print(first_user_id)
    
    all_fav_chars = FavChar.query.filter_by(id_user=first_user_id)
    all_fav_planets = FavPlanet.query.filter_by(id_user=first_user_id)
    print(all_fav_chars)
    print(all_fav_planets)

    response_body = {
        "characters": "Hello, this is your GET /user response ",
        "planets" : "list_of_users"
    }

    return "jsonify(list_of_users)", 200




######
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
