from sqlalchemy import UUID, Column, Integer, Table, ForeignKey
from sqlalchemy.orm import mapped_column

from lib.models.base import Base


conversation_participants = Table(
    'conversation_participants',
    Base.metadata,
    Column('conversation_id', UUID(as_uuid=True), ForeignKey('conversations.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)