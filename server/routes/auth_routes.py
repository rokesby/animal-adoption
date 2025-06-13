
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from lib.database_connection import db
from routes.auth import decode_token, generate_token, token_checker
from lib.models.auth_repository import AuthRepository


auth_bp = Blueprint('auth_bp', __name__)
auth_repository = AuthRepository(db)

@auth_bp.route('/token', methods=['POST'])
def login():
    data = request.get_json()
    token = auth_repository.get_token(data)
    return token

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
    
@auth_bp.route('/protected', methods=['GET'])
@token_checker
def protected_route():
    return jsonify({"message": f"Access granted, user_id: {request}"}), 200
