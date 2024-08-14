from mongoengine import *
from models.user import User
from models.animal import Animal
from models.shelter import Shelter
from db_file import *

connect_db()

# class Animal(Document):
#     name = StringField(required=True, max_length=100)
#     species = StringField(required=True)
#     age = StringField(required=True)
#     breed = StringField(required=True)
#     location = StringField(required=True)
#     male = BooleanField(required=True)
#     bio = StringField(required=True, max_length=500)
#     neutered = BooleanField(required=True)
#     owner = ReferenceField(Shelter, reverse_delete_rule='CASCADE')
#     lives_with_children = BooleanField(required=True)

#     meta = {
#         'collection': 'animals'
#     }


# class Shelter(Document):
#     name_of_shelter = StringField(required=True)
#     location = StringField(required=True)
#     email = StringField(required=True)
#     phone_number = IntField(required=True, max_length=11)
#     animals = ListField(ReferenceField(Animal))
#     staff = ListField(ReferenceField(User))

#     meta = {
#         'collection': 'shelters'
#     }
# class User(Document):
#     email = StringField(required=True)
#     password = StringField(required=True)
#     first_name = StringField(max_length=50)
#     last_name = StringField(max_length=50)
#     shelter = ReferenceField(Shelter)

#     meta = {
#     'collection': 'users',
#     'indexes': [
#         'email'
#     ]
#     }

User.drop_collection()
Animal.drop_collection()
Shelter.drop_collection()

# Creating Seeds for Shelters

shelter1 = Shelter(name_of_shelter='RSPCA', location='London', email='1234@rspca.co.uk', phone_number=12345678910, animals = [], staff=[])
shelter2= Shelter(name_of_shelter='Battersea Dogs Home', location='London', email='1234@rspca.co.uk', phone_number= 12345678910, animals = [], staff=[])

# Creating seeds for users

user1= User(email='1234@battersea.co.uk', password='1234', first_name='Marya', last_name= 'Shariq', shelter=shelter2)

# Creating seed for animals

animal1 = Animal(name='Charlie', species='dog', age='2', breed='Dalmation', location='London', male=True, bio='I am a cute dog', neutered=True, lives_with_children=True )

print('Database seeded successfully!')
print("Users and their Animals:")
for user in User.objects:
    print(f"User: {user.name}, Email: {user.email}")
    for animal in User.animals:
        print(f" - {animal.name} ({animal.species}, {animal.age} years old)")

disconnect_db()