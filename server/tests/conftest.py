from datetime import datetime
import time
import uuid
from flask import Flask, jsonify
import pytest
from lib.database_connection import DatabaseConnection, db, flask_bcrypt
from lib.models import Shelter, User, Animal, Message, Conversation
from lib.models.animal_repository import AnimalRepository
from lib.models.message_repository import MessageRepository
from lib.models.conversation_repository import ConversationRepository
from app import create_app
from lib.models.user_repository import UserRepository
from lib.models.shelter_repository import ShelterRepository
from lib.models.verification_repository import VerificationRepository
from lib.models.verification import Verification

# https://docs.pytest.org/en/stable/how-to/fixtures.html
# This is a Pytest fixture.
# It creates an object that we can use in our tests.
# We will use it to create a database connection.

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
    hashed_password = flask_bcrypt.generate_password_hash('V@lidp4ss').decode('utf-8') 
    test_user = User(email = "Unique_test1@example.com",password = hashed_password,first_name = "Unique_test",last_name = "user", verified=True, shelter = Shelter(name = "Example Shelter",location = "South London",email = "info@example.com",domain = "example.com", phone_number = "07123123123"))
    
    db.session.add(test_user)
    db.session.commit()
    
    yield test_user
    db.session.delete(test_user)
    db.session.commit()
    
def test_public_user(app_ctx):
    hashed_password = flask_bcrypt.generate_password_hash('V@lidp4ss').decode('utf-8') 
    test_public_user = User(email = "Unique_test2@example333.com",password = hashed_password,first_name = "Unique_test",last_name = "user", verified=True)
    
    db.session.add(test_public_user)
    db.session.commit()
    
    yield test_public_user
    db.session.delete(test_public_user)
    db.session.commit()

@pytest.fixture
def auth_user(mocker):
    def _auth_user(user_id=1,shelter_id=1, **claims):
        iat = int(time.time()) - 100
        exp = int(time.time()) + 900
        mock_token = mocker.Mock()
        mock_token.claims = {
            "iss": "pawsforacause",
            "sub": user_id,
            "iat": iat,
            "exp": exp,
            "token_type": "access",
            "shelter_id": shelter_id
        }
        mocker.patch('lib.services.auth.decode_token', return_value=mock_token)
        mocker.patch('lib.services.auth.validate_token', return_value=None)
        return mock_token
    return _auth_user

@pytest.fixture
def auth_non_shelter_user(mocker):
    def _auth_user(user_id=1, **claims):
        iat = int(time.time()) - 100
        exp = int(time.time()) + 900
        mock_token = mocker.Mock()
        mock_token.claims = {
            "iss": "pawsforacause",
            "sub": user_id,
            "iat": iat,
            "exp": exp,
            "token_type": "access",
        }
        mocker.patch('lib.services.auth.decode_token', return_value=mock_token)
        mocker.patch('lib.services.auth.validate_token', return_value=None)
        return mock_token
    return _auth_user

@pytest.fixture  
def no_auth(mocker):
    """Mock failed authentication"""
    mocker.patch('lib.services.auth.decode_token', side_effect=Exception("Invalid token"))
    

@pytest.fixture
def animal_repository(app_ctx, db_connection: DatabaseConnection):
    test_shelter = Shelter(
    name = "Example Shelter",
    location = "South London",
    email = "info@example.com",
    domain = "example.com",
    phone_number = "07123123123"
)
    test_shelter_2 = Shelter(
    name = "Example Shelter 2",
    location = "North London",
    email = "info@example2.com",
    domain = "example2.com",
    phone_number = "07321321321"
)
    test_animals = [
        Animal(
            id=uuid.UUID("fe96bf2a-7ef1-410a-887a-28a61f418304"),
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
            id=uuid.UUID("bfd86d41-07df-4b0d-85e0-bec04f61094b"),
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
            id=uuid.UUID("082ad5ad-ae09-4046-9b63-8d81b6fb6f0d"),
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
        ),
        Animal(
            id=uuid.UUID("04595568-1801-40d4-be13-bdbfe8ded0d8"),
            name="Test Four",
            species="Rabbit",
            age=3,
            breed="wereRabbit",
            location="London",
            male=True,
            bio="This is a test wereRabbit.",
            neutered=False,
            lives_with_children=False,
            images=1,
            isActive=True,
            shelter=test_shelter_2
        ),
        Animal(
            id=uuid.UUID("f8f12b04-b612-48cc-b87d-058dee19b36e"),
            name="Test Five",
            species="Other",
            age=2,
            breed="Monkey",
            location="London",
            male=True,
            bio="This is a test Monkey.",
            neutered=False,
            lives_with_children=False,
            images=1,
            isActive=True,
            shelter=test_shelter_2
        ),
    ]
    # with app.app_context():
    db_connection.seed_db(test_animals)
    
    repo = AnimalRepository(db)
    return repo, test_animals

