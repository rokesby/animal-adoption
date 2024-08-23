# Guidance from here - https://coderpad.io/blog/development/sqlalchemy-with-postgresql/

from sqlalchemy import create_engine
from sqlalchemy import URL

from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, MetaData
from sqlalchemy.orm import declarative_base


import os
from dotenv import load_dotenv

load_dotenv()
print("RESEEDING DB - ", "DB Name => ", os.getenv('DATABASE_NAME'), "DB Host => ", os.getenv('DATABASE_HOST'))

url = URL.create(
    drivername="postgresql",
    host = os.getenv("DATABASE_HOST"),
    database= os.getenv("DATABASE_NAME")
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
    bio = Column(String(2048), nullable=False)
    neutered = Column(Boolean, nullable=False)
    lives_with_children = Column(Boolean, nullable=False)
    image = Column(String(255))
    isActive = Column(Boolean, nullable=False, default=True)
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
    email = "info@themayhew.org",
    phone_number = "07931996802"
)
session.add(shelter3)

# Populate the ANIMALS table
###############################

animal1 = Animal(
    name = "Andie",
    species = "Cat",
    age = 3,
    breed = "British Shorthair",
    location = "Cardiff",
    male = True,
    bio = "This is a lovely cat and he needs a good home.",
    neutered = True,
    lives_with_children = True,
    image = "seed_andie.png",
    isActive = True,
    shelter = shelter1
)

session.add(animal1)

#################### 

animal2 = Animal(
    name = "Cinnamon",
    species = "Cat",
    age = 3,
    breed = "Maine Coon",
    location = "London",
    male = True,
    bio = "This is a lovely kitten and he needs a good home.",
    neutered = False,
    lives_with_children = False,
    image = "seed_cinnamon.png",
    isActive = True,
    shelter = shelter2
)

session.add(animal2)

#################### 

animal3 = Animal(
    name = "River",
    species = "Dog",
    age = 3,
    breed = "Husky",
    location = "London",
    male = True,
    bio = "This is a lovely dog and he needs a good home and lots of carrots.",
    neutered = False,
    lives_with_children = False,
    image = "seed_river.png",
    isActive = True,
    shelter = shelter2
)

session.add(animal3)

#################### 

animal4 = Animal(
    name = "Kylie",
    species = "Dog",
    age = 2,
    breed = "German Shepherd Cross",
    location = "London",
    male = False,
    bio = "Lovely Kylie is an intelligent and caring girl who is ready to go to her new home. She is sensitive and can be shy when meeting new people, but once she gains her confidence loves affection. She enjoys walks, treats and playing with her toys, especially tennis balls. She has learnt a number of commands including sit, paw, down, roll over and leave and is doing well with her training. She is friendly and social with other dogs, but will need some guidance and ongoing socialisation as she is a young dog. She would be best suited to a quiet or semi rural location as can be sensitive to new places and traffic, however is gaining confidence in this area. With the right person making her feel safe and being patient with her she would make an amazing and loyal companion.",
    neutered = False,
    lives_with_children = False,
    image = "seed_kylie.png",
    isActive = True,
    shelter = shelter3
)

session.add(animal4)

#################### 

animal5 = Animal(
    name = "Biscuit",
    species = "Rabbit",
    age = 1,
    breed = "Crossbreed",
    location = "London",
    male = True,
    bio = "He is a friendly and inquisitive boy who is happy spending time with people. He loves to be stroked and often approaches humans for a fuss, but like most rabbits he prefers not to be picked up. He will be able to live with any age children in his new home as long as they can be calm and quiet around him and understand he would like to keep all four paws on the ground! Biscuit has been neutered so will be looking for an indoor or outdoor home with a neutered female bunny to keep him company. He would thrive in a home where he has a companion to play and snuggle with. Rabbits are social animals, and having a partner can provide them with companionship and mental stimulation. Biscuit’s friendly and calm nature makes him an excellent candidate for bonding with another rabbit.",
    neutered = False,
    lives_with_children = False,
    image = "seed_biscuit.jpeg",
    isActive = True,
    shelter = shelter3
)

session.add(animal5)

#################### 

