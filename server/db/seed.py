from pymongo_get_database import get_database
# Get the database using the method we defined in pymongo_test_insert file

dbname = get_database()

##################################################


collection_name = dbname["shelters"]
collection_name.drop()

# TODO : RJ - Create an environment variable for the database name.

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

collection_name.insert_many([s_item_1,s_item_2])

##################################################


collection_name_2 = dbname["aa_users"] # Clash with Acebook.
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