@pytest.fixture
def user_repo(app_ctx, db_connection: DatabaseConnection):
    test_public_user = User(id=30, email="user@example.com", 
                    password="$2b$12$ktcmG68CCpPTv6QgRiqGOOhvjuSmEXjJyJmurK3RhvKTYihVJXM8W",
                    first_name="public", last_name="user", verified=True)
    test_shelter = Shelter(name="Example Shelter", location="South London", 
                          email="info@example.com", domain="example.com", phone_number="07123123123")
    test_shelter_user = User(id=10, email="shelter_user@example.com",
                            password="$2b$12$ktcmG68CCpPTv6QgRiqGOOhvjuSmEXjJyJmurK3RhvKTYihVJXM8W", 
                            first_name="test", last_name="user",verified=True, shelter=test_shelter)
    test_unverified_user = User(id=20, email="unverified.user@example.com",
                            password="$2b$12$ktcmG68CCpPTv6QgRiqGOOhvjuSmEXjJyJmurK3RhvKTYihVJXM8W", 
                            first_name="test", last_name="user", shelter=test_shelter,verified=False)
    db_connection.seed_db([test_public_user, test_shelter_user])
    repo = UserRepository(db)
    return repo

@pytest.fixture
def verification_repo(app_ctx, db_connection: DatabaseConnection):
    test_unverified_user = User(id=19,email="public_user@public-example.com", 
                    password="$2b$12$UQntHyyyDPNavpk984PDyu6JjfuE.CqJ8AEkxK4WUx5BbBOrXYtS6",
                    first_name="public", last_name="user", verified=False)
    test_unverified_user_1 = User(id=20, email="unverified.user@example.com",
                            password="$2b$12$UQntHyyyDPNavpk984PDyu6JjfuE.CqJ8AEkxK4WUx5BbBOrXYtS6", 
                            first_name="test", last_name="user", verified=False)
    test_verified_user = User(id=25, email="verified.user@example.com",
                            password="$2b$12$UQntHyyyDPNavpk984PDyu6JjfuE.CqJ8AEkxK4WUx5BbBOrXYtS6", 
                            first_name="test", last_name="user", verified=True)
    
    test_verification_item = Verification(id=uuid.UUID('5235c2d2-266a-4851-a48a-777ce595065e'),user_id=20, pin_hash=flask_bcrypt.generate_password_hash('123456').decode('utf-8'))
    
    test_verification_item_2 = Verification(id=uuid.UUID('5a991853-3ff2-48b3-b4f2-d5399324bfd4'),user_id=19, pin_hash=flask_bcrypt.generate_password_hash('123456').decode('utf-8'), used_at=int(time.time()))
    
    db_connection.seed_db([test_unverified_user_1, test_unverified_user, test_verification_item, test_verification_item_2, test_verified_user ])
    repo = VerificationRepository(db)
    return repo

