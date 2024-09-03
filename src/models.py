from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    userId = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    user_favorites = db.relationship('Favorites', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.userId,
            "email": self.email,
            "username": self.userName,
        }
class Character(db.Model):
    __tablename__ = 'character'
    characterId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    species = db.Column(db.String(25), nullable=False)
    gender = db.Column(db.String(25), nullable=False)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    age = db.Column(db.Integer)

    character_favorites = db.relationship('Favorites', backref='character', lazy=True)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.characterId,
            "species": self.species,
            "name": self.name,
            "gender": self.gender,
            "name": self.gender,
            "height": self.height,
            "weight": self.weight,
            "age": self.age,
        }
    

class Planet(db.Model):
    __tablename__ = 'planet'
    planetId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    population = db.Column(db.Integer)
    diameter = db.Column(db.Integer)
    rotationPeriod = db.Column(db.Integer)
    orbitalPeriod = db.Column(db.Integer)
    climate = db.Column(db.String(25))

    planet_favorites = db.relationship('Favorites', backref='planet', lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.planetId,
            "name": self.name,
            "population": self.population,
            "gender": self.gender,
            "diameter": self.diameter,
            "rotationPeriod": self.rotationPeriod,
            "orbitalPeriod": self.orbitalPeriod,
            "climate": self.climate,
        }

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    vehicleId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    vehicleClass = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(25))
    passengers = db.Column(db.Integer)
    loadCapacity = db.Column(db.Integer)

    vehicle_favorites = db.relationship('Favorites', backref='vehicle', lazy=True)       

    def __repr__(self):
        return '<Vehicle %r>' % self.vehicle

    def serialize(self):
        return {
            "id": self.vehicleId,
            "name": self.name,
            "vehicleClass": self.vehicleClass,
            "model": self.model,
            "passenger": self.passengers,
            "LoadCapacity": self.loadCapacity,
        
        }
class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    characterId = db.Column(db.Integer, db.ForeignKey('character.characterId'), nullable=False)
    planetId = db.Column(db.Integer, db.ForeignKey('planet.planetId'), nullable=False)
    vehicleId = db.Column(db.Integer, db.ForeignKey('vehicle.vehicleId'), nullable=False)


    def to_dict(self):
        return {
            "id":self.id,
            "userID":self.userId,
            "characterId":self.characterId,
            "planetId": self.planetId,
            "vehicleId": self.vehicleId,

        }
