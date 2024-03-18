from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username
            # do not serialize the password, its a security breach
        }
    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    char_name = db.Column(db.String(120), unique=True, nullable=False)
    char_description = db.Column(db.String(240), unique=False, nullable=False)
    char_img_url = db.Column(db.String(240), unique=False, nullable=True)
    char_habitat = db.Column(db.Integer, db.ForeignKey('habitat.id'), nullable=False)
    habitat = db.relationship('Habitat', backref='character', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "character_name": self.char_name,
            "char_description": self.char_description,
            "char_habitat_id": self.char_habitat,
            "char_img_url": self.char_img_url
        }

class Habitat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habitat_name = db.Column(db.String(120), unique=True, nullable=False)
    habitat_description = db.Column(db.String(240), unique=False, nullable=False)

    def __repr__(self):
        return '<Habitat %r>' % self.habitat_name
    
    def serialize(self):
        return {
            "id": self.id,
            "habitat_name": self.habitat_name,
            "habitat_description": self.habitat_description
            # do not serialize the password, its a security breach
        }
    
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fav_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    habitat_id = db.Column(db.Integer, db.ForeignKey('habitat.id'), nullable=True)
    habitat = db.relationship('Habitat', backref='favorites', lazy=True)

