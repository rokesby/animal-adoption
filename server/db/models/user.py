from mongoengine import *
from models.shelter import Shelter

class User(Document):
    email = StringField(required=True)
    password = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    shelter = ReferenceField(Shelter)

    meta = {
    'collection': 'users',
    'indexes': [
        'email'
    ]
}