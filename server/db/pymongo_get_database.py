from pymongo import MongoClient

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   #CONNECTION_STRING = "mongodb+srv://user:pass@cluster.mongodb.net/myFirstDatabase"
   CONNECTION_STRING = "mongodb://0.0.0.0/"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['acebook']
   #return client['adoptions']
  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
    # Get the database
    dbname = get_database()
    print(dbname)

    