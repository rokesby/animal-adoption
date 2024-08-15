from flask import Flask, request, render_template, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


from db.database_connection import db_session
from db.seed import Animal, Shelter, User

from dotenv import load_dotenv
import os


# Create a new Flask app
app = Flask(__name__)

CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_CONNECT")
db = SQLAlchemy(app)


class Animal(db.Model):
    __tablename__ = 'animals'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    species = db.Column(db.String(50))
    age = db.Column(db.Integer)
    breed = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    male = db.Column(db.Boolean, nullable=False)
    bio = db.Column(db.String(500), nullable=False)
    neutered = db.Column(db.Boolean, nullable=False)
    lives_with_children = db.Column(db.Boolean, nullable=False)
    shelter_id = db.Column(db.Integer(), db.ForeignKey('shelters.id'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)

    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    shelter_id = db.Column(db.Integer, db.ForeignKey('shelters.id'), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Shelter(db.Model):
    __tablename__ = 'shelters'

    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

    animals = db.relationship('Animal', backref='shelter', lazy=True)
    # animals = relationship('Animal', backref='shelter')
    # users = relationship('User', backref='shelter')
    users = db.relationship('User', backref='shelter', lazy=True)



# == Routes Here ==

# # Login route - get users
# @app.route('/users', methods=['GET'])
# def display_users():
#     # connection = get_flask_database_connection(app)
#     # class AnimalsResource(Resource)
#     return render_template('users.html', Users=Users)


# Listings route - return a list of Animals.
# @app.route('/signup', methods=['POST'])
# def create_new_users():

#     #with db_session() as db:
#     with app.app_context():
#         # Extract and validate input data
#         data = request.get_json()
#         first_name = data.get('first_name')
#         last_name = data.get('last_name')
#         email = data.get('email')
#         password = data.get('password')
#         shelter_id = int(data.get('shelter_id'))
#     user = User(
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             password=password,
#             shelter_id=shelter_id,
#         )
#     db.session.add(user)
#     db.session.commit()
@app.route('/signup', methods=['POST'])
def create_new_users():
    data = request.json

    shelter_id = data.get('shelter_id')
    if not shelter_id or not isinstance(shelter_id, int):
        return jsonify({"error": "Invalid shelter ID"}), 400

    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data['password'],
        shelter_id=data['shelter_id']
    )

    db.session.add(user)
    db.session.commit()

    return jsonify(user.as_dict()), 201
    # user = User(
        #     first_name=request.json['first_name'],
        #     last_name=request.json['last_name'],
        #     email=request.json['email'],
        #     password=request.json['password'],
        #     shelter_id=request.json['shelter_id']
        # )
        # db.session.add(user)
        # db.session.commit()
        # return jsonify(user.as_dict())
    
@app.route('/listings', methods=['GET'])
def display_animals():

    #with db_session() as db:
    with app.app_context():
        #animals = db.query(Animal).all()
        animals = Animal.query.all()
        animals_to_json = []
        for animal in animals:
            animals_to_json.append(animal.as_dict())
        return jsonify(animals_to_json)
            # print({'Animal': animal.name})
        # return render_template('listings.html', animals=animals)
    
# Test JSON route
@app.route('/profile')
def my_profile():
    response_body = {
        "name": "Nagato",
        "about" :"Hello! I'm a full stack developer that loves python and javascript"
    }

    return response_body

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True)