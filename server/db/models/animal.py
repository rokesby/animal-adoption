from mongoengine import *
from models.shelter import Shelter

class Animal(Document):
    name = StringField(required=True, max_length=100)
    species = StringField(required=True)
    age = StringField(required=True)
    breed = StringField(required=True)
    location = StringField(required=True)
    male = BooleanField(required=True)
    bio = StringField(required=True, max_length=500)
    neutered = BooleanField(required=True)
    owner = ReferenceField(Shelter, reverse_delete_rule='CASCADE')
    lives_with_children = BooleanField(required=True)

    meta = {
        'collection': 'animals'
    }





