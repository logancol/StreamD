from __future__ import annotations
from sqlalchemy import BigInteger, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.sa_base import Base

class ModernTeamIndex(Base):
    __tablename__ = "modern_team_index"
    __table_args__ = (
        PrimaryKeyConstraint("id", "abrev"),
    )
    id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    abrev: Mapped[str] = mapped_column(String(3), nullable=False)
    nickname: Mapped[str | None] = mapped_column(String(256), nullable=True)