@pytest.fixture
def message_repo(app_ctx, db_connection: DatabaseConnection):
    test_shelter = Shelter(id=1, name="Example Shelter", location="South London", 
                          email="info@example.com", domain="example.com", phone_number="07123123123")
    test_shelter_2 = Shelter(id=2, name="Example Shelter 2", location="North London",
                            email="info@example2.com", domain="example2.com", phone_number="07321321321")
    
    test_user = User(id=2, email="user@example333.com", 
                    password="$2b$12$ktcmG68CCpPTv6QgRiqGOOhvjuSmEXjJyJmurK3RhvKTYihVJXM8W",
                    first_name="public", last_name="user")
    
    test_user_2 = User(id=3, email="user@example333.com", 
                    password="$2b$12$ktcmG68CCpPTv6QgRiqGOOhvjuSmEXjJyJmurK3RhvKTYihVJXM8W",
                    first_name="public", last_name="user")
    
    test_shelter_user = User(id=1, email="shelter_user@example.com",
                            password="$2b$12$ktcmG68CCpPTv6QgRiqGOOhvjuSmEXjJyJmurK3RhvKTYihVJXM8W", 
                            first_name="test", last_name="user", shelter=test_shelter)
    
    test_shelter_2_user = User(id=4,email="shelter_2_user@example2.com",
                            password="$2b$12$ktcmG68CCpPTv6QgRiqGOOhvjuSmEXjJyJmurK3RhvKTYihVJXM8W", 
                            first_name="test", last_name="user", shelter=test_shelter_2)
    
    test_animal_1 = Animal(id=uuid.UUID("6ebc0357-849a-47ac-84c1-45cb40fa15a1"),name="Test One", species="cat", age=1, breed="Maine Coon",
                          location="London", male=True, bio="This is a test cat.",
                          neutered=False, lives_with_children=False, images=1, 
                          isActive=True, shelter=test_shelter)
    
    test_animal_2 = Animal(id=uuid.UUID("93497185-f4be-491d-a478-b26e16ebeb4f"),name="Test Two", species="dog", age=2, breed="test breed",
                          location="London", male=True, bio="This is a test dog.",
                          neutered=False, lives_with_children=False, images=1,
                          isActive=True, shelter=test_shelter)
    
    test_animal_3 = Animal(id=uuid.UUID("c01e1135-d5c3-4711-9c91-29f8903f742c"),name="Test Three", species="wolf", age=3, breed="werewolf",location="London", male=True, bio="This is a test werewolf.",neutered=False, lives_with_children=False, images=1,isActive=False, shelter=test_shelter_2)
    
    test_conversation = Conversation(id=uuid.UUID('05800ada-a00b-4d32-9aea-6eae201acc58'),shelter=test_shelter,animal=test_animal_1)
    
    test_conversation_1 = Conversation(
        id=uuid.UUID('0b598972-693f-4825-b34d-83d73afd89ce'),shelter=test_shelter,animal=test_animal_2, participants=[test_user])
    test_conversation_2 = Conversation(shelter=test_shelter_2,animal=test_animal_3)
    test_conversation_3 = Conversation(shelter=test_shelter_2,animal=test_animal_3)
    
    test_data = [
        Message(
            content=f"This is a test message\
                from {test_user.id}\
                to {test_shelter.name}\
                for {test_animal_1.name}",
            sender=test_user,
            conversation=test_conversation
            ),
        Message(
            id=uuid.UUID('5235c2d2-266a-4851-a48a-777ce595065e'),
            content=f"This is a test message reply\
                from {test_shelter_user.id}\
                to {test_user.id}\
                for {test_animal_1.name}",
            sender=test_shelter_user,
            conversation=test_conversation
            ),
        Message(
            id=uuid.UUID('33ba2e0b-481e-4c4d-8ceb-3027379177c1'),
            content=f"This is a test message \
            from: {test_user.id} \
            to {test_shelter.id} \
            for {test_animal_2.name}",
            sender=test_user,
            conversation=test_conversation_1
            ),
        Message(
            content=f"This is a test message\
                to {test_shelter_2.id}\
                from {test_user.id}",
            sender=test_user,
            conversation=test_conversation_2
            ),
        Message(
            content=f"This is a test message\
                for {test_shelter_2.id}\
                from {test_user_2.id}",
            sender=test_user_2,
            conversation=test_conversation_3
            ),
        Message(
            content=f"This is a test response\
                for {test_user_2.id}\
                from {test_shelter_2_user.id}",
            sender=test_shelter_2_user,
            conversation=test_conversation_3
            ),
        
    ]
    
    # db_connection.seed_db(test_data, preserve_order=True)
    db_connection.seed_db(test_data, preserve_order=True)
    
    repo = MessageRepository(db)
    return repo
    
