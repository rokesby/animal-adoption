from lib.database_connection import flask_bcrypt
from helpers.helpers import *

def test_generate_pin():
    """
    generate_pin should generate a 6 digit plain pin
    AND hash the pin
    THEN return both
    """
    
    plain_pin, hashed_pin = generate_pin()
    
    assert len(plain_pin) == 6
    assert plain_pin.isdigit()
    
    assert flask_bcrypt.check_password_hash(hashed_pin, plain_pin)
    
def test_generate_pin_creates_different_pins():
    """
    generate_pin should create a different pin each time
    """
    
    pin_1, _ = generate_pin()
    pin_2, _ = generate_pin()
    pin_3, _ = generate_pin()
    
    assert pin_1 != pin_2 != pin_3
    
def test_generate_pin_within_valid_range():
    """
    pins should be generated between range of 100000-999999
    """
    
    for n in range(20):
        plain_pin, _ = generate_pin()
        assert int(plain_pin) <= 999999 and int(plain_pin) > 0

def test_generate_pin_hash_format():
    """
    generate_pin should return a hash as a utf-8 string
    """
    _, hashed_pin = generate_pin()
    
    assert isinstance(hashed_pin, str)