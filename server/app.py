from flask import Flask, request, render_template, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from db.database_connection import db_session
from db.seed import Animal, Shelter, User
from functools import wraps
from controllers.auth import generate_token, decode_token
from flask_bcrypt import Bcrypt 

# Photo upload
from werkzeug.utils import secure_filename
from flask import url_for
import imghdr # TODO  - remove and cleanup.
from flask import send_from_directory
from flask import abort
import FileUploader
# End photo upload.

from dotenv import load_dotenv
import os

# Create a new Flask app
app = Flask(__name__)
# Encryption with Bcrypt
bcrypt = Bcrypt(app) 

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
    # shelter = db.relationship('Shelter', backref='animals', lazy=True)

    def as_dict(self):
        animal_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        shelter_info = Shelter.query.get(self.shelter_id)

        animal_dict['shelter'] = {
            'name': shelter_info.name,
            'location': shelter_info.location,
            'email': shelter_info.email,
            'phone_number': shelter_info.phone_number
        }
        return animal_dict

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


# decorator function used for sake of DRY
def token_checker(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header:
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

# Listings route - return a list of all animals.
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
        return jsonify(animal.as_dict()), 200


# THIS FUNCTION WILL POST A NEW ANIMAL TO THE DATABASE

# Will I need to change '/listings' to something else? 
@app.route('/listings', methods=['POST'])
@token_checker # Added this decorator to check for token. 
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

# This function allows a logged in user to edit information about a specific animal
@app.route('/listings/<int:id>', methods=['PUT'])
@token_checker  # Ensures that the user is authenticated
def update_animal(id):
    with app.app_context():

        data = request.get_json()
        print('Received the data:', data)
        animal = Animal.query.get(id)
        if not animal:
            return jsonify({"message": "Animal not found"}), 404

        # Update the animal's attributes with the new data
        animal.name = data.get('name', animal.name)
        animal.species = data.get('species', animal.species)
        animal.age = data.get('age', animal.age)
        animal.breed = data.get('breed', animal.breed)
        animal.location = data.get('location', animal.location)
        animal.male = data.get('male', animal.male)
        animal.bio = data.get('bio', animal.bio)
        animal.neutered = data.get('neutered', animal.neutered)
        animal.lives_with_children = data.get('lives_with_children', animal.lives_with_children)
        animal.shelter_id = data.get('shelter_id', animal.shelter_id)

        db.session.commit()

        return jsonify(animal.as_dict()), 200



@app.route('/users', methods=['GET'])
def get_users():
    with app.app_context():
        users = User.query.all()
        users_list = [user.as_dict() for user in users]
        return jsonify(users_list)
    
@app.route('/token', methods=['POST'])
def login():
    with app.app_context():
        data = request.get_json()
        req_email = data.get('email')
        req_password = data.get('password')
        user = User.query.filter_by(email=req_email).first()
        if not user:
            return jsonify({"error": "User not found"}), 401
        elif bcrypt.check_password_hash(user.password, req_password):
            token_data = {
            "id": user.id,
            "shelter_id": user.shelter_id
            }
            token = generate_token(req_email, token_data) #generate token here 
            data = decode_token(token) # decode token 
            return jsonify({"token": token.decode('utf-8'), "user_id": data.get('id'), "shelter_id": data.get('shelter_id')}), 200
        else:
            return jsonify({"error": "Password is incorrect"}), 401

# This function adds a new user to the database
@app.route('/sign-up', methods=['POST'])
def signup():
    with app.app_context():
        data = request.get_json()
        print('Received the data:', data)
        req_email = data.get('email')
        # Password hashing happens here
        plaintext_password = data['password']
        hashed_password = bcrypt.generate_password_hash(plaintext_password).decode('utf-8') 

        user = User(
            email=data['email'],
            password=hashed_password,
            first_name=data['first_name'],
            last_name=data['last_name'],
            shelter_id=data['shelter_id']
        )
        db.session.add(user)
        db.session.commit()
        token_data = {
            "id": user.id,
            "shelter_id": user.shelter_id
            }
        token = generate_token(req_email, token_data)
        data = decode_token(token)
        return jsonify({"token": token.decode('utf-8'), "user_id": data.get('id'), "shelter_id": data.get('shelter_id')}), 201
        # return jsonify(user.as_dict()), 201

        

############ Photo Upload.

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'

# TODO Specify GET?
# Test to allow system admin to view files.
@app.route('/upload', methods=['GET'])
def upload_form():
    file_listing = os.listdir(os.getenv("PHOTO_UPLOAD_LOCATION"))
    return render_template('upload.html', file_listing = file_listing)

@app.route('/upload', methods=['POST'])
def upload_files():
    uploader = FileUploader.FileUploader(
        upload_location=os.getenv("PHOTO_UPLOAD_LOCATION"),
        allowed_extensions=app.config['UPLOAD_EXTENSIONS']
    )

    uploaded_file = request.files['file']
    success, message = uploader.validate_and_save(uploaded_file)

    if not success:
        return message, 400
    return '', 204

@app.route('/upload/<filename>')
def upload(filename):
    return send_from_directory(os.getenv("PHOTO_UPLOAD_LOCATION"), filename)


# Validator for Dropzone js component.
@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413


############ End Photo Upload

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