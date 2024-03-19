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
from models import db, User, Character, Habitat, Favorites
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

@app.route('/user', methods=['GET'])
def handle_user():

    all_user = User.query.all()

    response_body = list(map(lambda x: x.serialize(), all_user))

    return jsonify(response_body), 200

@app.route('/user/<int:id>', methods=['GET'])
def handle_single_user(id):

    user = User.query.get(id)

    response_body = user.serialize()

    return jsonify(response_body), 200

@app.route('/user', methods=['POST'])
def handle_add_user():
    request_body = request.json
    new_user = User(email = request_body['email'],
                    password = request_body['password'],
                    username = request_body['username']
                    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(f'new user {new_user} created'), 200


@app.route('/character', methods=['GET'])
def handle_character():

    all_character = Character.query.all()

    response_body = list(map(lambda x: x.serialize(), all_character))

    return jsonify(response_body), 200

@app.route('/character/<int:id>', methods=['GET'])
def handle_single_character(id):

    character = Character.query.get(id)

    response_body = character.serialize()

    return jsonify(response_body), 200

@app.route('/habitat', methods=['GET'])
def handle_habitat():

    all_habitat = Habitat.query.all()

    response_body = list(map(lambda x: x.serialize(), all_habitat))

    return jsonify(response_body), 200

@app.route('/habitat/<int:id>', methods=['GET'])
def handle_single_habitat(id):

    habitat =Habitat.query.get(id)

    response_body = habitat.serialize()

    return jsonify(response_body), 200

@app.route('/user/<int:id>/favorites', methods=['GET'])
def handle_single_user_favorites(id):

    get_favorites = Favorites.query.filter_by(fav_user_id =id)
    user_favorites = list(map(lambda x: x.serialize(), get_favorites))

    response_body = user_favorites


    return jsonify(response_body), 200

@app.route('/favorites', methods=['GET'])
def handle_favorites():

    all_favorites = Favorites.query.all()

    response_body = list(map(lambda x: x.serialize(), all_favorites))

    return jsonify(response_body), 200

@app.route('/favorites', methods=['POST'])
def handle_post():
    request_body = request.json
    new_favorite = Favorites(fav_user_id = request_body['user_id'],
                             entity_id = request_body['entity_id'],
                             entity_type = request_body['entity_type'],
                             fav_name = request_body['fav_name'])
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(f'new favorite {new_favorite} successfully created'), 200

@app.route('/favorites/<id>', methods=['DELETE'])
def handle_delete(id):
    del_favorite = Favorites.query.get(id)
    db.session.delete(del_favorite)
    db.session.commit()
    return jsonify(f'{del_favorite} deleted'), 200

    




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
