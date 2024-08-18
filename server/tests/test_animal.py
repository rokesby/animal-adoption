# class Animal:
#     def __init__(self, id, name, species, age, breed, location, gender, description, neutered, lives_with_children, shelter_id):
#         self.id = id
#         self.name = name
#         self.species = species
#         self.age = age
#         self.breed = breed
#         self.location = location
#         self.gender = gender
#         self.description = description
#         self.neutered = neutered
#         self.lives_with_children = lives_with_children
#         self.shelter_id = shelter_id
from server.db.models.Animal import Animal
"""
Book constructs with an id, title and author_name
"""
def test_animal():
    animal = Animal(1, "Test Title", "Test Author")
    assert animal.id == 1
    assert animal.name == "Test Animal"
    assert animal.species == "Test Dog"
    assert animal.age == 4
    assert animal.breed == "Test Breed"
    assert animal.location == "Test Location"
    assert animal.gender == "Male"
    assert animal.description == "Test Description"
    assert animal.neutered == True
    assert animal.lives_with_children == False
    assert animal.shelter_id == 1