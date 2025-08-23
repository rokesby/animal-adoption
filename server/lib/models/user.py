from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lib.models.conversation_participants import conversation_participants
from .base import Base

if TYPE_CHECKING:
    from lib.models import Shelter, Message, Conversation

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    first_name: Mapped[str]= mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    shelter_id: Mapped[Optional[int]] = mapped_column(ForeignKey("shelters.id"))
    shelter: Mapped["Shelter"] = relationship("Shelter", back_populates="users")
    sent_messages: Mapped[List["Message"]] = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    conversations: Mapped[List["Conversation"]] = relationship("Conversation", secondary=conversation_participants,back_populates="participants")
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, shelter_id={self.shelter_id!r})"