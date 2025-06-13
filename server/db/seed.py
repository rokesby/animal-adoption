from lib.models import Base, Animal, User, Shelter


# Populate the SHELTER table
###############################

shelter1 = Shelter(
    name = "Battersea Dogs Home",
    location = "South London",
    email = "info@batterseadogshome.org",
    phone_number = "07931996801"
)


shelter2 = Shelter(
    name = "Cardiff Dogs Home",
    location = "Cardiff",
    email = "info@cardiffdogshome.org",
    phone_number = "07931996802"
)


shelter3 = Shelter(
    name = "Mayhew Animal Home",
    location = "NW London",
    email = "info@themayhew.org",
    phone_number = "07931996802"
)

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
    images = 1,
    profileImageId = 'profile.png',
    isActive = True,
    shelter = shelter1
)


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
    images = 1,
    profileImageId = 'profile.png',
    isActive = True,
    shelter = shelter3
)


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
    images = 1,
    profileImageId = 'profile.png',
    isActive = True,
    shelter = shelter2
)


#################### 

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
    images = 1,
    profileImageId = 'profile.png',
    isActive = True,
    shelter = shelter3
)


#################### 

animal5 = Animal(
    name = "Biscuit",
    species = "rabbit",
    age = 1,
    breed = "Crossbreed",
    location = "London",
    male = True,
    bio = "He is a friendly and inquisitive boy who is happy spending time with people. He loves to be stroked and often approaches humans for a fuss, but like most rabbits he prefers not to be picked up. He will be able to live with any age children in his new home as long as they can be calm and quiet around him and understand he would like to keep all four paws on the ground! Biscuit has been neutered so will be looking for an indoor or outdoor home with a neutered female bunny to keep him company. He would thrive in a home where he has a companion to play and snuggle with. Rabbits are social animals, and having a partner can provide them with companionship and mental stimulation. Biscuit’s friendly and calm nature makes him an excellent candidate for bonding with another rabbit.",
    neutered = False,
    lives_with_children = False,
    images = 1,
    profileImageId = 'profile.jpeg',
    isActive = True,
    shelter = shelter3
)


#################### 

animal6 = Animal(
    name = "Mango",
    species = "cat",
    age = 1,
    breed = "Domestic Short Hair",
    location = "Southampton",
    male = False,
    bio = "Meet golden girl Mango searching for her forever new home. This little lady is looking for an owner who is wanting a cat that is fun, inquisitive, playful and full of character! \n Mango is a sensitive cat who is social with her human friends once she has built a bond. When she has a relationship with you, she enjoys gentle strokes and lap time, but this is all on her terms. She does not like to be over handled so it will be important her new owners read her body language and don’t overstep boundaries. When she's really happy she greets you with the cutest chirp! Mango is looking for a home where she will have access to come and go as she pleases in a quiet area. She would ideally be best placed in a rural or semi-rural location or a home with interesting surroundings. \n She is unable to live with other pets and is looking for an adult only home.There is so much more to tell you about this lovely girl so please contact the centre today for more information.",
    neutered = False,
    lives_with_children = False,
    images = 1,
    profileImageId = 'profile.jpeg',
    isActive = True,
    shelter = shelter2
)


#################### 

animal7 = Animal(
    name = "Binx",
    species = "cat",
    age = 1,
    breed = "Domestic Short Hair, Tabby White",
    location = "Birmingham",
    male = True,
    bio = "Meet the beautiful Binx! Binx is looking for a quiet home where he can find his paws and settle into his new environment. Once he gets to know you he is a sweet and affectionate boy. He enjoys getting up on your lap and loves a fuss. He is looking for a home with no other pets. Binx can live with older school aged children who can allow him his own space when he needs it. Binx will need access to a garden when once he has settled in",
    neutered = False,
    lives_with_children = False,
    images = 1,
    profileImageId = 'profile.jpeg',
    isActive = True,
    shelter = shelter2
)


#################### 

animal8 = Animal(
    name = "Zara",
    species = "dog",
    age = 3,
    breed = "Doberman Brown",
    location = "Birmingham",
    male = False,
    bio = "Meet Zara, the delightful Doberman whose bouncy spirit and loving personality are sure to win your heart! This energetic girl is searching for a quiet home where she can thrive, complete with a consistent routine to help her settle in comfortably. Zara is strong on the lead, so she’ll need a family that can manage her enthusiasm while also appreciating her zest for life. This playful lady adores her ball and is always up for a game of fetch, making her the perfect companion for outdoor adventures. Zara would be best suited in a home with older children due to her size and needing a calm home routine to help her feel comfortable. Zara is eager to find a loving family who will cherish her as she embarks on a new chapter in her life. If you're ready to embark on adventures and create a routine filled with love and fun, Zara could be the perfect addition to your family!",
    neutered = False,
    lives_with_children = False,
    images = 1,
    profileImageId = 'profile.jpg',
    isActive = True,
    shelter = shelter1
)


#################### 


animal9 = Animal(
    name = "Bella",
    species = "dog",
    age = 5,
    breed = "Dachshund (Smooth-Haired)",
    location = "Sheffield",
    male = False,
    bio = "Bella is a gentle and sweet Dachshund with a heart full of love to give. She might take a little time to warm up, but once she does, she becomes a loyal and affectionate companion. Bella will need a patient family who can help her build her confidence. Once she is comfortable, Bella’s current family have described her as a 'brilliant dog'. Bella’s first home was a quiet household where she didn't get much exposure to the outside world. As a result, she can be anxious in new environments and around new people. Bella would be best suited to a calm and quiet home; she thrives on having a consistent environment with routine and regular walking routes. Dachshunds can suffer from breed related health problems. Dogs with long backs and short legs may also be pre-disposed to certain skeletal conditions. We always recommend anyone thinking about adopting or buying a dachshund to thoroughly research the breed beforehand. Our expert team will be able to give you advice on any support Bella may need.",
    neutered = False,
    lives_with_children = False,
    images = 1,
    profileImageId = 'profile.jpeg',
    isActive = True,
    shelter = shelter2
)

