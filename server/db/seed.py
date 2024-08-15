'''

'''

# Guidance from here - https://coderpad.io/blog/development/sqlalchemy-with-postgresql/

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker


# from database_connection import db_session


# TODO Refactor and place this in the database connection file.
url = URL.create(
    drivername="postgresql",
    host="localhost",
    database="adoption"
)

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
    bio = Column(String(500), nullable=False)
    neutered = Column(Boolean, nullable=False)
    lives_with_children = Column(Boolean, nullable=False)
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

Base.metadata.create_all(engine)


# Check which tables are being reflected
print("Tables reflected => ", Base.metadata.tables.keys())  # If using MetaData

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


# Populate the ANIMALS table
###############################

animal1 = Animal(
    name = "Bobby",
    species = "cat",
    age = 3,
    breed = "British Shorthair",
    location = "Cardiff",
    male = True,
    bio = "This is a lovely cat and he needs a good home.",
    neutered = True,
    lives_with_children = True,
    shelter = shelter1
)

session.add(animal1)


#################### 

animal2 = Animal(
    name = "Roger",
    species = "dog",
    age = 3,
    breed = "German Shepherd",
    location = "London",
    male = True,
    bio = "This is a lovely dog and he needs a good home.",
    neutered = False,
    lives_with_children = False,
    shelter = shelter2
)

session.add(animal2)

#################### 

animal3 = Animal(
    name = "Duke",
    species = "rabbit",
    age = 3,
    breed = "American Rabbit",
    location = "London",
    male = True,
    bio = "This is a lovely rabbit and he needs a good home and lots of carrots.",
    neutered = False,
    lives_with_children = False,
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




#############################################################

session.commit()