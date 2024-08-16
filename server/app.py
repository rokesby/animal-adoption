from flask import Flask, request, render_template, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from db.database_connection import db_session
from db.seed import Animal, Shelter, User
from functools import wraps
from controllers.auth import generate_token, decode_token

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

        def as_dict(self):
            return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
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

    with app.app_context():
        animals = Animal.query.all()
        animals_to_json = [animal.as_dict() for animal in animals]
        return jsonify(animals_to_json)


@app.route('/listings/<int:id>', methods= ['GET'])
def display_one_animal(id):
    with app.app_context():
        animal = Animal.query.get(id)
        return jsonify(animal.as_dict())

# THIS FUNCTION WILL POST A NEW ANIMAL TO THE DATABASE

# Will I need to change '/listings' to something else? 
@app.route('/listings', methods=['POST'])
def create_new_animal():
    with app.app_context():

        data = request.get_json()
        print('Received the data:', data)
        # data= request.json
        animal = Animal(
            name=data['name'],
            species=data['species'],
            age=data['age'],
            breed=data['breed'],
            location=data['location'],
            male=data['male'],
            bio=data['bio'],
            neutered=data['neutered'],
            lives_with_children=data['lives_with_children'],
            shelter_id=data['shelter_id']
        )

        db.session.add(animal)
        db.session.commit()

        return jsonify(animal.as_dict()), 201


@app.route('/users', methods=['GET'])
def get_users():
    with app.app_context():
        users = User.query.all()
        users_list = [user.as_dict() for user in users]
        return jsonify(users_list)
    
@app.route('/login', methods=['GET'])
def get_user_by_id():
    with app.app_context():
        req_email = request.headers.get('email')
        req_password = request.headers.get('password')
        user = User.query.filter_by(email=req_email).first()
        if not user:
            return jsonify({"error": "User not found"}), 401
        elif user.password == req_password:
            return jsonify(user.as_dict()), 200
        else:
            return jsonify({"error": "Password is incorrect"}), 401
            
# @app.route('/login', methods=['POST'])
# def login():
#     # Assume you validate the user's credentials and get the user_id
#     user_id = "some_user_id"  # Replace with actual user ID
#     token = generate_token(user_id)

#     return jsonify({"token": token.decode('utf-8')}), 200

    

# Test JSON route
@app.route('/profile')
def my_profile():
    response_body = {
        "name": "Nagato",
        "about" :"Hello! I'm a full stack developer that loves python and javascript"
    }

    return response_body

# decorator function used for sake of DRY
def token_checker(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header:
            # Assuming the token is in the format "Bearer <token>"
            token = auth_header.split(" ")[1]
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            payload = decode_token(token)
            request.user_id = payload.get('user_id')
        except Exception as e:
            return jsonify({"message": "Invalid or expired token!"}), 401

        return f(*args, **kwargs)

    return decorated_function

# test protected route
@app.route('/protected', methods=['GET'])
@token_checker
def protected_route():
    return jsonify({"message": f"Access granted, user_id: {request.user_id}"}), 200

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True)