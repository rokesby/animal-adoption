'''
ONE OFF INSTRUCTIONS

- go to /server/db
- active your venv environment!
- pip install psycopg2
- pip install SQLAlchemy
- type in createdb adoption # to create a new postgres database
- run this file : python seed.py
- run this file : python print_seed.py

'''

# Guidance from here - https://coderpad.io/blog/development/sqlalchemy-with-postgresql/


from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# TODO Refactor and place this in the database connection file.
url = URL.create(
    drivername="postgresql",
    host="localhost",
    database="adoption"
)

engine = create_engine(url)

connection = engine.connect()


from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, MetaData
from sqlalchemy.orm import declarative_base
from datetime import datetime

meta = MetaData()
meta.reflect(bind=engine)

Base = declarative_base()
# Drop all tables.
# Base.metadata.reflect()
meta.drop_all(bind=engine, tables=None, checkfirst=True)

# class Article(Base):
#     __tablename__ = 'articles'

#     id = Column(Integer(), primary_key=True)
#     slug = Column(String(100), nullable=False, unique=True)
#     title = Column(String(100), nullable=False)
#     created_on = Column(DateTime(), default=datetime.now)
#     updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
#     content = Column(Text)
#     author_id = Column(Integer(), ForeignKey('authors.id'))


from sqlalchemy.orm import relationship, backref

# class Author(Base):
#     __tablename__ = 'authors'

#     id = Column(Integer(), primary_key=True)
#     firstname = Column(String(100))
#     lastname = Column(String(100))
#     email = Column(String(255), nullable=False)
#     joined = Column(DateTime(), default=datetime.now)

#     articles = relationship('Article', backref='author')

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
    # TODO - animals - need to add relationships in here later on
    # TODO - animals = ListField(ReferenceField('Animal'))
    # TODO - staff = ListField(ReferenceField('User'))


#############################################################


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)

    email = Column(String(255), nullable=False)
    password = Column(String(60), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    shelter_id = Column(Integer(), ForeignKey('shelters.id'))
    
    # TODO - staff = ListField(ReferenceField('User'))
    # Link the staff member to a shelter    

#############################################################

Base.metadata.create_all(engine)

# Check which tables are being reflected
print("=> ", Base.metadata.tables.keys())  # If using MetaData

# TODO - Create relationships between the entities.
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# ezz = Author(
#     firstname="Ezzeddin",
#     lastname="Abdullah",
#     email="ezz_email@gmail.com"
# )

# ahmed = Author(
#     firstname="Ahmed",
#     lastname="Mohammed",
#     email="ahmed_email@gmail.com"
# )

# article1 = Article(
#     slug="clean-python",
#     title="How to Write Clean Python",
#     content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
#     author=ezz
#     )
# session.add(article1)

#############################################################


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




# Populate the USERS table

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

# article2 = Article(
#     slug="postgresql-system-catalogs-metadata",
#     title="How to Get Metadata from PostgreSQL System Catalogs",
#     content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
#     created_on = datetime(2022, 8, 29),
#     author=ezz
#     )

# article3 = Article(
#     slug="sqlalchemy-postgres",
#     title="Interacting with Databases using SQLAlchemy with PostgreSQL",
#     content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
#     author=ahmed
#     )

# session.add(article2)
# session.add(article3)
# session.flush()