@pytest.fixture
def conversation_repo(app_ctx, db_connection: DatabaseConnection):
    test_shelter = Shelter(id=1, name="Example Shelter", location="South London", 
                          email="info@example.com", domain="example.com", phone_number="07123123123")
    test_animal_1 = Animal(id=uuid.UUID("6ebc0357-849a-47ac-84c1-45cb40fa15a1"),name="Test One", species="cat", age=1, breed="test breed",
                          location="London", male=True, bio="This is a test cat.",
                          neutered=False, lives_with_children=False, images=1, 
                          isActive=True, shelter=test_shelter)
    test_user = User(id=2, email="user@example333.com", 
                    password="$2b$12$ktcmG68CCpPTv6QgRiqGOOhvjuSmEXjJyJmurK3RhvKTYihVJXM8W",
                    first_name="public", last_name="user")
    conversation = Conversation(
            id=uuid.UUID("ce8ea8a3-3680-41c5-83d1-7bf59cdc5a28"),
            shelter=test_shelter,
            animal=test_animal_1,
            participants=[test_user]
        )
    message = Message(
            content=f"This is a test message from public user 2 to shelter id 1 for test_animal_1",
            sender=test_user,
            conversation=conversation,
            created_at=datetime.fromisoformat('2025-01-04T16:26:26.841685+01:00')
            )
    
    repo = ConversationRepository(db)
    
    db_connection.seed_db([message])
    return repo

@pytest.fixture
def shelter_repo(app_ctx, db_connection: DatabaseConnection):
    
    test_shelter = Shelter(id=1, name="Example Shelter", location="South London", 
                          email="info@example.com", domain="example.com", phone_number="07123123123")
    
    test_shelter_2 = Shelter(id=2, name="Example Shelter 2", location="South London", 
                          email="info@example_battersea.com", domain="example_battersea.com", phone_number="07321321321")
    test_shelter_3 = Shelter(id=3, name="Example Shelter 3", location="South London", 
                          email="info@example_dogsandcats.com", domain="dogsandcats.com", phone_number="07111222333")
    
    repo = ShelterRepository(db)
    db_connection.seed_db([test_shelter, test_shelter_2, test_shelter_3])
    return repo

# new UUIDs
# 
# id=uuid.UUID('fa895567-cf50-49e8-b4f0-cf6d0b2cf0bc')
# id=uuid.UUID('64661364-3f1d-4fd4-a7a5-39ea709bb4b1')
# id=uuid.UUID('f7ebba41-c036-4798-85d9-291e98dd624a')
# id=uuid.UUID('6d8c483e-0754-459d-8899-237350eec87d')
# id=uuid.UUID('9dda4c62-717e-459e-ae94-bcef882b9d4f')
# id=uuid.UUID('7f2e54d6-c083-486b-b14b-6525ab8dcfe1')
# id=uuid.UUID('e4ba974e-0d52-40cb-98d8-a4a1d3f04f87')
# id=uuid.UUID('673e9051-4e9f-4d7b-8ac5-8db34f53b771')
# id=uuid.UUID('e680a49c-1853-4cee-bfa7-fc358482b41f')
# id=uuid.UUID('a3d813b4-ca2a-40ff-b9f6-bc03ef1db82d')
# id=uuid.UUID('117e5b7c-e525-46ca-a00f-a4e85b5cdd7c')
# id=uuid.UUID('7b37c203-cb86-418b-81e9-e1fdede6cbfc')
# id=uuid.UUID('28113132-74b7-4731-929a-098da1c37795')
# id=uuid.UUID('b5ca8a48-b256-4de0-99ad-dcfebae1b44e')
# id=uuid.UUID('44c9b475-20d6-4322-ae72-3bd14b8a1860')
# id=uuid.UUID('5f1990b8-d093-403c-84f4-dc8f27ae8b58')