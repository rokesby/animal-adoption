from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from lib.models import Animal, User, Conversation

class Shelter(Base):
    __tablename__ = "shelters"

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(255), nullable=False)
    location:Mapped[str] = mapped_column(String(255), nullable=False)
    email:Mapped[str] = mapped_column(String(255), nullable=False)
    domain:Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    phone_number:Mapped[str] = mapped_column(String(20))
    animals:Mapped[List["Animal"]] = relationship('Animal', back_populates='shelter')
    users:Mapped[List["User"]] = relationship('User', back_populates='shelter')
    conversations: Mapped[List["Conversation"]] = relationship('Conversation', back_populates='shelter')
    
    def __repr__(self) -> str:
        return f"id={self.id!r}, name={self.name!r}, location={self.location!r}, email={self.email!r}, phone_number={self.phone_number!r}, animals={self.animals!r}, users={self.users!r}"