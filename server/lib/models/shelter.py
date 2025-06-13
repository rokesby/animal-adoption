from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .animal import Animal
from .user import User

class Shelter(Base):
    __tablename__ = "shelters"

    id:Mapped[int] = mapped_column( primary_key=True)
    name:Mapped[str] = mapped_column(String(255), nullable=False)
    location:Mapped[str] = mapped_column(String(255), nullable=False)
    email:Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number:Mapped[str] = mapped_column(String(20))
    animals:Mapped[List["Animal"]] = relationship('Animal', backref='shelter')
    users:Mapped[List["User"]] = relationship('User', backref='shelter')
    
    def __repr__(self) -> str:
        return f"id={self.id!r}, name={self.name!r}, location={self.location!r}, email={self.email!r}, phone_number={self.phone_number!r}, animals={self.animals!r}, users={self.users!r}"