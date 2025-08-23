from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

from lib.models.user import User
class UserRepository:
    def __init__(self, db_instance: SQLAlchemy):
        self.db = db_instance
        
    def get_user_by_id(self, user_id):
        user = self.db.session.get(User, user_id)
        return user
    
    def get_user_by_email(self, email):
        user = self.db.session.scalar(select(User).filter_by(email=email))
        return user
        
    def create_user(self, data):
        
        user = User(
        email=data['email'],
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        shelter_id=data.get('shelter_id')
        # verified is False by default
    )
        self.db.session.add(user)
        self.db.session.commit()
        return user
    
    def update_user(self, user_id, data):
        user = self.db.session.get(User, user_id)
        
        for key, value in data.items():
            if hasattr(user, key):
                    setattr(user, key, value)
            else:
                raise AttributeError(f"attribute {key} doesn't exist")        
        
        self.db.session.commit()
        return user