animal6 = Animal(
    name = "Mango",
    species = "Cat",
    age = 1,
    breed = "Domestic Short Hair",
    location = "Southampton",
    male = False,
    bio = "Meet golden girl Mango searching for her forever new home. This little lady is looking for an owner who is wanting a cat that is fun, inquisitive, playful and full of character! \n Mango is a sensitive cat who is social with her human friends once she has built a bond. When she has a relationship with you, she enjoys gentle strokes and lap time, but this is all on her terms. She does not like to be over handled so it will be important her new owners read her body language and don’t overstep boundaries. When she's really happy she greets you with the cutest chirp! Mango is looking for a home where she will have access to come and go as she pleases in a quiet area. She would ideally be best placed in a rural or semi-rural location or a home with interesting surroundings. \n She is unable to live with other pets and is looking for an adult only home.There is so much more to tell you about this lovely girl so please contact the centre today for more information.",
    neutered = False,
    lives_with_children = False,
    image = "seed_mango.jpeg",
    isActive = True,
    shelter = shelter2
)

session.add(animal6)

#################### 

animal7 = Animal(
    name = "Binx",
    species = "Cat",
    age = 1,
    breed = "Domestic Short Hair, Tabby White",
    location = "Birmingham",
    male = True,
    bio = "Meet the beautiful Binx! Binx is looking for a quiet home where he can find his paws and settle into his new environment. Once he gets to know you he is a sweet and affectionate boy. He enjoys getting up on your lap and loves a fuss. He is looking for a home with no other pets. Binx can live with older school aged children who can allow him his own space when he needs it. Binx will need access to a garden when once he has settled in",
    neutered = False,
    lives_with_children = False,
    image = "seed_binx.jpeg",
    isActive = True,
    shelter = shelter2
)

session.add(animal7)

#################### 

animal8 = Animal(
    name = "Zara",
    species = "Dog",
    age = 3,
    breed = "Doberman Brown",
    location = "Birmingham",
    male = False,
    bio = "Meet Zara, the delightful Doberman whose bouncy spirit and loving personality are sure to win your heart! This energetic girl is searching for a quiet home where she can thrive, complete with a consistent routine to help her settle in comfortably. Zara is strong on the lead, so she’ll need a family that can manage her enthusiasm while also appreciating her zest for life. This playful lady adores her ball and is always up for a game of fetch, making her the perfect companion for outdoor adventures. Zara would be best suited in a home with older children due to her size and needing a calm home routine to help her feel comfortable. Zara is eager to find a loving family who will cherish her as she embarks on a new chapter in her life. If you're ready to embark on adventures and create a routine filled with love and fun, Zara could be the perfect addition to your family!",
    neutered = False,
    lives_with_children = False,
    image = "seed_zara.jpg",
    isActive = True,
    shelter = shelter1
)

session.add(animal8)

#################### 


animal9 = Animal(
    name = "Bella",
    species = "Dog",
    age = 5,
    breed = "Dachshund (Smooth-Haired)",
    location = "Sheffield",
    male = False,
    bio = "Bella is a gentle and sweet Dachshund with a heart full of love to give. She might take a little time to warm up, but once she does, she becomes a loyal and affectionate companion. Bella will need a patient family who can help her build her confidence. Once she is comfortable, Bella’s current family have described her as a 'brilliant dog'. Bella’s first home was a quiet household where she didn't get much exposure to the outside world. As a result, she can be anxious in new environments and around new people. Bella would be best suited to a calm and quiet home; she thrives on having a consistent environment with routine and regular walking routes. Dachshunds can suffer from breed related health problems. Dogs with long backs and short legs may also be pre-disposed to certain skeletal conditions. We always recommend anyone thinking about adopting or buying a dachshund to thoroughly research the breed beforehand. Our expert team will be able to give you advice on any support Bella may need.",
    neutered = False,
    lives_with_children = False,
    image = "seed_bella.jpeg",
    isActive = True,
    shelter = shelter2
)

session.add(animal9)

#################### 

# Populate the USERS table
###############################

user1 = User(
    email = "reza@jugon.com",
    password = "$2b$12$j1Jfgt6YnqBRF.4Npxlp9eVBPBgh/2HCdHHfMCcmsfmVIh98mM86O",
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
