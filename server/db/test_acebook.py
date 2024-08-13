from pymongo import MongoClient
uri = "mongodb://0.0.0.0/"

client = MongoClient(uri)
try:
    database = client.get_database("acebook")
    posts = database.get_collection("posts")
    
    # Query for a movie that has the title 'Back to the Future'
    query = { "message": "This is my test post" }
    post = posts.find_one(query)
    print("Here is the item : ", post)
    client.close()

except Exception as e:
    raise Exception("Unable to find the document due to the following error: ", e)
