import mongoengine 

def connect_db():
    mongoengine.connect('animal_adoption', host='localhost', port=27017)

def disconnect_db():
    mongoengine.disconnect()
