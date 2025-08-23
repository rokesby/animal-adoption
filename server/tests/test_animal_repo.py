import uuid
import pytest
from lib.database_connection import db
from sqlalchemy import select
from lib.models import Animal



def test_get_all_animals(app_ctx, animal_repository):
    """get_all should return all animals"""
    repo, test_animals = animal_repository
    animals = repo.get_all()
    print(animals)
    assert len(animals) == len(test_animals)

def test_get_all_active(app_ctx, app, animal_repository):
    """
    get_all_active should return all animals where 'isActive' is True
    """
    repo, test_animals = animal_repository
    active_animals = repo.get_all_active()
    assert len(active_animals) == 4
        

def test_get_by_id(app_ctx, app, animal_repository):
    """
    get_by_id should return the animal with a matching id
    """
    repo, test_animals = animal_repository
    test_animal_1 = test_animals[0].id
    animal = repo.get_by_id(test_animal_1)
    print(animal)
    assert animal.id == test_animal_1

def test_create_new_animal(app_ctx, app, animal_repository):
    """
    create_new_animal should create a new animal
    """
    repo, test_animals = animal_repository

    animal_data = {
        'name':"new animal",
        "species" : "rabbit",
        "age" : 5,
        "breed" : "robot",
        "location" : "Cardiff",
        "male" : True,
        "bio" : "This is a lovely cyborg",
        "neutered" : True,
        "lives_with_children" : True,
        "images" : 0,
        "isActive" : True,
        "shelter_id": 1
    }
    # with app.app_context():
    repo.create_new_animal(animal_data)
    animal = db.session.scalar(select(Animal).filter_by(name="new animal"))
    animals = repo.get_all()

    assert animals[-1].name == "new animal"
    assert animal.name == "new animal"
    assert len(animals) == len(test_animals)+1

def test_update_animal(app_ctx, app, animal_repository):
    """
    update_animal should update animal fields
    """
    repo, test_animals = animal_repository
    animal_three = test_animals[2]
    animal_data = {
    "id":animal_three.id,
    "name":"Test Three updated",
    "species" : "werewolf",
    "age" : 4,
    "breed" : "Canadian Werewolf",
    "location" : "Canada",
    "male" : False,
    "bio" : "This is a lovely werewolf",
    "neutered" : True,
    "lives_with_children" : True,
    "images" : 1,
    "isActive" : True,
    "shelter_id": 1
}
    with app.app_context():
        repo.update_animal(animal_data)
        
        animal = db.session.scalar(select(Animal).filter_by(id = animal_three.id))
        assert animal.name == "Test Three updated"
        assert animal.species == "werewolf"
        assert animal.age == 4
        assert animal.breed == "Canadian Werewolf"
        assert animal.location == "Canada"
        assert animal.male == False
        assert animal.bio == "This is a lovely werewolf"
        assert animal.neutered == True
        assert animal.lives_with_children == True
        assert animal.images == 1
        assert animal.isActive == True
        assert animal.shelter_id == 1

def test_get_shelters_animals(app_ctx, db_connection, animal_repository):
    """
    get_users_animals should return all animals 
    belonging to the given shelter_id
    """
    repo, test_animals = animal_repository
    shelter_id = 1
    shelters_animals = repo.get_shelters_animals(shelter_id)

    assert len(shelters_animals) == 3
    
def test_get_shelters_active_animals(app_ctx, db_connection, animal_repository):
    """
    get_users_active_animals should return all animals 
    that belong to the same shelter as the user
    and have an 'is_active' value of True
    """
    repo, test_animals = animal_repository
    shelter_id = 1
    shelters_animals = repo.get_shelters_active_animals(shelter_id)
    
    assert len(shelters_animals) == 2
    
    for animal in shelters_animals:
        assert animal.isActive is True
        assert animal.shelter_id == shelter_id
        
    animal_names = [animal.name for animal in shelters_animals]
    assert "Test One" in animal_names
    assert "Test Two" in animal_names
    
def test_get_shelters_inactive_animals(app_ctx, db_connection, animal_repository):
    """
    get_users_inactive_animals should return all animals 
    that belong to the same shelter as the user
    and have an 'is_active' value of False
    """
    repo, test_animals = animal_repository
    shelter_id = 1
    users_animals = repo.get_shelters_inactive_animals(shelter_id)
    
    assert len(users_animals) == 1
    
    for animal in users_animals:
        assert animal.isActive is False
        assert animal.shelter_id == shelter_id
        
    animal_names = [animal.name for animal in users_animals]
    assert "Test Three" in animal_names
    
    animal_names = [animal.name for animal in users_animals]
    assert "Test One" not in animal_names
    assert "Test Two" not in animal_names