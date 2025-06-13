
from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import URL
from lib.models.base import Base
import lib.models
from flask.cli import with_appcontext

import os
from dotenv import load_dotenv


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
class DatabaseConnection:
    
    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        

    def _database_name(self):
        if self.test_mode:
            return os.environ.get("TEST_DATABASE_NAME")
        else:
            return os.environ.get("DEV_DATABASE_NAME")
    
    def _database_url(self):

        db_url = URL.create(
            drivername="postgresql",
            username=os.environ.get("DATABASE_USER"),
            password=os.environ.get("DATABASE_PASSWORD"),
            host=os.environ.get("DATABASE_HOST"),
            database=self._database_name()
        )
        return db_url
    
    def _get_keys(self, app: Flask): 
        """ return public and private keys"""
        config_path = Path(app.root_path)/ 'config'
        private_key_path = os.path.join(app.instance_path, 'private_key.pem')
        public_key_path = os.path.join(config_path, 'public_key.pem')
        
        
        private_key_pem = os.environ.get('PRIVATE_KEY', None)
        if private_key_pem:
            private_key_pem = private_key_pem.encode('utf-8')
        elif os.path.exists(private_key_path):
            with open(private_key_path, 'rb') as f:
                private_key_pem = f.read()
        else:
            raise FileNotFoundError("Private key not found in environment or file system")
        
        if os.path.exists(public_key_path):
            with open(public_key_path, 'rb') as f:
                public_key_pem = f.read()
        
        return private_key_pem, public_key_pem
    
    def _set_keys(self, app):
        """set private and public keys"""
        private_key_pem, public_key_pem = self._get_keys(app)
        
        from joserfc.jwk import RSAKey
        app.config['JWT_PRIVATE_KEY'] = RSAKey.import_key(private_key_pem)
        app.config['JWT_PUBLIC_KEY'] = RSAKey.import_key(public_key_pem)
    
    def configure_app(self, app: Flask):
        """configure a flask app and set up a connection to the database"""
        
        env_path = Path(app.instance_path) / '.env'
        load_dotenv(dotenv_path=env_path)
        if os.environ.get('CI') == 'true':
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = self._database_url()
            
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        # app.config['UPLOAD_FOLDER'] = 'photo_uploads/images'
        app.config['GOOGLE_APPLICATION_CREDENTIALS'] = Path(app.instance_path) / 'storage-uploader-key.json'
        # app.config['SQLALCHEMY_ECHO'] = True
        app.config['ACCESS_TOKEN_EXPIRY'] = 900 # 15 minutes
        app.config['REFRESH_TOKEN_EXPIRY'] = 604800 # 7 days
        app.config['ACCESS_TOKEN_LEEWAY'] = 60 # 1 minute
        app.config['REFRESH_TOKEN_LEEWAY'] = 300 # 5 minutes

        # intialise SQLAlchemy with app
        db.init_app(app)
        
        migrate.init_app(app, db)
        
        self._set_keys(app)
        
        # store ref to the app, lets DatabaseConnection keep track of which app is configured
        # allows other methods in the class to accept app instance if needed
        # enables use of self.app.app_context() 
        self.app = app 
        
        return app
    
    def check_connection(self):
        """Check a flask app has been configured"""
        if self.app is None:
            raise ValueError("No flask app has been configured")
        return self.app
    
    def reset_db(self):
        """Drop db tables and recreate"""
        # with self.app.app_context():
        with db.session.begin():
            db.drop_all()
            db.create_all()
            print("Database has been reset")
    
    def seed_db(self, data):
        """Seed the database"""
        # with self.app.app_context():
        with db.session.begin():
            db.session.add_all(data)
            print(f"Database has been seeded")
    
    