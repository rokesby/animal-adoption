
import time
import uuid
import bcrypt
from flask import Blueprint, current_app, jsonify, request
from flask_cors import cross_origin
from lib.database_connection import db, flask_bcrypt
from lib.services.auth import decode_token, generate_token, token_checker, validate_token
from lib.models.auth_repository import AuthRepository
from lib.models import User
from lib.models.user_repository import UserRepository
from lib.models.verification_repository import VerificationRepository
from helpers.helpers import generate_pin
from utils.sendgrid_api_client import send_verification_email

auth_bp = Blueprint('auth_bp', __name__)
auth_repository = AuthRepository(db, flask_bcrypt)
user_repository = UserRepository(db)
verification_repository = VerificationRepository(db)

@auth_bp.route('/protected', methods=['GET'])
@token_checker
def protected_route():
    return jsonify({"message": f"Access granted, user_id: {request}"}), 200

@auth_bp.route('/token', methods=['POST'])
def login():
    data = request.get_json()
    user_email = data['email']
    user = user_repository.get_user_by_email(user_email)
    
    if not user:
            return jsonify({"error": "Email or password is incorrect"}), 401
    
    if user is not None:
        if user.verified == True:
            token = auth_repository.get_token(data)
            return token
        else:
            return jsonify({"error": "Please verify your account"}), 403
        

@auth_bp.route('/logout', methods=['POST'])
@cross_origin(supports_credentials=True)
def logout():
    response = jsonify({"message": "logged out successfully"})
    response.delete_cookie('refresh_token', path='/')
    return response, 200

@auth_bp.route('/refresh-token', methods=['POST'])
@cross_origin(supports_credentials=True)
def refresh_token():
    refresh_token = request.cookies.get('refresh_token')
    response, status_code = auth_repository.get_access_token(refresh_token)
    return response, status_code

@auth_bp.route('/verify', methods=['POST'])
@cross_origin(supports_credentials=True)
def verify():
    data = request.get_json()
   
    pin = data.get('pin')
    token = data.get('token')
    decoded_token_claims = decode_token(token).claims
    
    try:
        validate_token(decoded_token_claims)
    except:
        return jsonify({"message": "Invalid or expired token"}), 400
   
    
    verification_id = uuid.UUID(decoded_token_claims.get('sub'))
    
    verification = verification_repository.get_verification_by_id(verification_id)
    
    if not verification or verification.expires_at < int(time.time()):
        return jsonify({"message": "Cannot validate"}), 400
    
    if verification:
        if flask_bcrypt.check_password_hash(verification.pin_hash, pin) == True:
            user_id = verification.user_id
            verification_repository.update_verification_used_at(verification_id)
            user_repository.update_user(user_id, {"verified": True})
            return jsonify({"message": "success"}), 200
        else:
            return jsonify({"error": "invalid pin"}), 400
    
@auth_bp.route('/reverify', methods=['POST'])
def reVerify():
    data = request.get_json()
    email = data['email']
    user = user_repository.get_user_by_email(email)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    if user.verified == True:
        return jsonify({"error": "User is already verified"}), 500
    
    plain_pin, hashed_pin = generate_pin()
    
    verification = verification_repository.add_verification(user.id, hashed_pin)

    verification_token = generate_token(verification.id, token_type='verification')
    
    send_grid_status_code = send_verification_email(user.email, plain_pin, verification_token)
    
    if send_grid_status_code == 202:
        return jsonify({"message": "Check your email to verify your account"}), 200
    else:
        return jsonify({"error": "Failed to send verification email"}), 500
    