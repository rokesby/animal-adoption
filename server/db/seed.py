import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# Select the database.
# TODO : RJ - Create an environment variable for the database name.
mydb = myclient["adoption"]
# print(myclient.list_database_names())


##################################################
# Create shelters

mycol = mydb["shelters"]
mycol.drop()

s_item_1 = {
  "_id" : "S01",
  "name" : "Wood Green Shelter",
  "location" : "North London",
  "email" : "info@woodgreen.org",
}


s_item_2 = {
  "_id" : "S02",
  "name" : "Cardiff Dogs Home",
  "location" : "Cardiff",
  "email" : "info@cardiffdogs.org",
}

mycol.insert_many([s_item_1,s_item_2])


##################################################
# Create users.

collection_name_2 = mydb["users"] # Clash with Acebook.
collection_name_2.drop()

u_item_1 = {
  "_id" : "U01",
  "firstName" : "Reza",
  "lastName" : "Jugon",
  "email" : "reza@cardiffdogs.org",
  "shelter" : "Y"
}

u_item_2 = {
  "_id" : "U02",
  "firstName" : "Marya",
  "lastName" : "Shariq",
  "email" : "marya@woodgreen.org",
  "shelter" : "Y"
}

collection_name_2.insert_many([u_item_1, u_item_2])


##################################################
# Create animals.

collection_name_3 = mydb["animals"] # Clash with Acebook.
collection_name_3.drop()

u_item_1 = {
  "_id" : "U01",
  "name" : "Bobby",
  "species" : "cat",
  "age" : 7,
  "breed" : "British Shorthair",
  "location" : "Cardiff",
  "sex" : False,
  "bio" : "This is a lovely cat and he needs a good home.",
  "neutered" : False,
  "lives_with_children" : True,
}


u_item_2 = {
  "_id" : "U02",
  "name" : "Roger",
  "species" : "dog",
  "age" : 4,
  "breed" : "German Shepherd",
  "location" : "London",
  "sex" : True,
  "bio" : "This is a lovely dog and he needs a good home.",
  "neutered" : True,
  "lives_with_children" : False
}


collection_name_3.insert_many([u_item_1, u_item_2])
