from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from lib.models.user import User
from lib.services.auth import decode_token, generate_token

class AuthRepository:
    def __init__(self, db_instance: SQLAlchemy, bcrypt_instance):
        self.db = db_instance
        self.flask_bcrypt = bcrypt_instance
        
    def get_token(self, data):
        
        req_email = data.get('email')
        req_password = data.get('password')
        user = self.db.session.scalar(select(User).filter_by(email=req_email))
        if not user:
            return jsonify({"error": "Email or password is incorrect"}), 401
        elif self.flask_bcrypt.check_password_hash(user.password, req_password):
            token_data = {
            "id": user.id,
            "shelter_id": user.shelter_id
            }
            access_token = generate_token(user.id, additional_claims=token_data, token_type='access') 
            refresh_token = generate_token(user.id, token_type='refresh') 
            # 604800 = 1
            response = jsonify({"token": access_token,
                                # Why not just store this in state?
                            "user": {
                                "id": user.id,
                                "shelter_id": user.shelter_id
                                },
                            })
            response.set_cookie('refresh_token',
                                refresh_token,
                                httponly=True,
                                secure=False, # set to True in Prod
                                samesite='Lax',
                                max_age=604800,
                                path='/'
                                )
            return response, 200
        else:
            return jsonify({"error": "Email or password is incorrect"}), 401
    
    def get_access_token(self, refresh_token):
        if not refresh_token:
            print("No refresh token provided in request")
            return jsonify({"error": "No refresh_token provided"}), 401
        try:
            # This should be validated before - decode_token throws NONE if there's an issue
            decoded = decode_token(refresh_token)
            print(f"decoded refresh = ${decoded} ")
            
            user_id = decoded.claims.get("sub")
            print(f"user id: {user_id}")
            user = self.db.session.scalar(select(User).filter_by(id=user_id))
            
            if not user:
                return jsonify({"error": "User not found"}), 401
            
            token_data = {
            "id": user.id,
            "shelter_id": user.shelter_id
            }
            
            access_token = generate_token(user.id, token_data) 
            refresh_token = generate_token(user.id, {"token_type": "refresh"}, token_type='refresh') 
            
            response = jsonify({"token": access_token,
                                # bring this into claims and/or store in state
                            "user": {
                                "id": user.id,
                                "shelter_id": user.shelter_id
                                },
                            })
            response.set_cookie('refresh_token',
                                refresh_token,
                                httponly=True,
                                secure=False, # set to True in Prod
                                samesite='Lax',
                                max_age=604800,
                                path='/'
                                )
            return response, 200
        
        except Exception as e:
            print(f"Refresh token error: {e}")
            return jsonify({"error": "Invalid or expired refresh token"}), 401
        