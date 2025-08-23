
from flask import Blueprint, request, jsonify, g
from flask_cors import CORS

from lib.models.animal_repository import AnimalRepository
from lib.database_connection import db
from lib.services.auth import decode_token, token_checker
from utils.gcp_client import GCSImageStorage, get_gcs_public_config
from utils.upload_util import upload_images
from utils.image_validator import check_image_validity

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



@animal_bp.route('/<uuid:id>', methods=['GET'])
def display_one_animal(id):
    animal = animal_repo.get_by_id(id)
    print(f'animal_data: {animal}')
    return jsonify(animal.to_dict()), 200
    
@animal_bp.route('/<uuid:id>/images', methods=['GET'])
def get_images(id):
    config = get_gcs_public_config()
    storage_client = GCSImageStorage(config['bucket_name'])
    animal_image_list = storage_client.list_animal_images(id)
    return animal_image_list, 200



@animal_bp.route('', methods=['POST'])
@token_checker # Added this decorator to check for token. 
def create_new_animal():
    data = request.get_json()
    data['shelter_id']=g.shelter_id
    animal = animal_repo.create_new_animal(data)
    return jsonify(animal.to_dict()), 201
        

# This function allows a logged in user to edit information about a specific animal
@animal_bp.route('/<uuid:id>', methods=['PATCH'])
@token_checker  # Ensures that the user is authenticated
def update_animal(id):
    data = request.get_json()
    data["id"] = id
    
    animal = animal_repo.get_by_id(id)
    
    if not animal:
        return jsonify({"error": "Animal not found"}), 404
    
    elif animal.shelter_id == g.shelter_id:
        updated_animal = animal_repo.update_animal(data)
        if not updated_animal:
            return jsonify({"error": "something went wrong"}), 500
        else:
            return jsonify(updated_animal.to_dict()), 200
    else:
        return jsonify({"error": "You do not have permission to update this animal"}), 403
    
@animal_bp.route('/<uuid:id>/upload-images', methods=['POST'])
@token_checker
def upload_animal_images(id):

    files = request.files
    fileList = files.getlist('file')
    valid_files, invalid_files = check_image_validity(fileList)
    print(f"valid files: {valid_files}")
    print(f"invalid files: {invalid_files}")
    response = upload_images(valid_files, id)

    return response