from mongoengine import *
# Connect to a MongoDB instance
connect('adoption') 
# TODO - Push into the DB connection.


# Get all of the listings for all shelters.
from User import Users

counter = 0
for user in Users.objects:
    counter += 1
    print(counter, " : ", user.first_name, " : ", user.last_name,  " : ", user.email,  " : ", user.id,  " : ", user.shelter)


# # Get all of the shelters
from User import Users

# for user in Users.objects:
#     print(user.first_name, " : ", user.last_name,  " : ", user.email,  " : ", user.id)



# # Get all of the listings for all shelters.
# from User import Users

# for user in Users.objects:
#     print(user.first_name, " : ", user.last_name,  " : ", user.email,  " : ", user.id)        