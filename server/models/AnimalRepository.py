# This is where the CRUD functions for Animals lives

from models.Animal import Animal
class AnimalRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * from listings')
        return [Listing(row["id"], row["name"], row["description"], row["price_per_night"], row["available_from"], row["available_to"], row["user_id"]) for row in rows]
    
    def find_by_id(self, id):
        rows = self._connection.execute('SELECT * from listings WHERE id = %s', [id])
        row = rows[0]
        return Listing(row["id"], row["name"], row["description"], row["price_per_night"], row["available_from"], row["available_to"], row["user_id"])
    
    def create(self, listing):
        rows = self._connection.execute('INSERT INTO listings (name, description, price_per_night, available_from, available_to, user_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id', [listing.name, listing.description, listing.price_per_night, listing.available_from, listing.available_to, listing.user_id])
        row = rows[0]
        listing.id = row["id"]
        return listing
    
    def delete(self, id):
        self._connection.execute('DELETE FROM listings WHERE id = %s', [id])
        return None