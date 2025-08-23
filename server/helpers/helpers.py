import random
from lib.database_connection import flask_bcrypt

def generate_pin():
    plain_pin = ""
    for n in range(6):
        plain_pin += str(random.randint(0,9))
    
    hashed_pin = flask_bcrypt.generate_password_hash(plain_pin).decode('utf-8') 
    return plain_pin, hashed_pin