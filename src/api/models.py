from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True)

    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.email = email
        self.password = password
        self.is_active = True

    def serialize(self):
        favorites_list = [f.serialize() for f in self.favorites] # Se crea una lista de los favs y despues se llama en el serialize
        return {
            "id": self.id,
            "email": self.email,
            "favorites": favorites_list ## Se manda en el serialize toda la tabla favorites
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(180), unique=False, nullable=False)


    def __init__(self, name, description):
        self.name = name
        self.description = description

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(80), unique=False, nullable=False)


    def __init__(self, name, climate):
        self.name = name
        self.climate = climate

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            # do not serialize the password, its a security breach
        }

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) ## id referencia
    people_id = db.Column(db.Integer, db.ForeignKey('people.id')) ## id referencia
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))  
    
    user = db.relationship('User', backref='favorites') # relacion tabla
    planet = db.relationship('Planet', lazy='joined', backref='favorites')
    people = db.relationship('People', lazy='joined', backref='favorites')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people": self.people.serialize() if self.people else None, # Si el personaje existe devuelve todos los datos
            "planet": self.planet.serialize() if self.planet else None  # Si el planeta existe devuelve todos los datos
        }
