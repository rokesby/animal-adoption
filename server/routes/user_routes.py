
import uuid
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from lib.database_connection import db, flask_bcrypt
from lib.services.auth import generate_token
from lib.models.auth_repository import AuthRepository
from lib.models import User
from lib.models.user_repository import UserRepository
from helpers.helpers import generate_pin
from lib.models.shelter_repository import ShelterRepository
from lib.models.verification_repository import VerificationRepository
from utils.sendgrid_api_client import send_verification_email

user_bp = Blueprint('user_bp', __name__)
auth_repository = AuthRepository(db, flask_bcrypt)
user_repository = UserRepository(db)
shelter_repository = ShelterRepository(db)
verification_repository = VerificationRepository(db)

# This function adds a new user to the database
@user_bp.route('/sign-up', methods=['POST'])
@cross_origin(supports_credentials=True)
def signup():
    # with app.app_context():
    data = request.get_json()
    req_email = data['email']
    plaintext_password = data['password']
    hashed_password = flask_bcrypt.generate_password_hash(plaintext_password).decode('utf-8') 
    data['password'] = hashed_password
    
    domain = req_email.split('@')[1]
    
    data['shelter_id'] = shelter_repository.get_shelter_id_by_domain(domain)
    
    user = user_repository.create_user(data)
    
    plain_pin, hashed_pin = generate_pin()
    
    verification = verification_repository.add_verification(user.id, hashed_pin)

    verification_token = generate_token(verification.id, token_type='verification')
    
    send_grid_status_code = send_verification_email(user.email, plain_pin, verification_token)
    
    if send_grid_status_code == 202:
        return jsonify({"message": "Check your email to verify your account"}), 201
    else:
        return jsonify({"error": "Failed to send verification email"}), 500

