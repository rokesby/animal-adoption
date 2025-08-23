import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from lib.models import Message, User, Conversation, Animal


class MessageRepository:
    def __init__(self, db_instance: SQLAlchemy):
        self.db = db_instance
    
    def get_message_by_id(self, id):
        result = self.db.session.scalar(select(Message).filter_by(id=id))
        return result
    
    def create_new_message_with_conversation(self, data, user_id, animal_id):
        
        # animal_id=data['animal_id']
        # shelter_id=data['shelter_id']
        # with self.db.session.begin():
        animal = self.db.session.get(Animal, animal_id)
        user = self.db.session.get(User, user_id)
        new_message = Message(
        sender_id=user_id,
        content=data['content'],
        conversation=Conversation(animal_id=animal.id, shelter_id=animal.shelter_id, participants=[user])
        )
        self.db.session.add(new_message)
        self.db.session.commit()
        return new_message
    
    
    def reply_to_conversation(self, data, user_id, conversation_id):
        user = self.db.session.get(User, user_id)
        conversation = self.db.session.get(Conversation, conversation_id)
        new_message = Message(
        sender=user,
        content=data['content'],
        conversation=conversation
        )
        self.db.session.add(new_message)
        
        # only append if the user doesn't already exist in the conversation
        if user not in conversation.participants:
            conversation.participants.append(user)
            
        self.db.session.commit()
        return new_message
    
    def delete_message_id(self, id):
            message = self.db.session.scalar(select(Message).filter_by(id=id))
            self.db.session.delete(message)
            self.db.session.commit()