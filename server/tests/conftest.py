from flask import Flask, jsonify
import pytest
from lib.database_connection import DatabaseConnection, db
from lib.models import Shelter, User, Animal
from lib.models.animal_repository import AnimalRepository


# https://docs.pytest.org/en/stable/how-to/fixtures.html
# This is a Pytest fixture.
# It creates an object that we can use in our tests.
# We will use it to create a database connection.


from app import create_app, bcrypt

@pytest.fixture
def app():
    # Create a new Flask app for testing
    app = create_app(test_config={'TESTING': True})
    return app
    
@pytest.fixture
def db_connection(app: Flask):
    # Create a new DatabaseConnection instance in test mode
    conn = DatabaseConnection(test_mode=True)
    conn.configure_app(app)
    
    with app.app_context():
        conn.reset_db()
    return conn
# use a pytest fixture to push a context for a specific test.
@pytest.fixture
def app_ctx(app):
    with app.app_context():
        yield

@pytest.fixture
def client(app):
    # app.config['TESTING'] = True 
    with app.test_client() as client:
        yield client

@pytest.fixture
def test_user(app_ctx):
    hashed_password = bcrypt.generate_password_hash('V@lidp4ss').decode('utf-8') 
    test_user = User(email = "Unique_test1@example.com",password = hashed_password,first_name = "Unique_test",last_name = "user",shelter = Shelter(name = "Example Shelter",location = "South London",email = "info@example.com",phone_number = "07123123123"))
    
    db.session.add(test_user)
    db.session.commit()
    
    yield test_user
    db.session.delete(test_user)
    db.session.commit()

@pytest.fixture
def animal_repository(app, db_connection):
    test_shelter = Shelter(
    name = "Example Shelter",
    location = "South London",
    email = "info@example.com",
    phone_number = "07123123123"
)
    test_animals = [
        Animal(
            name="Test One",
            species="cat",
            age=1,
            breed="Maine Coon",
            location="London",
            male=True,
            bio="This is a test cat.",
            neutered=False,
            lives_with_children=False,
            images=1,
            isActive=True,
            shelter=test_shelter
        ),
        Animal(
            name="Test Two",
            species="dog",
            age=2,
            breed="test breed",
            location="London",
            male=True,
            bio="This is a test dog.",
            neutered=False,
            lives_with_children=False,
            images=1,
            isActive=True,
            shelter=test_shelter
        ),
        Animal(
            name="Test Three",
            species="wolf",
            age=3,
            breed="werewolf",
            location="London",
            male=True,
            bio="This is a test werewolf.",
            neutered=False,
            lives_with_children=False,
            images=1,
            isActive=False,
            shelter=test_shelter
        )
    ]
    with app.app_context():
        db_connection.seed_db(test_animals)
    
    repo = AnimalRepository(db)
    return repo, test_animals
