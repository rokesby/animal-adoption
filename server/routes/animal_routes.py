
from flask import Blueprint, request, jsonify, g
from flask_cors import CORS

from lib.models.animal_repository import AnimalRepository
from lib.database_connection import db
from routes.auth import decode_token, token_checker

animal_repo = AnimalRepository(db)
animal_bp = Blueprint('animal', __name__)


# def pet_signup():
#     data= request.get_json()
#     try:
#         pet = create_pet(data)
#         return jsonify({'message': 'Pet successfully registered'}), 201
#     except Exception as e:
#         return jsonify({"message": "Pet could not be registered", "error": str(e)}), 400


@animal_bp.route('', methods=['GET'])
def display_animals():
    animals = animal_repo.get_all_active()
    return jsonify([animal.to_dict() for animal in animals]), 200



@animal_bp.route('/<int:id>', methods= ['GET'])
def display_one_animal(id):
        animal = animal_repo.get_by_id(id)
        return jsonify(animal.to_dict()), 200


# THIS FUNCTION WILL POST A NEW ANIMAL TO THE DATABASE
# TODO : Will I need to change '/listings' to something else? 
@animal_bp.route('', methods=['POST'])
@token_checker # Added this decorator to check for token. 
def create_new_animal():
    data = request.get_json()
    data['shelter_id']=g.shelter_id
    animal = animal_repo.create_new_animal(data)
    return jsonify(animal.to_dict()), 201
   
        # below lines aren't needed until upload is implemented
        # retrieved_animal = db.session.get(Animal, animal.id)
        # retrieved_animal.image = f"unique_id_{retrieved_animal.id}"
        

        # Step b - Save the image into the static folder

        # uploader = FileUploader.FileUploader(
        #     upload_location=os.getenv("PHOTO_UPLOAD_LOCATION"),
        #     allowed_extensions=app.config['UPLOAD_EXTENSIONS']
        # )

        # uploaded_file = request.files['file']
        # success, message = uploader.validate_and_save(uploaded_file)

        # if not success:
        #     return message, 400
        # return jsonify(animal.as_dict()), 201
# @animal_bp.route('/', methods=['OPTIONS'])
# @animal_bp.route('/<int:id>', methods=['OPTIONS'])
# def handle_options(id=None):
#     response = jsonify({})
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#     response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
#     return response
        

# This function allows a logged in user to edit information about a specific animal
@animal_bp.route('/<int:id>', methods=['PUT'])
@token_checker  # Ensures that the user is authenticated
def update_animal(id):
    data = request.get_json()
    print(f"animal data: ${data}")
    animal = animal_repo.update_animal(data)
    if not animal:
        return jsonify({"message": "Animal not found"}), 404
    else:
        return jsonify(animal.to_dict()), 200