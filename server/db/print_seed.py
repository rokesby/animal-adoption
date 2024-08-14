from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from seed import Animal, Shelter, User

# TODO : Place this into the database connection object.

url = URL.create(
    drivername="postgresql",
    host="localhost",
    database="adoption"
)


engine = create_engine(url)

Session = sessionmaker(bind=engine)
session = Session()


# Now print a short listing 
print("Animal list............")
animals = session.query(Animal).all()
for animal in animals:
    print(animal.name) # or any other attribute


print("Shelter list............")
shelters = session.query(Shelter).all()
for shelter in shelters:
    print(shelter.name) # or any other attribute


print("User list............")
users = session.query(User).all()
for user in users:
    print(user.email) # or any other attribute