#################### 


# Populate the USERS table
###############################

user1 = User(
    email = "reza@example.com",
    password = "$2b$12$j1Jfgt6YnqBRF.4Npxlp9eVBPBgh/2HCdHHfMCcmsfmVIh98mM86O",
    first_name = "reza",
    last_name = "example",
    shelter = shelter1
)

user2 = User(
    email = "marya@example.com",
    password = "$2b$12$ktcmG68CCpPTv6QgRiqGOOhvjuSmEXjJyJmurK3RhvKTYihVJXM8W",
    first_name = "Marya",
    last_name = "example",
    shelter = shelter2
)


user3 = User(
    email = "matt@example.com",
    password = "$2b$12$ktcmG68CCpPTv6QgRiqGOOhvjuSmEXjJyJmurK3RhvKTYihVJXM8W",
    first_name = "Matt",
    last_name = "example",
    shelter = shelter2
)

shelters = [shelter1, shelter2, shelter3]
animals = [animal1, animal2, animal3, animal4, animal5, animal6, animal7, animal8, animal9]
users = [user1, user2, user3]

# Test data
test_shelter = Shelter(
    name = "Example Shelter",
    location = "South London",
    email = "info@example.com",
    phone_number = "07123123123"
)

test_user = User(
    email = "rtest@example.com",
    password = "Chicken123!",
    first_name = "test",
    last_name = "user",
    shelter = test_shelter
)

test_animal_1 = Animal(
    name = "Test One",
    species = "cat",
    age = 1,
    breed = "Maine Coon",
    location = "London",
    male = True,
    bio = "This is a ltest cat.",
    neutered = False,
    lives_with_children = False,
    images = 1,
    isActive = True,
    shelter = test_shelter
)
test_animal_2 = Animal(
    name = "Test Two",
    species = "dog",
    age = 2,
    breed = "test breed",
    location = "London",
    male = True,
    bio = "This is aa test dog.",
    neutered = False,
    lives_with_children = False,
    images = 1,
    isActive = True,
    shelter = test_shelter
)
test_animal_3 = Animal(
    name = "Test Three",
    species = "wolf",
    age = 3,
    breed = "werewolf",
    location = "London",
    male = True,
    bio = "This is a test werewolf.",
    neutered = False,
    lives_with_children = False,
    images = 1,
    isActive = False,
    shelter = test_shelter
)

test_animals = [test_animal_1, test_animal_2, test_animal_3]
#############################################################

# class Animal(db.Model):
#     __tablename__ = 'animals'

#     # TODO - Refactor the code so that this class is not duplicated in the backend code.
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(255))
#     species = db.Column(db.String(50))
#     age = db.Column(db.Integer)
#     breed = db.Column(db.String(50), nullable=False)
#     location = db.Column(db.String(50), nullable=False)
#     male = db.Column(db.Boolean, nullable=False)
#     bio = db.Column(db.String(500), nullable=False)
#     neutered = db.Column(db.Boolean, nullable=False)
#     lives_with_children = db.Column(db.Boolean, nullable=False)
#     image = db.Column(db.String(255))
#     isActive = db.Column(db.Boolean, nullable=False, default=True)
#     shelter_id = db.Column(db.Integer(), db.ForeignKey('shelters.id'))

# ------------------------------------

    # def as_dict(self):
    #     animal_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
    #     shelter_info = db.session.get(Shelter, self.shelter_id)
        # LegacyAPIWarning: The Query.get() method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. 
        # The method is now available as Session.get() (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)
        # shelter_info = Shelter.query.get(self.shelter_id)

        # animal_dict['shelter'] = {
        #     'name': shelter_info.name,
        #     'location': shelter_info.location,
        #     'email': shelter_info.email,
        #     'phone_number': shelter_info.phone_number
        # }
        # return animal_dict

# ------------------------------------

# class User(db.Model):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer(), primary_key=True)

#     email = db.Column(db.String(255), nullable=False)
#     password = db.Column(db.String(255), nullable=False)
#     first_name = db.Column(db.String(255), nullable=False)
#     last_name = db.Column(db.String(255), nullable=False)
#     shelter_id = db.Column(db.Integer, db.ForeignKey('shelters.id'), nullable=False)

#     def as_dict(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# ------------------------------------

# class Shelter(db.Model):
#     __tablename__ = 'shelters'

#     id = db.Column(db.Integer(), primary_key=True)

#     name = db.Column(db.String(255), nullable=False)
#     location = db.Column(db.String(255), nullable=False)
#     email = db.Column(db.String(255), nullable=False)
#     phone_number = db.Column(db.String(20), nullable=False)

#     animals = db.relationship('Animal', backref='shelter', lazy=True)
#     users = db.relationship('User', backref='shelter', lazy=True)

#     def as_dict(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# ------------------------------------
# Email domain name to shelter_id mapping dictionary is here

# email_to_shelter_mapping = {
#     '@batterseadogshome.org': 1,
#     '@cardiffdogshome.org': 2,
#     '@themayhew.org': 3,
#     '@rspca.org.uk': 4
# }
