from __future__ import annotations

from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.sa_base import Base


class Player(Base):
    __tablename__ = "player"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    full_name: Mapped[str | None] = mapped_column(String(256), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(256), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(256), nullable=True)
    is_active: Mapped[bool | None] = mapped_column(Boolean, nullable=True)