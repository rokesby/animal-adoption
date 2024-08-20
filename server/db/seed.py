# Guidance from here - https://coderpad.io/blog/development/sqlalchemy-with-postgresql/

from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, MetaData

from sqlalchemy.orm import declarative_base

from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker


import os
from dotenv import load_dotenv

load_dotenv()
print("RESEEDING DB - ", "DB Name => ", os.getenv('DATABASE_NAME'), "DB Host => ", os.getenv('DATABASE_HOST'))

url = URL.create(
    drivername="postgresql",
    host = os.getenv("DATABASE_HOST"),
    database= os.getenv("DATABASE_NAME")
)

#engine = create_engine("postgresql+psycopg2://reza@" + os.getenv('DATABASE_HOST') + "/" + os.getenv('DATABASE_NAME'))

engine = create_engine(url)
connection = engine.connect()

meta = MetaData()
meta.reflect(bind=engine)

Base = declarative_base()

# Drop all tables and clear the database.
meta.drop_all(bind=engine, tables=None, checkfirst=True)

# Create the models.

#############################################################


class Animal(Base):
    __tablename__ = 'animals'

    id = Column(Integer(), primary_key=True)
    name = Column(String(255))
    species = Column(String(50))
    age = Column(Integer)
    breed = Column(String(50), nullable=False)
    location = Column(String(50), nullable=False)
    male = Column(Boolean, nullable=False)
    bio = Column(String(2048), nullable=False)
    neutered = Column(Boolean, nullable=False)
    lives_with_children = Column(Boolean, nullable=False)
    image = Column(String(255))
    shelter_id = Column(Integer(), ForeignKey('shelters.id'))


#############################################################

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)

    email = Column(String(255), nullable=False)
    password = Column(String(60), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    shelter_id = Column(Integer(), ForeignKey('shelters.id'))

#############################################################


class Shelter(Base):
    __tablename__ = 'shelters'

    id = Column(Integer(), primary_key=True)

    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone_number = Column(String(20))

    animals = relationship('Animal', backref='shelter')
    users = relationship('User', backref='shelter')

# Animal.shelter = relationship("Shelter", back_populates="animals")
# User.shelter = relationship("Shelter", back_populates="users")

#############################################################

Base.metadata.create_all(engine)

# Check which tables are being reflected
print("Tables created => ", Base.metadata.tables.keys())  # If using MetaData

Session = sessionmaker(bind=engine)
session = Session()

# Populate the SHELTER table
###############################

shelter1 = Shelter(
    name = "Battersea Dogs Home",
    location = "South London",
    email = "info@batterseadogshome.org",
    phone_number = "07931996801"
)
session.add(shelter1)

shelter2 = Shelter(
    name = "Cardiff Dogs Home",
    location = "Cardiff",
    email = "info@cardiffdogshome.org",
    phone_number = "07931996802"
)
session.add(shelter2)

shelter3 = Shelter(
    name = "Mayhew Animal Home",
    location = "NW London",
    email = "info@themayhew.org.org",
    phone_number = "07931996802"
)
session.add(shelter3)

# Populate the ANIMALS table
###############################

animal1 = Animal(
    name = "Andie",
    species = "cat",
    age = 3,
    breed = "British Shorthair",
    location = "Cardiff",
    male = True,
    bio = "This is a lovely cat and he needs a good home.",
    neutered = True,
    lives_with_children = True,
    image = "seed_andie.png",
    shelter = shelter1
)

session.add(animal1)

#################### 

animal2 = Animal(
    name = "Cinnamon",
    species = "cat",
    age = 3,
    breed = "Maine Coon",
    location = "London",
    male = True,
    bio = "This is a lovely kitten and he needs a good home.",
    neutered = False,
    lives_with_children = False,
    image = "seed_cinnamon.png",
    shelter = shelter2
)

session.add(animal2)

#################### 

animal3 = Animal(
    name = "River",
    species = "dog",
    age = 3,
    breed = "Husky",
    location = "London",
    male = True,
    bio = "This is a lovely dog and he needs a good home and lots of carrots.",
    neutered = False,
    lives_with_children = False,
    image = "seed_river.png",
    shelter = shelter2
)

session.add(animal3)


# Populate the USERS table
###############################

user1 = User(
    email = "reza@jugon.com",
    password = "password1",
    first_name = "reza",
    last_name = "jugon",
    shelter = shelter1
)
session.add(user1)

user2 = User(
    email = "marya@shariq.com",
    password = "password1",
    first_name = "Marya",
    last_name = "Shariq",
    shelter = shelter2
)
session.add(user2)


user3 = User(
    email = "matt@wilkes.com",
    password = "password1",
    first_name = "Matt",
    last_name = "Wilkes",
    shelter = shelter2
)
session.add(user3)

#######

animal4 = Animal(
    name = "Kylie",
    species = "dog",
    age = 2,
    breed = "German Shepherd Cross",
    location = "London",
    male = False,
    bio = "Lovely Kylie is an intelligent and caring girl who is ready to go to her new home. She is sensitive and can be shy when meeting new people, but once she gains her confidence loves affection. She enjoys walks, treats and playing with her toys, especially tennis balls. She has learnt a number of commands including sit, paw, down, roll over and leave and is doing well with her training. She is friendly and social with other dogs, but will need some guidance and ongoing socialisation as she is a young dog. She would be best suited to a quiet or semi rural location as can be sensitive to new places and traffic, however is gaining confidence in this area. With the right person making her feel safe and being patient with her she would make an amazing and loyal companion.",
    neutered = False,
    lives_with_children = False,
    image = "",
    shelter = shelter3
)

session.add(animal4)

#############################################################

session.commit()