from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, or_, select
from sqlalchemy.orm import selectinload
from lib.models import Conversation, Message, User
from lib.models.conversation_participants import conversation_participants


class ConversationRepository:
    def __init__(self, db_instance: SQLAlchemy):
        self.db = db_instance
        
    def get_all_conversations(self):
        result = self.db.session.scalars(select(Conversation)).all()
        return result
        
    
    def get_conversation_by_id(self, id):
        result = self.db.session.get(Conversation, id)
        return result
    
    def get_conversation_by_animal_and_user(self, user_id, animal_id):
        result = self.db.session.scalar(
            select(Conversation).where(
                Conversation.participants.any(User.id == user_id), 
                Conversation.animal_id==animal_id)
            )
        return result
    
    def get_conversation_messages(self, conversation_id):
        result = self.db.session.scalars(select(Message).filter_by(conversation_id=conversation_id)).all()
        return result
    
    def get_user_conversations(self, user_id):
        user = self.db.session.get(User, user_id)
        result = user.conversations
        return result
    
    def get_shelter_conversations(self, shelter_id):
        result = self.db.session.scalars(select(Conversation).filter_by(shelter_id=shelter_id)).all()
        return result
    
    def get_shelter_conversations_with_message(self, shelter_id):
        
        latest_message_time = (select(func.max(Message.created_at))
                                .where(Message.conversation_id == Conversation.id)
                                .correlate(Conversation)
                                .scalar_subquery()
                                )
            
        results = self.db.session.execute(select(Conversation, Message)
                                                .join(Message, Conversation.id == Message.conversation_id)
                                                .where(Conversation.shelter_id == shelter_id)
                                                .where(Message.created_at == latest_message_time)
                                                ).all()
            
        return results 
    
    def create_conversation(self, data):
        with self.db.session.begin():
            user = self.db.session.get(User, data['user_id'])
            conversation = Conversation(
                animal_id=data['animal_id'],
                shelter_id=data['shelter_id'],
                participants=[user]
            )
            self.db.session.add(conversation)
        return conversation
    
    def add_participant(self, data):
        conversation = self.db.session.get(Conversation, data['conversation_id'])
        if not conversation:
            raise ValueError("Conversation not found")
        
        user = self.db.session.get(User, data['user_id'])
        if not user:
            raise ValueError("User not found")
        
        if user not in conversation.participants:
            conversation.participants.append(user)
            
        self.db.session.commit()
        
        return conversation
    