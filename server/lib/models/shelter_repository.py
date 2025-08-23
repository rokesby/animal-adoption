from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

from lib.models.shelter import Shelter


class ShelterRepository:
    def __init__(self, db_instance: SQLAlchemy):
        self.db = db_instance
        
    def get_shelter_id_by_domain(self, domain):
        result = self.db.session.scalar(select(Shelter.id).filter_by(domain=domain))
        return result
    