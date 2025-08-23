import time
from flask_sqlalchemy import SQLAlchemy

from lib.models.verification import Verification


class VerificationRepository:
    def __init__(self, db_instance: SQLAlchemy):
        self.db = db_instance
        
    def add_verification(self, user_id, hashed_pin):
        verification = Verification(
            user_id=user_id,
            pin_hash=hashed_pin
        )
        self.db.session.add(verification)
        self.db.session.commit()
        return verification
    
    def get_verification_by_id(self, verification_id):
        result = self.db.session.get(Verification, verification_id)
        if result.used_at is not None:
            return None
        else:
            return result
    
    def update_verification_used_at(self, verification_id):
        verification = self.db.session.get(Verification, verification_id)
        setattr(verification, 'used_at', int(time.time()))
        self.db.session.commit()
        return verification