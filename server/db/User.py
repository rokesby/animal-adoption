from mongoengine import Document
from mongoengine import StringField
from mongoengine import BooleanField
from mongoengine import *


# Tutorial
# https://docs.vultr.com/how-to-use-mongodb-in-python-with-mongoengine

# Data types:
# https://docs.mongoengine.org/guide/defining-documents.html

from mongoengine import *
# Connect to a MongoDB instance
connect('adoption')


# Define the schema
class Users(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    shelter = BooleanField(required=True)


# Example document insertion
user1 = Users(
    email="reza@jugon.com",
    first_name="Reza",
    last_name="Jugon",
    shelter=True
)
user1.save()



    