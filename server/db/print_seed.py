from seed import Animal, Shelter, User
from database_connection import db_session

with db_session() as db:
    # Now print a short listing 
    print("Animal list............")
    animals = db.query(Animal).all()
    for animal in animals:
        print(animal.name) # or any other attribute

    print("Shelter list............")
    shelters = db.query(Shelter).all()
    for shelter in shelters:
        print(shelter.name) # or any other attribute

    print("User list............")
    users = db.query(User).all()
    for user in users:
        print(user.email) # or any other attribute