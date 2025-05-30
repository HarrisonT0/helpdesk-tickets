from ..database import db
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Boolean
from datetime import datetime


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True
    )
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    admin: Mapped[bool] = mapped_column(Boolean, default=False)

    tickets: Mapped[list["Ticket"]] = relationship(
        "Ticket", back_populates="author", cascade="all, delete-orphan"
    )
