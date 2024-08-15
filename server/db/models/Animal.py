# The functions for READING and POSTING are defined here

class Animal:
    def __init__(self, id, name, species, age, breed, location, gender, description, neutered, lives_with_children, shelter_id):
        self.id = id
        self.name = name
        self.species = species
        self.age = age
        self.breed = breed
        self.location = location
        self.gender = gender
        self.description = description
        self.neutered = neutered
        self.lives_with_children = lives_with_children
        self.shelter_id = shelter_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"Listing:({self.id}, {self.name}, {self.species}, {self.age}, {self.breed}, {self.location}, {self.gender}, {self.description}, {self.neutered}, {self.lives_with_children}, {self.shelter_id}"
    