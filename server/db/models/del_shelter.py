from mongoengine import *
# from models.animal import Animal
# from models.user import User

class Shelter(Document):
    name_of_shelter = StringField(required=True)
    location = StringField(required=True)
    email = StringField(required=True)
    phone_number = IntField(required=True, max_length=11)
    animals = ListField(ReferenceField('Animal'))
    staff = ListField(ReferenceField('User'))

    meta = {
        'collection': 'shelters'
    }
    
