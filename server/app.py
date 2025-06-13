from pathlib import Path
import time
import click
from flask import Blueprint, Flask, request, jsonify, send_from_directory
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from sqlalchemy import select
from db.seed import Animal, User, users, animals
from routes.auth import generate_token
from flask_bcrypt import Bcrypt 
from lib.database_connection import DatabaseConnection, db
from routes.animal_routes import animal_bp
from routes.auth_routes import auth_bp
# from dotenv import load_dotenv
import os

# Photo upload
# from werkzeug.utils import secure_filename
# import FileUploader
# End photo upload.



app_dir = Path(os.path.dirname(os.path.abspath(__file__)))
print(f'app path:{app_dir}')

def create_app(test_config=None, instance_relative_config=True, static_folder='static'):
    """Create and configure the Flask app"""
    app = Flask(__name__)
    
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Configure the app
    if test_config is None:
        # Load the default configuration
        conn = DatabaseConnection()
        conn.configure_app(app)
    else:
        # Load the test configuration
        app.config.update(test_config)
    # Register blueprints
    app.register_blueprint(animal_bp, url_prefix='/listings')
    app.register_blueprint(auth_bp)
    
    # # Define routes
    
    # Other routes and configurations
    
    @app.route('/api/assets/images/<int:id>')
    def get_profile_image(id):
        directory = f"{app.config['UPLOAD_FOLDER']}/{id}"
        if not os.path.isdir(directory):
            return f"Directory {directory} not found", 404
        try:
            assets = [file for file in os.listdir(directory)]
            profile_images = list(filter(lambda filename: filename.lower().startswith("profile"), assets))
            profile_image = profile_images[0]
            
            if not profile_image:
                return "Profile image not found", 404
            
            return send_from_directory(directory, profile_image), 200

        except Exception as e:
            return "Error serving image", 500
    
    return app

# Create the app for production use
app = create_app()


CORS(app,
     origins=["http://localhost:5173"],
     supports_credentials=True)

# Encryption with Bcrypt
bcrypt = Bcrypt(app) 

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Drop db tables and recreate"""
    with db.session.begin():
        db.drop_all()
        db.create_all()
        click.echo("Database has been created")
        
@click.command('seed-db')
@with_appcontext
def seed_db_command():
    """Drop db tables and recreate"""
    with db.session.begin():
        db.session.add_all(animals)
        db.session.add_all(users)
        click.echo("Database has been seeded")

@click.command()
@with_appcontext
def current_time():
    """Show current UTC unix timestamp"""
    timestamp = int(time.time())
    click.echo(f"UTC Unix timestamp: {timestamp}")

app.cli.add_command(current_time)
app.cli.add_command(init_db_command)
app.cli.add_command(seed_db_command)

# ------------------------------------

# == Routes Here ==
# This backend function allows a user to update the isActive field in the database 
# This is mainly used when the user wants to 'hide' an animal profile by setting isActive to false

# @app.route('/<int:id>/change_isactive', methods=['PUT'])
# @token_checker 
# def update_is_active(id):
#     with app.app_context():
#         animal = Animal.query.get(id)
#         if not animal:
#             return jsonify({"message": "Animal not found"}), 404
        
#         data = request.get_json()
#         animal.isActive = data.get('isActive', animal.isActive)
        
#         db.session.commit()
#         return jsonify(animal.as_dict()), 200
    


# This function adds a new user to the database
@app.route('/api/sign-up', methods=['POST'])
@cross_origin(supports_credentials=True)
def signup():
    with app.app_context():
        data = request.get_json()
        req_email = data.get('email')
        plaintext_password = data['password']
        hashed_password = bcrypt.generate_password_hash(plaintext_password).decode('utf-8') 

        # Shelter_id assignment via email domain name happens here
        # shelter_id = None
        # for domain, id in email_to_shelter_mapping.items():
        #     if domain in req_email:
        #         shelter_id = id
        #         break

        #     if shelter_id is None:
        #         return jsonify({'error': 'You do not have a registered animal shelter email'}), 400

        user = User(
            email=data['email'],
            password=hashed_password,
            first_name=data['first_name'],
            last_name=data['last_name'],
            shelter_id = data['shelter_id']
        )
        db.session.add(user)
        db.session.commit()
        token_data = {
            "id": user.id,
            "shelter_id": user.shelter_id
            }
        access_token = generate_token(req_email, token_data, token_type='access', expiry=900) 
        refresh_token = generate_token(req_email, {"token_type": "refresh"}, token_type='refresh', expiry=604800) 
        response = jsonify({"token": access_token,
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
                            path='/',
                            )
        return response, 201

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True)
    
############ Photo Upload.

# app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
# app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
# app.config['UPLOAD_PATH'] = 'uploads'

# # Test to allow system admin to view files.
# @app.route('/upload', methods=['GET'])
# def upload_form():
#     file_listing = os.listdir(os.getenv("PHOTO_UPLOAD_LOCATION"))
#     return render_template('upload.html', file_listing = file_listing)

# @app.route('/upload', methods=['POST'])
# def upload_files():
#     uploader = FileUploader.FileUploader(
#         upload_location=os.getenv("PHOTO_UPLOAD_LOCATION"),
#         allowed_extensions=app.config['UPLOAD_EXTENSIONS']
#     )

#     uploaded_file = request.files['file']
#     success, message = uploader.validate_and_save(uploaded_file)

#     if not success:
#         return message, 400
#     return '', 204

# 
# @app.route('/upload/<filename>')
# def upload(filename):
#     return send_from_directory(os.getenv("PHOTO_UPLOAD_LOCATION"), filename)

# # Validator for Dropzone js component.
# @app.errorhandler(413)
# def too_large(e):
#     return "File is too large", 413

############ End Photo Upload