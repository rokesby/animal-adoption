from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
import uuid

from .base import Base
from sqlalchemy import UUID, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

if TYPE_CHECKING:
    from lib.models import Conversation, User

class Message(Base):
    __tablename__= "messages"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    read_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    content: Mapped[str] = mapped_column(Text)
    conversation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id"))
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    sender: Mapped["User"] = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")
    
    def __repr__(self):
        try:
            read_time_str = self.read_time.isoformat() if self.read_time else None
            return f"Message(id={str(self.id)!r}, created_at={self.created_at.isoformat()!r}, received_at={self.received_at.isoformat()!r}, read_time={read_time_str!r}, content={self.content!r}, conversation_id={str(self.conversation_id)!r}, sender_id={self.sender_id!r})"
        except Exception:
            return f"Message(detached)"
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "created_at": self.created_at,
            "received_at": self.received_at,
            "read_time": self.read_time,
            "content": self.content,
            "conversation_id": self.conversation_id,
            "sender_id": self.sender_id,
            "sender_name": f'{self.sender.first_name} {self.sender.last_name}'
        }
    