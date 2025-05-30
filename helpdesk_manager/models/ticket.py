from ..database import db
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Ticket(db.Model):
    __tablename__ = "ticket"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
