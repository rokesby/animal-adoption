from sqlalchemy import Boolean, ForeignKey,String
from .base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Animal(Base):
    __tablename__ = "animals"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    species: Mapped[str] = mapped_column(String(50))
    age: Mapped[int]
    breed: Mapped[str] = mapped_column(String(50), nullable=False)
    location: Mapped[str] = mapped_column(String(50), nullable=False)
    male: Mapped[bool] = mapped_column(Boolean, nullable=False)
    bio: Mapped[str] = mapped_column(String(2048), nullable=False)
    neutered: Mapped[bool] = mapped_column(Boolean, nullable=False)
    lives_with_children: Mapped[bool] = mapped_column(Boolean, nullable=False)
    images: Mapped[int]
    profileImageId: Mapped[str] = mapped_column(String(50), nullable=True)
    isActive: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    shelter_id: Mapped[int] = mapped_column(ForeignKey("shelters.id"))
    
    def __repr__(self):
        try:
            return f"Animal(id={self.id!r}, name={self.name!r}, species={self.species!r}, age={self.age!r}, breed={self.breed!r},location={self.location!r},male={self.male!r}, bio={self.bio!r}, neutered={self.neutered!r}, lives_with_children={self.lives_with_children!r}, images={self.images!r}, profileImageId={self.profileImageId!r}, isActive={self.isActive!r}, shelter_id={self.shelter_id!r})"
        except Exception:
            return f"Animal(detached)"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "breed": self.breed,
            "location": self.location,
            "male": self.male,
            "bio": self.bio,
            "neutered": self.neutered,
            "lives_with_children": self.lives_with_children,
            "images": self.images,
            "profileImageId": self.profileImageId,
            "isActive": self.isActive,
            "shelter_id": self.shelter_id
        }