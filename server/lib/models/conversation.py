from datetime import datetime
from typing import List, Optional
import uuid

from lib.models.conversation_participants import conversation_participants

from .base import Base
from sqlalchemy import UUID, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from lib.models import Animal, Shelter, Message, User

class Conversation(Base):
    __tablename__="conversations"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shelter_id: Mapped[int] = mapped_column(ForeignKey("shelters.id"))
    animal_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("animals.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    participants: Mapped[List["User"]] = relationship("User", secondary=conversation_participants, back_populates="conversations")
    owner: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    animal: Mapped["Animal"] = relationship("Animal", back_populates="conversations")
    shelter: Mapped["Shelter"] = relationship("Shelter", back_populates="conversations")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="conversation")
    
    def __repr__(self):
        try:
            created_at_str = self.created_at.isoformat() if self.created_at else None
            updated_at_str = self.updated_at.isoformat() if self.updated_at else None
            return f"Conversation(id={str(self.id)!r}, shelter_id={self.shelter_id!r}, animal_id={str(self.animal_id)!r}, created_at={created_at_str!r}, updated_at={updated_at_str})"
        except Exception:
            return f"Conversation(detached)"
        
    def to_dict(self):
        return {
            "id": str(self.id),
            "shelter_id": self.shelter_id,
            "animal_id": str(self.animal_id),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            # "owner_id": self.owner
        }