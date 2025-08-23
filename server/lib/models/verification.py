from datetime import datetime
import time
import uuid
from lib.models import Base
from sqlalchemy import UUID, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Verification(Base):
    __tablename__ = "verifications"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    pin_hash: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[int] = mapped_column(Integer, default=lambda: int(time.time()))
    used_at: Mapped[int] = mapped_column(Integer, nullable=True)
    expires_at: Mapped[int] = mapped_column(Integer, default=lambda: int(time.time()) + 900) 

    def __repr__(self):
        return f"Verification(id={self.id!r}, created_at:{self.created_at!r}, expires_at{self.expires_at!r})"