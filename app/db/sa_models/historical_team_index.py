from __future__ import annotations
from sqlalchemy import BigInteger, Boolean, Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.sa_base import Base

class HistoricalTeamIndex(Base):
    __tablename__ = "historical_team_index"
    __table_args__ = (
        PrimaryKeyConstraint("id", "nickname", "year_active_til"),
    )
    id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    current_iteration: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    city: Mapped[str | None] = mapped_column(String(256), nullable=True)
    nickname: Mapped[str] = mapped_column(String(256), nullable=False)
    year_founded: Mapped[int | None] = mapped_column(Integer, nullable=True)
    year_active_til: Mapped[int] = mapped_column(Integer, nullable=False)