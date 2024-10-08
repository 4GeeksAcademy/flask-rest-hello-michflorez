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
from models import db, User, Character, Planet, Vehicle, Favorites

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
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

db.init_app(app)
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
   user_query = User.query.filter_by(id=id).first()
   if user_query: 
       response_body = {
            "msg": "Usuario encontrado",
            "result": user_query.serialize()
        }
   return jsonify (response_body), 200


@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    return jsonify([character.serialize() for character in characters])

@app.route('/character/<int:id>', methods=['GET'])
def get_character(id):
   character_query = Character.query.filter_by(id=id).first()
   if character_query: 
       response_body = {
            "msg": "Usuario encontrado",
            "result": character_query.serialize()
        }
   return jsonify (response_body), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]) , 200

@app.route('/planet/<int:id>', methods=['GET'])
def get_planet(id):
   planet_query = Planet.query.filter_by(id=id).first()
   if planet_query: 
       response_body = {
            "msg": "Usuario encontrado",
            "result": planet_query.serialize()
        }
   return jsonify (response_body), 200


@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([vehicle.serialize() for vehicle in vehicles]) , 200

@app.route('/vehicle/<int:id>', methods=['GET'])
def get_vehicle(id):
   vehicle_query = Vehicle.query.filter_by(id=id).first()
   if vehicle_query: 
       response_body = {
            "msg": "Usuario encontrado",
            "result": vehicle_query.serialize()
        }
   return jsonify (response_body), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def create_favorite_planet(planet_id):
   request_body = request.json
   planet_favorite = Favorites(userId=request_body["user_id"],planetId=planet_id)
   db.session.add(planet_favorite)
   db.session.commit()
   response_body = {
            "msg": "Planeta creado con exito"
            
        }
   return jsonify (response_body), 200

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def create_favorite_vehicle(vehicle_id):
   request_body = request.json
   vehicle_favorite = Favorites(userId=request_body["user_id"],vehicleId=vehicle_id)
   db.session.add(vehicle_favorite)
   db.session.commit()
   response_body = {
            "msg": "Vehiculo creado con exito"
            
        }
   return jsonify (response_body), 200

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def create_favorite_character(character_id):
   request_body = request.json
   character_favorite = Favorites(userId=request_body["user_id"],characterId=character_id)
   db.session.add(character_favorite)
   db.session.commit()
   response_body = {
            "msg": "Cáracter creado con exito"
            
        }
   return jsonify (response_body), 200

@app.route('/signup', methods=['POST'])
def create_user():
    request_body = request.json
    user_query = User.query.filter_by(email = request_body["email"]).first()
    if user_query is None:
        create_user = User(email = request_body["email"], password = request_body["password"], is_active = request_body["is_active"],userName = request_body["userName"])
        db.session.add(create_user)
        db.session.commit()
        response_body = {
             "msg": "Usuario creado con exito"
            }
        return jsonify(response_body), 200
    else:
        response_body = {
             "msg": "Usuario ya existe"
            }
        return jsonify(response_body), 404
    
@app.route('/login', methods=['POST'])
def login_user():
    request_body = request.json
    email = request_body.get("email")
    password = request_body.get("password")
    user_login = User.query.filter_by(email = request_body["email"]).first()
    if user_login is None:
        response_body = {
             "msg": "Usuario no existe"
            }
        return jsonify(response_body), 404
    elif email != user_login.email or password != user_login.password:
        return jsonify({"msg": "Usuario o contraseña incorrecta"}), 404
    else:
        return jsonify({ "user_id": user_login.userId })
    
@app.route('/character', methods=['POST'])
def create_character():
    request_body = request.json
    
    character_query = Character.query.filter_by(name=request_body["name"]).first()
    
    if character_query is None:
       
        create_character = Character(
            name=request_body["name"], 
            species=request_body["species"], 
            gender=request_body["gender"], 
            height=request_body.get("height"), 
            weight=request_body.get("weight"), 
            age=request_body.get("age")
        )
        
        db.session.add(create_character)
        db.session.commit()
    
        response_body = {
            "msg": "Personaje creado con éxito"
        }
        return jsonify(response_body), 200
    else:
        
        response_body = {
            "msg": "El personaje ya existe"
        }
        return jsonify(response_body), 409    

@app.route('/vehicle', methods=['POST'])
def create_vehicle():
    request_body = request.json
    
    vehicle_query = Vehicle.query.filter_by(name=request_body["name"]).first()
    
    if vehicle_query is None:
        
        create_vehicle = Vehicle(
            name=request_body["name"], 
            vehicleClass=request_body["vehicleClass"], 
            model=request_body.get("model"),  
            passengers=request_body.get("passengers"), 
            loadCapacity=request_body.get("loadCapacity")
        )
        
        db.session.add(create_vehicle)
        db.session.commit()
        
        response_body = {
            "msg": "Vehículo creado con éxito"
        }
        return jsonify(response_body), 200
    else:
       
        response_body = {
            "msg": "El vehículo ya existe"
        }
        return jsonify(response_body), 409
    
@app.route('/planet', methods=['POST'])
def create_planet():
    request_body = request.json
    
   
    planet_query = Planet.query.filter_by(name=request_body["name"]).first()
    
    if planet_query is None:
        create_planet = Planet(
            name=request_body["name"], 
            population=request_body.get("population"), 
            diameter=request_body.get("diameter"), 
            rotationPeriod=request_body.get("rotationPeriod"), 
            orbitalPeriod=request_body.get("orbitalPeriod"), 
            climate=request_body.get("climate")
        )
        
        db.session.add(create_planet)
        db.session.commit()
        
        response_body = {
            "msg": "Planeta creado con éxito"
        }
        return jsonify(response_body), 200
    else:
    
        response_body = {
            "msg": "El planeta ya existe"
        }
        return jsonify(response_body), 409 





@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
   request_body = request.json
   character_delete_favorite = Favorites.query.filterby(userId=request_body["user_id"],characterId=character_id).first()
   if character_delete_favorite:
     db.session.delete(character_delete_favorite)
     db.session.commit()
     response_body = {
            "msg": "Cáracter eliminado con exito"

        }
     return jsonify (response_body), 200
   else:
    response_body = {
            "msg": "Cáracter no existe"

        }
    return jsonify (response_body), 404
   

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
   request_body = request.json
   planet_delete_favorite = Favorites.query.filterby(userId=request_body["user_id"],planetId=planet_id).first()
   if planet_delete_favorite:
     db.session.delete(planet_delete_favorite)
     db.session.commit()
     response_body = {
            "msg": "planeta eliminado con exito"

        }
     return jsonify (response_body), 200
   else:
    response_body = {
            "msg": "planeta no existe"

        }
    return jsonify (response_body), 404
   
   
   
@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(vehicle_id):
   request_body = request.json
   vehicle_delete_favorite = Favorites.query.filterby(userId=request_body["user_id"],vehicleId=vehicle_id).first()
   if vehicle_delete_favorite:
     db.session.delete(vehicle_delete_favorite)
     db.session.commit()
     response_body = {
            "msg": "CVehículo eliminado con exito"

        }
     return jsonify (response_body), 200
   else:
    response_body = {
            "msg": "Vehículo no existe"

        }
    return jsonify (response_body), 404



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
