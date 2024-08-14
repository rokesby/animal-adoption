from mongoengine import *
from models.user import User
from models.animal import Animal
from models.shelter import Shelter
from db_file import *

connect_db()


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