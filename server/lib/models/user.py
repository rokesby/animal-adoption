from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    first_name: Mapped[str]= mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    shelter_id: Mapped[int] = mapped_column(ForeignKey("shelters.id"))
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r}, password={self.password!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, shelter_id={self.shelter_id!r})"